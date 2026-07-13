"""
Slash command handlers: /orgpulse status | risks | experts <topic>
"""
import httpx

from blocks import risk_alert_blocks, daily_digest_blocks, expert_result_blocks
from config import BACKEND_URL

BACKEND_DOWN_MESSAGE = (
    "OrgPulse could not reach the backend right now. Please try again shortly, "
    "or check that the FastAPI server is running."
)


def _safe_get(path: str, **kwargs):
    """
    Wraps httpx.get with consistent timeout + error handling so every
    subcommand degrades gracefully instead of raising an uncaught exception
    that would make the slash command silently fail in Slack.
    Returns None on any network/HTTP error.
    """
    try:
        r = httpx.get(f"{BACKEND_URL}{path}", timeout=15, **kwargs)
        r.raise_for_status()
        return r
    except httpx.HTTPError:
        return None


def register(app):
    @app.command("/orgpulse")
    def handle_command(ack, respond, command):
        ack()
        text = (command.get("text") or "").strip()
        parts = text.split(maxsplit=1)
        subcommand = parts[0].lower() if parts else "status"
        arg = parts[1] if len(parts) > 1 else ""

        if subcommand in ("status", ""):
            r = _safe_get("/api/dashboard/summary")
            if r is None:
                respond(text=BACKEND_DOWN_MESSAGE)
                return
            respond(blocks=daily_digest_blocks(r.json()), text="OrgPulse status")

        elif subcommand == "risks":
            r = _safe_get("/api/dependency-graph/critical-path")
            if r is None:
                respond(text="No active blocker chains detected, or the backend is unreachable.")
                return
            chain = r.json()
            blocks = risk_alert_blocks(
                title="Active blocker chain detected",
                probability=chain["risk_score"],
                chain=chain["labels"],
                recommendation="Fast-track the upstream blocker to protect downstream releases.",
            )
            respond(blocks=blocks, text="OrgPulse risk alert")

        elif subcommand == "experts":
            if not arg:
                respond(text="Usage: /orgpulse experts <topic>")
                return
            r = _safe_get("/api/experts/search", params={"topic": arg})
            if r is None:
                respond(text=BACKEND_DOWN_MESSAGE)
                return
            respond(blocks=expert_result_blocks(arg, r.json()), text=f"Experts on {arg}")

        else:
            respond(text="Unknown subcommand. Try: status, risks, experts <topic>")
