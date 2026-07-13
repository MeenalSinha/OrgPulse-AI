from fastapi import APIRouter, Query

from app.services.data_loader import store
from app.services.rag_service import find_experts

router = APIRouter(prefix="/api/experts", tags=["experts"])


@router.get("")
def list_top_experts(limit: int = 20):
    ranked = sorted(store.employees, key=lambda e: e["contribution_score"], reverse=True)
    return ranked[:limit]


@router.get("/search")
def search_experts(topic: str = Query(..., min_length=1, max_length=200)):
    return find_experts(topic)
