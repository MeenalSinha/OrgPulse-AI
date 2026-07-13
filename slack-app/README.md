# OrgPulse AI - Slack App

Bolt for Python app providing the Slack-native experience: @mentions,
`/orgpulse` slash command, App Home tab, and proactive alerts.

## Setup

1. Create a Slack app at https://api.slack.com/apps using the provided
   `slack-app/manifest.yaml` as a starting point (Bot Token Scopes:
   `app_mentions:read`, `chat:write`, `commands`, `channels:history`).
2. Enable Socket Mode and generate an app-level token (`xapp-...`).
3. Install the app to your workspace to get a bot token (`xoxb-...`).
4. Copy `.env.example` to `.env` and fill in:
   - `SLACK_BOT_TOKEN`
   - `SLACK_APP_TOKEN`
   - `BACKEND_URL` (defaults to `http://localhost:8000`)
5. `pip install -r requirements.txt && python app.py`

## Commands

- `@OrgPulse <question>` - ask anything, answered with citations from the
  organizational memory graph.
- `/orgpulse status` - posts the daily intelligence digest.
- `/orgpulse risks` - posts the current highest-risk blocker chain.
- `/orgpulse experts <topic>` - finds top experts on a topic.

## Proactive alerts

`scripts/send_daily_digest.py` (backend) is intended to be run on a schedule
(Celery beat / cron) and posts `daily_digest_blocks` to a configured channel.
