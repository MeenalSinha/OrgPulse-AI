from .base import BaseConnector
from ._fixtures import load


class JiraConnector(BaseConnector):
    display_name = "Jira"
    category = "project_management"
    env_url_var = "JIRA_MCP_URL"
    env_token_var = "JIRA_API_TOKEN"

    def fetch(self):
        return load("tickets")
