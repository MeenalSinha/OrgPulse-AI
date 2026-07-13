# MCP Connectors

Shared connector layer used by both the FastAPI backend (`/api/integrations`)
and the Slack app. Every connector implements `base.BaseConnector` and ships
in **mock mode** by default, returning data from `data/fixtures/*.json`, so
the whole platform runs without any external credentials.

## Adding a new connector

1. Create `my_source_connector.py` subclassing `BaseConnector`, setting
   `display_name`, `category`, `env_url_var`, `env_token_var`, and
   implementing `fetch()`.
2. Register it in `registry.py`.

## Going live

Set `MCP_MODE=live` and the connector's `env_url_var` (e.g. `GITHUB_MCP_URL`)
to a real MCP server endpoint. `BaseConnector.connect()` documents the exact
`mcp.client.sse` session code to use. Connectors can be flipped to live
independently of one another.

## Connectors included

| Connector | Category | Env var |
|---|---|---|
| GitHub | code | `GITHUB_MCP_URL` |
| GitLab | code | `GITLAB_MCP_URL` |
| Jira | project_management | `JIRA_MCP_URL` |
| Linear | project_management | `LINEAR_MCP_URL` |
| Azure DevOps | project_management | `AZURE_DEVOPS_MCP_URL` |
| Notion | documentation | `NOTION_MCP_URL` |
| Confluence | documentation | `CONFLUENCE_MCP_URL` |
| Google Drive | documentation | `GDRIVE_MCP_URL` |
| Slack | communication | `SLACK_MCP_URL` |
| Google Calendar | scheduling | `GCAL_MCP_URL` |
| Figma | design | `FIGMA_MCP_URL` |
