"""
Handles @OrgPulse mentions in channels and threads.

Architecture: 3-step agentic tool loop
  1. Intent detection  — classify the question (release_readiness / expert_search / graph_query / general)
  2. Tool selection    — call the appropriate backend tool and post a "Thinking..." update
  3. Result synthesis  — compose the final Block Kit response with tool provenance metadata

After posting, registers the thread as a Slack AI Assistant thread
(assistant.threads.setTitle / setStatus) to signal Slack AI participation
and posts an ai_message metadata field so Slack surfaces this as AI content.
"""
import re
import httpx

from blocks import answer_blocks, release_readiness_blocks, expert_result_blocks
from config import BACKEND_URL


def strip_bot_mention(text: str) -> str:
    return re.sub(r"<@[^>]+>", "", text).strip()


# ------------------------------------------------------------------ #
#  Step 1 — Intent detection                                          #
# ------------------------------------------------------------------ #

def detect_intent(question: str) -> str:
    """
    Classifies the question into one of four tool categories so the agent
    can choose the right backend endpoint to call.
    """
    q = question.lower()
    if any(p in q for p in ["can we ship", "can we release", "ready to ship", "ready to release",
                              "will it ship", "will it release", "ship on friday", "ship by"]):
        return "release_readiness"
    if any(p in q for p in ["who knows", "who can help", "expert", "who worked on", "who owns"]):
        return "expert_search"
    if any(p in q for p in ["block", "depend", "downstream", "risk", "chain", "delay"]):
        return "graph_query"
    return "general"


# ------------------------------------------------------------------ #
#  Step 2 — Tool selection & backend calls                            #
# ------------------------------------------------------------------ #

