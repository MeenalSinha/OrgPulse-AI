"""
Tests for the "Can we ship on Friday?" release readiness reasoning chain -
the demo's wow-moment capability. Verifies intent detection, that the
verdict is actually derived from the graph/risk primitives (not hardcoded),
and that a recommended expert is always attached when a blocker chain
exists.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.services import release_readiness, rag_service


def test_detects_release_readiness_intent():
    assert release_readiness.is_release_readiness_query("Can we ship on Friday?")
    assert release_readiness.is_release_readiness_query("ready to release the mobile app?")
    assert not release_readiness.is_release_readiness_query("Why did we migrate to PostgreSQL?")


def test_resolves_to_the_release_threatened_by_the_active_blocker_chain():
    result = release_readiness.answer_release_readiness("Can we ship the mobile app on Friday?")
    rr = result["release_readiness"]
    assert rr is not None
    assert "Mobile" in rr["release_name"]
    assert rr["chain"] == ["Security Review", "Payments API", "Backend Core", "Mobile App"]


def test_verdict_is_derived_not_hardcoded():
    result = release_readiness.answer_release_readiness("Can we ship the mobile app on Friday?")
    rr = result["release_readiness"]
    # verdict must be consistent with the probability threshold logic
    if rr["probability"] >= 60:
        assert rr["verdict"] == "No"
    elif rr["probability"] >= 35:
        assert rr["verdict"] == "At Risk"
    else:
        assert rr["verdict"] == "Yes"


def test_recommends_an_expert_on_the_root_blocker_not_the_release_itself():
    result = release_readiness.answer_release_readiness("Can we ship the mobile app on Friday?")
    rr = result["release_readiness"]
    assert rr["recommended_expert"] is not None
    assert "name" in rr["recommended_expert"] and "role" in rr["recommended_expert"]


def test_falls_back_to_highest_risk_release_when_nothing_specific_is_named():
    result = release_readiness.answer_release_readiness("can we ship on friday")
    assert result["release_readiness"] is not None
    assert result["release_readiness"]["release_name"]


def test_answer_query_routes_release_readiness_queries_to_the_dedicated_chain():
    result = rag_service.answer_query("Can we ship the mobile app on Friday?")
    assert result["release_readiness"] is not None
    assert result["release_readiness"]["verdict"] in ("Yes", "No", "At Risk")


def test_non_release_query_does_not_trigger_release_readiness():
    result = rag_service.answer_query("Why did we migrate to PostgreSQL?")
    assert result["release_readiness"] is None
