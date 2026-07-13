from fastapi import APIRouter, HTTPException

from app.services.data_loader import store
from app.services import risk_engine

router = APIRouter(prefix="/api/releases", tags=["releases"])


@router.get("")
def list_releases():
    return store.releases


@router.get("/{release_id}/risk")
def release_risk(release_id: str):
    result = risk_engine.release_delay_probability(release_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
