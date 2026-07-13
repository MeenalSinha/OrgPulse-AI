"""
Handles @OrgPulse mentions in channels and threads. Extracts the question,
calls the backend /api/chat endpoint, and replies in-thread with a
Block Kit formatted, cited answer - or, for "Can we ship on Friday?" style
questions, the dedicated release-readiness card (verdict, chain, mitigation,
recommended expert).
"""
import re
import httpx

from blocks import answer_blocks, release_readiness_blocks
from config import BACKEND_URL


def strip_bot_mention(text: str) -> str:
    return re.sub(r"<@[^>]+>", "", text).strip()


def register(app):
    @app.event("app_mention")
    def handle_mention(event, say, client):
        question = strip_bot_mention(event.get("text", ""))
        if not question:
            say(text="Ask me something about your organization, for example: "
                     "\"Can we ship the Mobile App on Friday?\"", thread_ts=event.get("ts"))
            return

        try:
            resp = httpx.post(f"{BACKEND_URL}/api/chat", json={"query": question}, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPError:
            say(text="OrgPulse could not reach the backend right now. Please try again shortly.",
                thread_ts=event.get("ts"))
            return

        if data.get("release_readiness"):
            blocks = release_readiness_blocks(data["release_readiness"])
            say(blocks=blocks, text=f"{data['release_readiness']['verdict']} - {data['release_readiness']['release_name']}",
                thread_ts=event.get("ts"))
            return

        blocks = answer_blocks(question, data["answer"], data["citations"], data["confidence"])
        say(blocks=blocks, text=data["answer"], thread_ts=event.get("ts"))
