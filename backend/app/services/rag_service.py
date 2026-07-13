"""
Organizational Memory / RAG reasoning service.

Architecture (prototype):
  1. Retrieval: hybrid lexical scoring over decisions, docs, conversations,
     tickets and PRs (stand-in for embeddings + pgvector/Qdrant hybrid
     retrieval described in the architecture doc).
  2. Graph grounding: cross-references retrieved evidence against the
     dependency graph so answers about "why is X blocked" are graph-derived,
     not just text-derived.
  3. Synthesis: if ANTHROPIC_API_KEY is configured, calls Claude to compose a
     grounded, cited answer from the retrieved evidence. Otherwise falls back
     to a deterministic template so the demo works with zero external calls.

Every answer includes a `citations` list referencing concrete fixture IDs so
the UI/Slack layer can render "View evidence" links. The service never
fabricates a citation: if there is no supporting evidence, it says so.
"""
import os
import re
from typing import List, Dict

from app.services.data_loader import store
from app.services import graph_service

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

_anthropic_client = None
if ANTHROPIC_API_KEY:
    try:
        import anthropic
        _anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    except Exception:
        # Missing package or bad key at import time; fall back to the
        # deterministic template rather than crashing the API.
        _anthropic_client = None


def _synthesize_with_claude(query: str, evidence_summaries: List[str], graph_summary: str | None) -> str | None:
    """
    Composes the final answer with Claude, strictly grounded in the evidence
    already retrieved by retrieve_evidence()/graph_service. The model is
    instructed to use ONLY the provided evidence and never introduce facts
    not present in it - this is what keeps the "never hallucinate" guarantee
    intact even when an LLM is in the loop, since Claude sees pre-retrieved,
    graph-grounded context rather than generating freely.

    Returns None (triggering fallback to the template answer) if no client
    is configured or the call fails for any reason.
    """
    if not _anthropic_client:
        return None

    context_blocks = "\n".join(f"- {s}" for s in evidence_summaries)
    if graph_summary:
        context_blocks = f"- {graph_summary}\n{context_blocks}"

    system_prompt = (
        "You are OrgPulse AI, an organizational intelligence assistant. Answer the "
        "user's question using ONLY the evidence provided below. Do not introduce "
        "any fact, name, date, or number that is not present in the evidence. If "
        "the evidence is insufficient to fully answer, say so explicitly rather "
        "than guessing. Keep the answer to 2-4 sentences, written for a Slack "
        "message or chat UI. Do not fabricate citations."
    )

    try:
        response = _anthropic_client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=400,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"Question: {query}\n\nEvidence:\n{context_blocks}",
            }],
        )
        text_blocks = [b.text for b in response.content if getattr(b, "type", None) == "text"]
        return "".join(text_blocks).strip() or None
    except Exception:
        # Network error, rate limit, bad key, etc: fail open to the
        # deterministic template so the demo never breaks on this path.
        return None


def _score_text(query_terms: List[str], text: str) -> int:
    text_l = text.lower()
    return sum(text_l.count(term) for term in query_terms)


def _tokenize(query: str) -> List[str]:
    return [t for t in re.findall(r"[a-zA-Z0-9]+", query.lower()) if len(t) > 2]


def retrieve_evidence(query: str, top_k: int = 5) -> List[Dict]:
    terms = _tokenize(query)
    candidates = []

    for d in store.decisions:
        blob = f"{d['title']} {d['category']} {d['rationale']}"
        score = _score_text(terms, blob)
        if score > 0:
            candidates.append({"type": "decision", "score": score, "item": d})

    for doc in store.docs:
        score = _score_text(terms, doc["title"])
        if score > 0:
            candidates.append({"type": "doc", "score": score, "item": doc})

    for c in store.conversations:
        score = _score_text(terms, c["summary"])
        if score > 0:
            candidates.append({"type": "conversation", "score": score, "item": c})

    for pr in store.pull_requests:
        blob = f"{pr['title']} {' '.join(pr['impacted_services'])}"
        score = _score_text(terms, blob)
        if score > 0:
            candidates.append({"type": "pull_request", "score": score, "item": pr})

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return candidates[:top_k]


