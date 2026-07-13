"""
App Home tab: personal snapshot shown when a user opens the OrgPulse app in
the Slack sidebar. Publishes on `app_home_opened`.
"""
import httpx

from config import BACKEND_URL


def register(app):
    @app.event("app_home_opened")
    def update_home_tab(client, event):
        try:
            summary = httpx.get(f"{BACKEND_URL}/api/dashboard/summary", timeout=15).json()
            insights = httpx.get(f"{BACKEND_URL}/api/dashboard/ai-insights", timeout=15).json()
        except httpx.HTTPError:
            summary, insights = {}, []

        insight_blocks = [
            {"type": "section", "text": {"type": "mrkdwn", "text": f"- {i['text']}"}}
            for i in insights
        ]

        client.views_publish(
            user_id=event["user"],
            view={
                "type": "home",
                "blocks": [
                    {"type": "header", "text": {"type": "plain_text", "text": "OrgPulse AI"}},
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Org Health:*\n{summary.get('org_health_score', '-')}/100"},
                            {"type": "mrkdwn", "text": f"*At-Risk Projects:*\n{summary.get('at_risk_projects', '-')}"},
                        ],
                    },
                    {"type": "divider"},
                    {"type": "section", "text": {"type": "mrkdwn", "text": "*AI Insights*"}},
                    *insight_blocks,
                ],
            },
        )
