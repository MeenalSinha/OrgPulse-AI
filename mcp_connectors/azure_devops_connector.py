from .base import BaseConnector
from ._fixtures import load


class AzureDevOpsConnector(BaseConnector):
    display_name = "Azure DevOps"
    category = "project_management"
    env_url_var = "AZURE_DEVOPS_MCP_URL"
    env_token_var = "AZURE_DEVOPS_PAT"

    def fetch(self):
        return load("tickets")
