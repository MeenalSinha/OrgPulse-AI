"""
Common connector interface.

Every source system (GitHub, Jira, Notion, Slack, Google Drive, Confluence,
Calendar, Linear, Figma, GitLab, Azure DevOps) implements this interface.

Two modes are supported:
  - "mock":  returns deterministic fixture data. Used in this prototype so
             the demo runs with zero external credentials.
  - "live":  wraps a real MCP server connection (Model Context Protocol).
             When MCP_MODE=live and the relevant server URL/credentials are
             set, connect() establishes a real session and live_list_tools() /
             live_call_tool() communicate using the official MCP protocol.

This lets the org swap any single connector to "live" independently, which
is the point of standardizing on MCP rather than a bespoke client per tool.
"""
import os
import asyncio
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any


class BaseConnector(ABC):
    display_name: str = "Unnamed Connector"
    category: str = "general"
    env_url_var: str = ""
    env_token_var: str = ""

    def __init__(self):
        self.mode = "live" if (
            os.getenv("MCP_MODE", "mock") == "live"
            and self.env_url_var
            and os.getenv(self.env_url_var)
        ) else "mock"
        self._last_sync = None

    def status(self) -> str:
        if self.mode == "live":
            return "connected"
        return "mock" if os.getenv("MCP_MODE", "mock") == "mock" else "not_configured"

    def _get_server_url(self) -> str | None:
        return os.getenv(self.env_url_var) if self.env_url_var else None

    # ------------------------------------------------------------------ #
    #  Real MCP session helpers                                            #
    # ------------------------------------------------------------------ #

    def live_list_tools(self) -> list[dict]:
        """
        Connects to the real MCP server via SSE and calls list_tools().
        Returns a list of tool descriptors from the live MCP server.
        Raises RuntimeError if in mock mode or if no server URL is set.
        """
        url = self._get_server_url()
        if not url:
            raise RuntimeError(
                f"{self.display_name}: MCP_MODE=live but {self.env_url_var} is not set."
            )
        return asyncio.run(self._async_list_tools(url))

    def live_call_tool(self, tool_name: str, arguments: dict | None = None) -> Any:
        """
        Connects to the real MCP server via SSE and invokes a specific tool.
        Returns the tool result content.
        Raises RuntimeError if in mock mode or if no server URL is set.
        """
        url = self._get_server_url()
        if not url:
            raise RuntimeError(
                f"{self.display_name}: MCP_MODE=live but {self.env_url_var} is not set."
            )
        return asyncio.run(self._async_call_tool(url, tool_name, arguments or {}))

    @staticmethod
    async def _async_list_tools(server_url: str) -> list[dict]:
        """
        Opens an MCP SSE session, calls initialize + list_tools, returns
        a JSON-serialisable list of tool descriptors.
        """
        from mcp import ClientSession
        from mcp.client.sse import sse_client

        async with sse_client(server_url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                response = await session.list_tools()
                return [
                    {
                        "name": tool.name,
                        "description": tool.description or "",
                        "input_schema": tool.inputSchema if hasattr(tool, "inputSchema") else {},
                    }
                    for tool in response.tools
                ]

    @staticmethod
    async def _async_call_tool(server_url: str, tool_name: str, arguments: dict) -> Any:
        """
        Opens an MCP SSE session, calls initialize + call_tool, returns result content.
        """
        from mcp import ClientSession
        from mcp.client.sse import sse_client

        async with sse_client(server_url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                # Return the content blocks as plain dicts
                return [
                    {"type": getattr(block, "type", "text"), "text": getattr(block, "text", str(block))}
                    for block in result.content
                ]

    # ------------------------------------------------------------------ #
    #  Mock / abstract interface                                           #
    # ------------------------------------------------------------------ #

    @abstractmethod
    def fetch(self) -> list:
        """Return a list of normalized records from the source system (mock mode)."""
        raise NotImplementedError

    def sync(self) -> dict:
        records = self.fetch()
        self._last_sync = datetime.now(timezone.utc).isoformat()
        return {
            "connector": self.display_name,
            "mode": self.mode,
            "synced_at": self._last_sync,
            "record_count": len(records),
        }
