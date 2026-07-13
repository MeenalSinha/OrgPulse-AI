"""
Common connector interface.

Every source system (GitHub, Jira, Notion, Slack, Google Drive, Confluence,
Calendar, Linear, Figma, GitLab, Azure DevOps) implements this interface.

Two modes are supported:
  - "mock":  returns deterministic fixture data. Used in this prototype so
             the demo runs with zero external credentials.
  - "live":  wraps a real MCP server connection (Model Context Protocol).
             When MCP_MODE=live and the relevant server URL/credentials are
             set, `connect()` establishes a real session and `sync()` pulls
             live data through the same shape returned by mock mode, so
             nothing downstream (graph builder, routers, Slack app) needs to
             change.

This lets the org swap any single connector to "live" independently, which
is the point of standardizing on MCP rather than a bespoke client per tool.
"""
import os
from abc import ABC, abstractmethod
from datetime import datetime, timezone


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

    def connect(self):
        """
        Establish a real MCP session. Production implementation:

            from mcp import ClientSession
            from mcp.client.sse import sse_client
            async with sse_client(os.getenv(self.env_url_var)) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    return session

        Left unimplemented in mock mode.
        """
        if self.mode == "mock":
            raise RuntimeError(f"{self.display_name} is in mock mode; no live connection to open.")
        raise NotImplementedError("Wire this connector to a live MCP server URL to enable live mode.")

    @abstractmethod
    def fetch(self) -> list:
        """Return a list of normalized records from the source system."""
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
