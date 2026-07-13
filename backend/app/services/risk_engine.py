"""
Predictive Risk Engine.

Combines dependency-graph risk (blocker chains, downstream impact) with
release metadata to produce a delay-probability estimate. This is a
transparent heuristic model in the prototype; docs/ARCHITECTURE.md describes
how it would be replaced with a trained model over historical release/ticket
data in a production system.
"""
from typing import Dict, List

from app.services.data_loader import store
from app.services import graph_service


def release_delay_probability(release_id: str) -> Dict:
    release = next((r for r in store.releases if r["id"] == release_id), None)
    if not release:
        return {"error": "release not found"}

    chain = graph_service.critical_path()
    base = {"Shipped": 5, "On Track": 20, "At Risk": 65, "Delayed": 85}.get(release["status"], 30)
    graph_penalty = chain["risk_score"] // 3 if chain else 0
    probability = min(97, base + graph_penalty)

    return {
        "release_id": release_id,
        "release_name": release["name"],
        "probability": probability,
        "status": release["status"],
        "contributing_chain": chain["labels"] if chain else [],
        "recommendation": (
            "Fast-track the upstream blocker or descope dependent work for this release."
            if probability >= 60 else
            "No immediate action required; continue monitoring dependency health."
        ),
    }


def org_wide_risk_summary() -> List[Dict]:
    return store.risks


def top_bottlenecks() -> List[Dict]:
    """Rank dependency graph nodes by computed risk score, highest first."""
    nodes = store.dependency_graph["nodes"]
    scored = [
        {**n, "risk_score": graph_service.risk_score_for_node(n["id"])}
        for n in nodes
    ]
    scored.sort(key=lambda n: n["risk_score"], reverse=True)
    return scored
