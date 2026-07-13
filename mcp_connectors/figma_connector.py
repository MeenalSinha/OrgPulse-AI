from .base import BaseConnector
from ._fixtures import load


class FigmaConnector(BaseConnector):
    display_name = "Figma"
    category = "design"
    env_url_var = "FIGMA_MCP_URL"
    env_token_var = "FIGMA_API_TOKEN"

    def fetch(self):
        # No dedicated design-file fixture yet; represented as design docs.
        return [d for d in load("docs") if d["type"] == "Design Doc"]
