from fastapi import APIRouter

from app.services.data_loader import store

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/velocity")
def velocity_by_team():
    return [
        {"team": t["name"], "health_score": t["health_score"], "member_count": t["member_count"]}
        for t in store.teams
    ]


@router.get("/pr-throughput")
def pr_throughput():
    from collections import Counter
    counts = Counter(pr["status"] for pr in store.pull_requests)
    return [{"status": k, "count": v} for k, v in counts.items()]


@router.get("/incident-trend")
def incident_trend():
    from collections import Counter
    counts = Counter(inc["severity"] for inc in store.incidents)
    return [{"severity": k, "count": v} for k, v in counts.items()]
