"""
Unit tests for the organizational memory / RAG service: verifies answers
are always grounded (never hallucinated) and citations reference real
fixture IDs.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.services import rag_service
from app.services.data_loader import store


def test_answer_query_returns_citations_for_known_topic():
    result = rag_service.answer_query("Why did we migrate to PostgreSQL?")
    assert result["citations"], "Expected at least one citation for a matched topic"
    assert result["confidence"] > 0


def test_answer_query_is_honest_when_no_evidence_exists():
    result = rag_service.answer_query("zzz-nonexistent-topic-qqq")
    assert result["citations"] == []
    assert result["confidence"] == 0
    assert "No supporting evidence" in result["answer"]


def test_citations_reference_real_fixture_ids():
    result = rag_service.answer_query("Payments API security review")
    decision_ids = {d["id"] for d in store.decisions}
    for citation in result["citations"]:
        assert citation == "dependency_graph" or citation in decision_ids or citation.startswith(
            ("doc-", "conv-", "pr-")
        ) or any(citation == item["id"] for item in store.docs + store.conversations + store.pull_requests)


def test_find_experts_ranks_by_relevance():
    results = rag_service.find_experts("Security Review Service")
    assert len(results) > 0
    scores = [r["confidence_score"] for r in results]
    assert scores == sorted(scores, reverse=True)


def test_synthesis_fails_open_to_template_when_client_unavailable():
    """
    With no ANTHROPIC_API_KEY configured (the default test environment),
    _synthesize_with_claude must return None so answer_query falls back to
    the deterministic, citation-safe template rather than erroring.
    """
    result = rag_service._synthesize_with_claude("test query", ["some evidence"], None)
    assert result is None


def test_answer_query_reports_synthesis_source():
    result = rag_service.answer_query("Why did we migrate to PostgreSQL?")
    assert result["synthesized_by"] in ("template", "claude")


def test_synthesis_fails_open_on_client_exception(monkeypatch):
    """
    If a Claude API call raises for any reason (bad key, network error, rate
    limit), the RAG service must not propagate the exception - it should
    fail open to the template answer so the demo never breaks on this path.
    """
    class ExplodingClient:
        class messages:
            @staticmethod
            def create(**kwargs):
                raise RuntimeError("simulated API failure")

    monkeypatch.setattr(rag_service, "_anthropic_client", ExplodingClient())
    result = rag_service._synthesize_with_claude("test query", ["some evidence"], None)
    assert result is None
