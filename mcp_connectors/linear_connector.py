from .base import BaseConnector
from ._fixtures import load


class LinearConnector(BaseConnector):
    display_name = "Linear"
    category = "project_management"
    env_url_var = "LINEAR_MCP_URL"
    env_token_var = "LINEAR_API_KEY"

    def fetch(self):
        return [t for t in load("tickets") if t["priority"] in ("High", "Critical")]
