from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from mcp_connectors.registry import CONNECTOR_REGISTRY

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: dict = {}


@router.get("")
def list_integrations():
    return [
        {
            "id": key,
            "name": connector.display_name,
            "category": connector.category,
            "status": connector.status(),
            "mode": connector.mode,
        }
        for key, connector in CONNECTOR_REGISTRY.items()
    ]


@router.post("/{connector_id}/sync")
def sync_connector(connector_id: str):
    connector = CONNECTOR_REGISTRY.get(connector_id)
    if not connector:
        raise HTTPException(status_code=404, detail="Unknown connector")
    return connector.sync()


@router.get("/{connector_id}/tools")
def list_mcp_tools(connector_id: str):
    """
    Connects to the live MCP server for this connector and returns the list
    of tools it exposes (via MCP protocol list_tools call).
    Only works when MCP_MODE=live and the connector's URL env var is set.
    In mock mode, returns a curated list of representative mock tools so
    judges can see what the tool browser looks like without live credentials.
    """
    connector = CONNECTOR_REGISTRY.get(connector_id)
    if not connector:
        raise HTTPException(status_code=404, detail="Unknown connector")

    if connector.mode == "live":
        try:
            tools = connector.live_list_tools()
            return {
                "connector": connector.display_name,
                "mode": "live",
                "mcp_protocol": "list_tools",
                "tools": tools,
            }
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"MCP server error: {exc}")

    # Mock mode: return representative tool stubs so the UI always renders
    mock_tools = _mock_tools_for(connector_id, connector.display_name)
    return {
        "connector": connector.display_name,
        "mode": "mock",
        "mcp_protocol": "list_tools (simulated)",
        "note": "Set MCP_MODE=live and configure the server URL to connect to a real MCP server.",
        "tools": mock_tools,
    }


@router.post("/{connector_id}/call")
def call_mcp_tool(connector_id: str, body: ToolCallRequest):
    """
    Invokes a specific tool on the connector's live MCP server.
    In mock mode, returns a simulated result so the judge-facing demo still works.
    """
    connector = CONNECTOR_REGISTRY.get(connector_id)
    if not connector:
        raise HTTPException(status_code=404, detail="Unknown connector")

    if connector.mode == "live":
        try:
            result = connector.live_call_tool(body.tool_name, body.arguments)
            return {
                "connector": connector.display_name,
                "mode": "live",
                "mcp_protocol": "call_tool",
                "tool": body.tool_name,
                "arguments": body.arguments,
                "result": result,
            }
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"MCP tool call failed: {exc}")

    # Mock mode: return representative simulated result
    return {
        "connector": connector.display_name,
        "mode": "mock",
        "mcp_protocol": "call_tool (simulated)",
        "tool": body.tool_name,
        "arguments": body.arguments,
        "result": [
            {
                "type": "text",
                "text": (
                    f"[Mock MCP result] Tool '{body.tool_name}' was called on the "
                    f"{connector.display_name} connector with arguments {body.arguments}. "
                    f"Set MCP_MODE=live and configure {connector.env_url_var} to get real results."
                ),
            }
        ],
    }


def _mock_tools_for(connector_id: str, display_name: str) -> list[dict]:
    """Returns realistic mock tool descriptors for the named connector."""
    tool_map = {
        "github": [
            {"name": "list_repositories", "description": "List repositories for the authenticated user or org", "input_schema": {"type": "object", "properties": {"org": {"type": "string"}}}},
            {"name": "get_pull_request", "description": "Get details of a specific pull request", "input_schema": {"type": "object", "properties": {"repo": {"type": "string"}, "pr_number": {"type": "integer"}}}},
            {"name": "list_issues", "description": "List open issues for a repository", "input_schema": {"type": "object", "properties": {"repo": {"type": "string"}, "state": {"type": "string", "enum": ["open", "closed", "all"]}}}},
            {"name": "search_code", "description": "Search code across repositories", "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}}},
        ],
        "jira": [
            {"name": "search_issues", "description": "Search Jira issues using JQL", "input_schema": {"type": "object", "properties": {"jql": {"type": "string"}, "max_results": {"type": "integer"}}}},
            {"name": "get_issue", "description": "Get a specific Jira issue by key", "input_schema": {"type": "object", "properties": {"issue_key": {"type": "string"}}}},
            {"name": "list_projects", "description": "List all accessible Jira projects", "input_schema": {"type": "object", "properties": {}}},
            {"name": "get_sprint_board", "description": "Get current sprint details for a board", "input_schema": {"type": "object", "properties": {"board_id": {"type": "integer"}}}},
        ],
        "notion": [
            {"name": "search_pages", "description": "Search Notion pages and databases", "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}}},
            {"name": "get_page", "description": "Get a specific Notion page by ID", "input_schema": {"type": "object", "properties": {"page_id": {"type": "string"}}}},
            {"name": "list_databases", "description": "List all accessible Notion databases", "input_schema": {"type": "object", "properties": {}}},
        ],
        "slack": [
            {"name": "search_messages", "description": "Search Slack messages across channels", "input_schema": {"type": "object", "properties": {"query": {"type": "string"}, "channel": {"type": "string"}}}},
            {"name": "get_channel_history", "description": "Get recent messages from a channel", "input_schema": {"type": "object", "properties": {"channel": {"type": "string"}, "limit": {"type": "integer"}}}},
            {"name": "list_channels", "description": "List all public channels", "input_schema": {"type": "object", "properties": {}}},
        ],
    }
    default_tools = [
        {"name": f"list_{connector_id}_items", "description": f"List items from {display_name}", "input_schema": {"type": "object", "properties": {"limit": {"type": "integer"}}}},
        {"name": f"search_{connector_id}", "description": f"Search {display_name} content", "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}}},
        {"name": f"get_{connector_id}_item", "description": f"Get a specific {display_name} item by ID", "input_schema": {"type": "object", "properties": {"id": {"type": "string"}}}},
    ]
    return tool_map.get(connector_id, default_tools)
