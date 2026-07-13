from .base import BaseConnector
from ._fixtures import load


class GoogleCalendarConnector(BaseConnector):
    display_name = "Google Calendar"
    category = "scheduling"
    env_url_var = "GCAL_MCP_URL"
    env_token_var = "GCAL_OAUTH_TOKEN"

    def fetch(self):
        # Derives meeting-shaped records from release + decision dates for the demo.
        releases = load("releases")
        return [{"title": r["name"], "date": r["date"], "type": "release_review"} for r in releases]
