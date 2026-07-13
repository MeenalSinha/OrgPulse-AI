import os

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET", "")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN", "")  # xapp-... for Socket Mode
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
