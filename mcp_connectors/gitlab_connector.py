from .base import BaseConnector
from ._fixtures import load


class GitLabConnector(BaseConnector):
    display_name = "GitLab"
    category = "code"
    env_url_var = "GITLAB_MCP_URL"
    env_token_var = "GITLAB_TOKEN"

    def fetch(self):
        # Mirrors GitHub connector shape; kept separate so orgs on GitLab can
        # point this at a real MCP server without touching GitHub config.
        return load("repos")
