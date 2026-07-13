from .base import BaseConnector
from ._fixtures import load


class GoogleDriveConnector(BaseConnector):
    display_name = "Google Drive"
    category = "documentation"
    env_url_var = "GDRIVE_MCP_URL"
    env_token_var = "GDRIVE_OAUTH_TOKEN"

    def fetch(self):
        return load("docs")