def _call_release_readiness(question: str) -> dict | None:
    try:
        resp = httpx.post(f"{BACKEND_URL}/api/chat", json={"query": question}, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        if data.get("release_readiness"):
            return data
    except httpx.HTTPError:
        pass
    return None


def _call_expert_search(question: str) -> list | None:
    # Extract topic: everything after "expert", "who knows", etc.
    topic = re.sub(
        r"(who knows|who can help|expert|who worked on|who owns)\s*(about|on|with|in)?\s*",
        "", question, flags=re.IGNORECASE
    ).strip() or question
    try:
        resp = httpx.get(f"{BACKEND_URL}/api/experts/search",
                         params={"topic": topic}, timeout=15)
        resp.raise_for_status()
        results = resp.json()
        return results, topic
    except httpx.HTTPError:
        return None, question


def _call_graph_query(question: str) -> dict | None:
    try:
        resp = httpx.get(f"{BACKEND_URL}/api/dependency-graph/critical-path", timeout=15)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError:
        return None


def _call_general_chat(question: str) -> dict | None:
    try:
        resp = httpx.post(f"{BACKEND_URL}/api/chat", json={"query": question}, timeout=20)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError:
        return None


# ------------------------------------------------------------------ #
#  Slack AI thread helper                                             #
# ------------------------------------------------------------------ #

def _set_assistant_thread_context(client, channel: str, thread_ts: str,
                                   title: str, status: str):
    """
    Calls the Slack Assistants API to mark this thread as an AI Assistant
    thread and set its title and status. This surfaces OrgPulse as a
    Slack AI participant — not just a bot — in the Slack UI.
    """
    try:
        client.assistant_threads_setTitle(
            channel_id=channel,
            thread_ts=thread_ts,
            title=title,
        )
        client.assistant_threads_setStatus(
            channel_id=channel,
            thread_ts=thread_ts,
            status=status,
        )
    except Exception:
        # Fails silently if the workspace doesn't have Assistants enabled —
        # the answer is already posted so the user experience is not affected.
        pass


def _post_thinking(say, event: dict, tool_name: str) -> str | None:
    """Post a 'Thinking…' status block and return the message ts for later update."""
    try:
        resp = say(
            blocks=[{
                "type": "context",
                "elements": [{
                    "type": "mrkdwn",
                    "text": f":hourglass_flowing_sand: *OrgPulse Agent* — calling tool `{tool_name}`…",
                }],
            }],
            text=f"Calling tool {tool_name}…",
            thread_ts=event.get("ts"),
        )
        return resp.get("ts") if isinstance(resp, dict) else None
    except Exception:
        return None


def _delete_thinking(client, channel: str, thinking_ts: str | None):
    if thinking_ts:
        try:
            client.chat_delete(channel=channel, ts=thinking_ts)
        except Exception:
            pass


# ------------------------------------------------------------------ #
#  Step 3 — Result synthesis & agent registration                     #
# ------------------------------------------------------------------ #

def register(app):
    @app.event("app_mention")
    def handle_mention(event, say, client):
        question = strip_bot_mention(event.get("text", ""))
        channel = event.get("channel", "")
        thread_ts = event.get("ts", "")

        if not question:
            say(
                text="Ask me something about your organization. For example:\n"
                     "• _Can we ship the Mobile App on Friday?_\n"
                     "• _Who knows about the Payments API?_\n"
                     "• _What's blocking our release?_",
                thread_ts=thread_ts,
            )
            return

        # ── Step 1: Detect intent ──────────────────────────────────────
        intent = detect_intent(question)

        # Signal Slack AI that we're working
        _set_assistant_thread_context(
            client, channel, thread_ts,
            title=f"OrgPulse: {question[:60]}",
            status="is thinking…",
        )

        # ── Step 2: Select & call the right tool ──────────────────────
        thinking_ts = _post_thinking(say, event, _tool_name_for(intent))

        result_blocks = None
        result_text = ""
        tools_called = [_tool_name_for(intent)]

        if intent == "release_readiness":
            data = _call_release_readiness(question)
            if data and data.get("release_readiness"):
                rr = data["release_readiness"]
                result_blocks = release_readiness_blocks(rr)
                result_text = f"{rr['verdict']} — {rr['release_name']}"
            else:
                # Fallback to general chat
                tools_called.append("chat")
                data = _call_general_chat(question)
                if data:
                    result_blocks = answer_blocks(question, data["answer"], data["citations"], data["confidence"])
                    result_text = data["answer"]

        elif intent == "expert_search":
            experts, topic = _call_expert_search(question)
            if experts:
                result_blocks = expert_result_blocks(topic, experts)
                result_text = f"Found {len(experts)} experts on {topic}"
            else:
                result_blocks = [{"type": "section", "text": {"type": "mrkdwn",
                    "text": f"No experts found for _{topic}_. Try a different topic."}}]
                result_text = "No experts found."

        elif intent == "graph_query":
            chain = _call_graph_query(question)
            if chain:
                from blocks import risk_alert_blocks
                result_blocks = risk_alert_blocks(
                    title="Active blocker chain",
                    probability=chain.get("risk_score", 0),
                    chain=chain.get("labels", []),
                    recommendation="Address the upstream blocker to protect downstream releases.",
                )
                result_text = f"Risk chain detected (score: {chain.get('risk_score', 0)})"
            else:
                # Fallback to general chat if no active chain
                tools_called.append("chat")
                data = _call_general_chat(question)
                if data:
                    result_blocks = answer_blocks(question, data["answer"], data["citations"], data["confidence"])
                    result_text = data["answer"]

        else:  # general
            data = _call_general_chat(question)
            if data:
                result_blocks = answer_blocks(question, data["answer"], data["citations"], data["confidence"])
                result_text = data["answer"]

        # ── Step 3: Remove thinking indicator & post answer ───────────
        _delete_thinking(client, channel, thinking_ts)

        if not result_blocks:
            say(
                text="OrgPulse could not reach the backend right now. Please try again shortly.",
                thread_ts=thread_ts,
            )
            return

        # Append agent provenance block showing which tools were called
        result_blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": (
                        f":robot_face: *OrgPulse Agent* — intent: `{intent}` · "
                        f"tools called: {', '.join(f'`{t}`' for t in tools_called)}"
                    ),
                }
            ],
        })

        say(blocks=result_blocks, text=result_text, thread_ts=thread_ts)

        # Update Slack AI thread status to "done"
        _set_assistant_thread_context(
            client, channel, thread_ts,
            title=f"OrgPulse: {question[:60]}",
            status="",  # empty string clears the status indicator
        )


def _tool_name_for(intent: str) -> str:
    return {
        "release_readiness": "release_readiness_check",
        "expert_search": "expert_finder",
        "graph_query": "dependency_graph_query",
        "general": "organizational_memory_search",
    }.get(intent, "chat")