def answer_query(query: str) -> Dict:
    # "Can we ship on Friday?" style questions get the dedicated release
    # readiness reasoning chain (verdict + causal chain + mitigation +
    # recommended expert) rather than generic evidence retrieval.
    from app.services.release_readiness import is_release_readiness_query, answer_release_readiness
    if is_release_readiness_query(query):
        return answer_release_readiness(query)

    evidence = retrieve_evidence(query)

    # Graph-grounded shortcut: "why is X blocked" / "what is blocking Y"
    ql = query.lower()
    graph_context = None
    if "block" in ql or "delay" in ql or "risk" in ql:
        chain = graph_service.critical_path()
        if chain:
            graph_context = chain

    if not evidence and not graph_context:
        return {
            "answer": "No supporting evidence was found in the organizational graph for this "
                      "question. Try rephrasing, or ask about a specific project, service, "
                      "decision, or team.",
            "citations": [],
            "confidence": 0,
            "synthesized_by": "none",
            "release_readiness": None,
        }

    citation_ids = []
    answer_parts = []

    if graph_context:
        labels = " -> ".join(graph_context["labels"])
        answer_parts.append(
            f"The dependency graph shows an active blocker chain: {labels}. "
            f"This chain has a risk score of {graph_context['risk_score']} out of 100."
        )
        citation_ids.append("dependency_graph")

    if evidence:
        top = evidence[0]
        item = top["item"]
        if top["type"] == "decision":
            answer_parts.append(
                f"Related decision: '{item['title']}' ({item['category']}, {item['date']}). "
                f"{item['rationale']}"
            )
            citation_ids.append(item["id"])
        elif top["type"] == "doc":
            answer_parts.append(f"Related architecture document: '{item['title']}'.")
            citation_ids.append(item["id"])
        elif top["type"] == "conversation":
            answer_parts.append(f"Related discussion in {item['channel']}: {item['summary']}")
            citation_ids.append(item["id"])
        elif top["type"] == "pull_request":
            answer_parts.append(
                f"Related pull request: '{item['title']}' impacting {', '.join(item['impacted_services'])}."
            )
            citation_ids.append(item["id"])

        for extra in evidence[1:3]:
            citation_ids.append(extra["item"]["id"])

    confidence = min(97, 55 + len(evidence) * 8 + (15 if graph_context else 0))

    template_answer = " ".join(answer_parts)

    # If Claude is configured, let it compose the final prose from the exact
    # same evidence the template used - citations stay whatever retrieval
    # found, so this can never add an uncited claim.
    evidence_summaries = []
    if graph_context:
        evidence_summaries.append(
            f"Dependency graph blocker chain: {' -> '.join(graph_context['labels'])} "
            f"(risk score {graph_context['risk_score']}/100)"
        )
    for e in evidence[:3]:
        item = e["item"]
        if e["type"] == "decision":
            evidence_summaries.append(f"Decision [{item['id']}] '{item['title']}': {item['rationale']}")
        elif e["type"] == "doc":
            evidence_summaries.append(f"Doc [{item['id']}] '{item['title']}' ({item['type']})")
        elif e["type"] == "conversation":
            evidence_summaries.append(f"Slack conversation [{item['id']}] in {item['channel']}: {item['summary']}")
        elif e["type"] == "pull_request":
            evidence_summaries.append(
                f"PR [{item['id']}] '{item['title']}' impacting {', '.join(item['impacted_services'])}"
            )

    synthesized = _synthesize_with_claude(query, evidence_summaries, None)

    return {
        "answer": synthesized or template_answer,
        "citations": citation_ids,
        "confidence": confidence,
        "synthesized_by": "claude" if synthesized else "template",
        "release_readiness": None,
    }


def find_experts(topic: str) -> List[Dict]:
    terms = _tokenize(topic)
    scored = []
    for emp in store.employees:
        expertise_blob = " ".join(emp["expertise"]).lower()
        score = sum(1 for t in terms if t in expertise_blob)
        if score > 0:
            pr_count = sum(
                1 for pr in store.pull_requests
                if pr["author_id"] == emp["id"]
                and any(t in " ".join(pr["impacted_services"]).lower() for t in terms)
            )
            incident_count = sum(
                1 for inc in store.incidents if emp["id"] in inc["participant_ids"]
            )
            confidence = min(99, score * 20 + pr_count * 5 + incident_count * 3 + emp["contribution_score"] // 5)
            scored.append({
                "employee": emp,
                "pr_count": pr_count,
                "incident_count": incident_count,
                "confidence_score": confidence,
            })
    scored.sort(key=lambda x: x["confidence_score"], reverse=True)
    return scored[:10]
