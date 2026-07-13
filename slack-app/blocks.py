"""
Block Kit builders. Kept separate from event handlers so the same rich
formatting is reusable across @mentions, slash commands, and proactive
alerts (daily digest, dependency warnings, release readiness, etc).
"""


def answer_blocks(question: str, answer: str, citations: list, confidence: int):
    blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Question:* {question}"},
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": answer},
        },
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": f"Confidence: {confidence}%"},
                {"type": "mrkdwn", "text": f"Sources: {len(citations)}"},
            ],
        },
    ]
    if citations:
        citation_text = "\n".join(f"- `{c}`" for c in citations)
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Evidence:*\n{citation_text}"},
        })
    blocks.append({
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "Open in OrgPulse"},
                "action_id": "open_orgpulse_dashboard",
                "url": "https://app.orgpulse.example.com/ai-chat",
            }
        ],
    })
    return blocks


def risk_alert_blocks(title: str, probability: int, chain: list, recommendation: str):
    chain_text = " -> ".join(chain) if chain else "No active blocker chain"
    return [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Risk Alert: {title}*"},
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Delay probability:*\n{probability}%"},
                {"type": "mrkdwn", "text": f"*Blocker chain:*\n{chain_text}"},
            ],
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Recommendation:*\n{recommendation}"},
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "View Dependency Graph"},
                    "action_id": "view_dependency_graph",
                    "url": "https://app.orgpulse.example.com/dependency-graph",
                }
            ],
        },
    ]


def daily_digest_blocks(summary: dict):
    return [
        {"type": "header", "text": {"type": "plain_text", "text": "OrgPulse Daily Intelligence Digest"}},
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Org Health Score:*\n{summary['org_health_score']}/100"},
                {"type": "mrkdwn", "text": f"*At-Risk Projects:*\n{summary['at_risk_projects']}"},
                {"type": "mrkdwn", "text": f"*Blocked Tasks:*\n{summary['blocked_tasks']}"},
                {"type": "mrkdwn", "text": f"*Team Velocity:*\n{summary['team_velocity']}%"},
            ],
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Ask `@OrgPulse` any question about your organization, "
                                                "or run `/orgpulse status` for a live snapshot."},
        },
    ]


def release_readiness_blocks(rr: dict):
    """
    The Slack rendering of the 'Can we ship on Friday?' wow moment: a blunt
    verdict, the causal chain, why, mitigation, and who can unblock it -
    all in one thread-friendly message.
    """
    verdict_emoji = {"No": ":no_entry:", "At Risk": ":warning:", "Yes": ":white_check_mark:"}.get(rr["verdict"], "")
    chain_text = " -> ".join(rr["chain"]) if rr["chain"] else "No active blocker chain"

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"{rr['verdict']} - {rr['release_name']}"},
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Delay probability:*\n{rr['probability']}%"},
                {"type": "mrkdwn", "text": f"*Status:*\n{rr['release_status']}"},
            ],
        },
        {"type": "divider"},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*Blocker chain:*\n{chain_text}"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*Why:*\n{rr['explanation']}"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*Mitigation:*\n{rr['recommendation']}"}},
    ]

    expert = rr.get("recommended_expert")
    if expert:
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Recommended expert:*\n{expert['name']} - {expert['role']}, {expert['team_name']}"},
        })

    blocks.append({
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "View Dependency Graph"},
                "action_id": "view_dependency_graph",
                "url": "https://app.orgpulse.example.com/dependency-graph",
            }
        ],
    })
    return blocks


def expert_result_blocks(topic: str, experts: list):
    lines = []
    for e in experts[:5]:
        emp = e["employee"]
        lines.append(f"*{emp['name']}* - {emp['role']} ({emp['team_name']}) "
                      f"- confidence {e['confidence_score']}%")
    body = "\n".join(lines) if lines else "No strong matches found."
    return [
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*Experts on {topic}:*\n{body}"}},
    ]
