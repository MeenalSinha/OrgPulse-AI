from .base import BaseConnector
from ._fixtures import load


class ConfluenceConnector(BaseConnector):
    display_name = "Confluence"
    category = "documentation"
    env_url_var = "CONFLUENCE_MCP_URL"
    env_token_var = "CONFLUENCE_API_TOKEN"

    def fetch(self):
        return [d for d in load("docs") if d["type"] in ("Architecture Doc", "Runbook")]
