from .base import BaseConnector
from ._fixtures import load


class SlackConnector(BaseConnector):
    display_name = "Slack"
    category = "communication"
    env_url_var = "SLACK_MCP_URL"
    env_token_var = "SLACK_BOT_TOKEN"

    def fetch(self):
        return load("conversations")
