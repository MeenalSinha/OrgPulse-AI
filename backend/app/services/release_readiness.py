"""
Release readiness reasoning - the "Can we ship on Friday?" capability.

This is deliberately its own module rather than folded into rag_service so
the reasoning chain is explicit and independently testable: detect intent
-> resolve which release is being asked about -> pull the current critical
blocker chain -> compute delay probability -> recommend the person who can
actually unblock it -> synthesize a verdict.

Every field returned is derived from the same graph/risk primitives used
elsewhere (graph_service, risk_engine, rag_service.find_experts) - nothing
here is a scripted response, so it generalizes beyond the one demo release.
"""
import re
from typing import Dict, Optional

from app.services.data_loader import store
from app.services import graph_service, risk_engine
from app.services.rag_service import find_experts

INTENT_PATTERNS = [
    r"can we ship", r"can we release", r"ready to ship", r"ready to release",
    r"ship .* (by|on) ", r"release .* (by|on) ", r"will .* ship", r"will .* release",
]


def is_release_readiness_query(query: str) -> bool:
    ql = query.lower()
    return any(re.search(p, ql) for p in INTENT_PATTERNS)


def _resolve_target_release(query: str) -> Optional[Dict]:
    """
    Tries to match a specific release mentioned in the query. Falls back to
    whichever release the current critical blocker chain actually threatens
    (matched by shared tokens with the chain's terminal node), and if that
    also fails, falls back to the single highest-risk release org-wide -
    so this always resolves to something concrete rather than refusing.
    """
    ql = query.lower()
    tokens = set(re.findall(r"[a-zA-Z0-9]+", ql))

    for r in store.releases:
        release_tokens = set(re.findall(r"[a-zA-Z0-9]+", r["name"].lower()))
        if tokens & release_tokens - {"the", "a", "an", "we", "can", "ship", "release", "by", "on"}:
            return r

    chain = graph_service.critical_path()
    if chain:
        terminal_label = chain["labels"][-1].lower()
        for r in store.releases:
            if any(word in r["project"].lower() or word in r["name"].lower()
                   for word in terminal_label.split() if len(word) > 3):
                return r

    scored = [(r, risk_engine.release_delay_probability(r["id"])["probability"]) for r in store.releases]
    if not scored:
        return None
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0][0]


def answer_release_readiness(query: str) -> Dict:
    release = _resolve_target_release(query)
    if not release:
        return {
            "answer": "No release data is available to assess readiness against.",
            "citations": [],
            "confidence": 0,
            "synthesized_by": "none",
            "release_readiness": None,
        }

    risk = risk_engine.release_delay_probability(release["id"])
    chain = graph_service.critical_path()
    probability = risk["probability"]

    if probability >= 60:
        verdict = "No"
    elif probability >= 35:
        verdict = "At Risk"
    else:
        verdict = "Yes"

    # Recommend whoever can actually unblock the root cause - the upstream
    # end of the chain, not the release itself - since that's who needs to
    # act. Falls back to the release's own project name if there's no
    # active blocker chain to reason about.
    expert_topic = chain["labels"][0] if chain else release["project"]
    experts = find_experts(expert_topic)
    recommended_expert = experts[0]["employee"] if experts else None

    citations = ["dependency_graph"] if chain else []

    if verdict == "Yes":
        explanation = (
            f"{release['name']} has no active blocker chain and is currently {release['status']}. "
            f"Estimated delay probability: {probability}%."
        )
        recommendation = "No mitigation needed; continue normal release monitoring."
    else:
        chain_text = " -> ".join(chain["labels"]) if chain else "no graph-traced chain"
        explanation = (
            f"{release['name']} is blocked by a dependency chain: {chain_text}. "
            f"This chain has a graph-derived risk score of {chain['risk_score']}/100, giving an "
            f"estimated delay probability of {probability}%." if chain else
            f"{release['name']} is flagged {release['status']} with an estimated delay "
            f"probability of {probability}%, though no single blocker chain currently explains it."
        )
        recommendation = risk["recommendation"]

    answer_text = f"{verdict}."
    answer_text += f" {explanation} {recommendation}"
    if recommended_expert:
        answer_text += (
            f" {recommended_expert['name']} ({recommended_expert['role']}) is best positioned to help "
            f"unblock this, based on their history with {expert_topic}."
        )

    return {
        "answer": answer_text,
        "citations": citations,
        "confidence": min(97, 60 + (15 if chain else 0)),
        "synthesized_by": "template",
        "release_readiness": {
            "verdict": verdict,
            "release_name": release["name"],
            "release_status": release["status"],
            "probability": probability,
            "chain": chain["labels"] if chain else [],
            "risk_score": chain["risk_score"] if chain else 0,
            "explanation": explanation,
            "recommendation": recommendation,
            "recommended_expert": {
                "name": recommended_expert["name"],
                "role": recommended_expert["role"],
                "team_name": recommended_expert["team_name"],
                "confidence_score": experts[0]["confidence_score"],
            } if recommended_expert else None,
        },
    }
