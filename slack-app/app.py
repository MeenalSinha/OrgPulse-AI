"""
OrgPulse AI Slack app entrypoint (Bolt for Python, Socket Mode).

Run:
    python app.py

Requires SLACK_BOT_TOKEN and SLACK_APP_TOKEN (Socket Mode) to be set, or
SLACK_SIGNING_SECRET if switching to the Events API/HTTP mode instead - see
README.md for both setups.
"""
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN, SLACK_SIGNING_SECRET
from handlers import mentions, commands, home_tab

logging.basicConfig(level=logging.INFO)

app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

mentions.register(app)
commands.register(app)
home_tab.register(app)


if __name__ == "__main__":
    if not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN:
        raise SystemExit(
            "Set SLACK_BOT_TOKEN and SLACK_APP_TOKEN environment variables before starting "
            "the Slack app. See slack-app/README.md for setup instructions."
        )
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
