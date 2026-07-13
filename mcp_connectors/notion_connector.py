from .base import BaseConnector
from ._fixtures import load


class NotionConnector(BaseConnector):
    display_name = "Notion"
    category = "documentation"
    env_url_var = "NOTION_MCP_URL"
    env_token_var = "NOTION_API_KEY"

    def fetch(self):
        return [d for d in load("docs") if d["type"] in ("RFC", "Design Doc")]
