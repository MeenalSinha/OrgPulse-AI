from .base import BaseConnector
from ._fixtures import load


class GitHubConnector(BaseConnector):
    display_name = "GitHub"
    category = "code"
    env_url_var = "GITHUB_MCP_URL"
    env_token_var = "GITHUB_TOKEN"

    def fetch(self):
        """Returns repositories and pull requests, normalized for the knowledge graph."""
        return load("repos") + load("pull_requests")
