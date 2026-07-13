from fastapi import APIRouter

from app.services.data_loader import store
from app.services import graph_service, risk_engine

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary")
def get_summary():
    summary = dict(store.dashboard_summary)
    critical_chain = graph_service.critical_path()
    summary["critical_chain"] = critical_chain
    return summary


@router.get("/recent-decisions")
def recent_decisions(limit: int = 3):
    decisions = sorted(store.decisions, key=lambda d: d["date"], reverse=True)[:limit]
    return decisions


@router.get("/upcoming-deadlines")
def upcoming_deadlines(limit: int = 3):
    releases = [r for r in store.releases if r["status"] in ("At Risk", "On Track", "Delayed")]
    releases.sort(key=lambda r: r["date"])
    return releases[:limit]


@router.get("/ai-insights")
def ai_insights():
    return store.ai_insights


@router.get("/top-experts")
def top_experts(limit: int = 4):
    ranked = sorted(store.employees, key=lambda e: e["contribution_score"], reverse=True)[:limit]
    return ranked
