from fastapi import APIRouter

from app.services import risk_engine

router = APIRouter(prefix="/api/risks", tags=["risks"])


@router.get("")
def list_risks():
    return risk_engine.org_wide_risk_summary()


@router.get("/bottlenecks")
def bottlenecks():
    return risk_engine.top_bottlenecks()
