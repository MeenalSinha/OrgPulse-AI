from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.services.rag_service import answer_query
from app.services.data_loader import store

router = APIRouter(prefix="/api/chat", tags=["chat"])
limiter = Limiter(key_func=get_remote_address)


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="Natural language question")
    channel: str | None = Field(default=None, max_length=200)
    user: str | None = Field(default=None, max_length=200)


class ReleaseReadiness(BaseModel):
    verdict: str
    release_name: str
    release_status: str
    probability: int
    chain: list[str]
    risk_score: int
    explanation: str
    recommendation: str
    recommended_expert: dict | None = None


class ChatResponse(BaseModel):
    answer: str
    citations: list[str]
    confidence: int
    synthesized_by: str = "template"
    release_readiness: ReleaseReadiness | None = None


@router.post("", response_model=ChatResponse)
@limiter.limit("20/minute")
def chat(request: Request, body: ChatRequest):
    result = answer_query(body.query)
    return result


@router.get("/citation/{citation_id}")
def resolve_citation(citation_id: str):
    """Resolve a citation ID back to its source object for 'View evidence' links."""
    if citation_id == "dependency_graph":
        return {"type": "dependency_graph", "detail": "See Dependency Graph explorer"}
    for collection_name, id_field_matches in [
        ("decisions", lambda x: x["id"] == citation_id),
        ("docs", lambda x: x["id"] == citation_id),
        ("conversations", lambda x: x["id"] == citation_id),
        ("pull_requests", lambda x: x["id"] == citation_id),
        ("tickets", lambda x: x["id"] == citation_id),
    ]:
        collection = getattr(store, collection_name)
        match = next((item for item in collection if id_field_matches(item)), None)
        if match:
            return {"type": collection_name, "detail": match}
    return {"type": "unknown", "detail": None}
