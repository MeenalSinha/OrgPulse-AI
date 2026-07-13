"""
Unit tests for the dependency graph reasoning core: this is the logic that
turns raw graph edges into blocker chains, impact radius, and risk scores,
so it is covered directly rather than only through the API layer.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.services import graph_service


def test_blocker_chain_includes_known_demo_chain():
    chains = graph_service.find_blocker_chains()
    flattened = [c["labels"] for c in chains]
    assert any(
        "Security Review" in labels and "Mobile App" in labels
        for labels in flattened
    ), "Expected the scripted demo blocker chain (Security Review -> ... -> Mobile App)"


def test_critical_path_returns_highest_risk_chain():
    chain = graph_service.critical_path()
    assert chain is not None
    assert chain["risk_score"] > 0
    assert len(chain["chain"]) >= 2


def test_downstream_impact_is_transitive():
    downstream = graph_service.downstream_impact("security-review")
    ids = {n["id"] for n in downstream}
    assert "payments-api" in ids
    assert "backend-core" in ids
    assert "mobile-app" in ids


def test_upstream_dependencies_for_leaf_node():
    upstream = graph_service.upstream_dependencies("mobile-app")
    ids = {n["id"] for n in upstream}
    assert "payments-api" in ids
    assert "security-review" in ids


def test_risk_score_bounded_between_0_and_99():
    for node in graph_service.store.dependency_graph["nodes"]:
        score = graph_service.risk_score_for_node(node["id"])
        assert 0 <= score <= 99
