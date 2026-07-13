from fastapi import APIRouter, HTTPException

from app.services.data_loader import store

router = APIRouter(prefix="/api/decisions", tags=["decisions"])


@router.get("")
def list_decisions(category: str | None = None):
    decisions = store.decisions
    if category:
        decisions = [d for d in decisions if d["category"].lower() == category.lower()]
    return sorted(decisions, key=lambda d: d["date"], reverse=True)


@router.get("/{decision_id}")
def get_decision(decision_id: str):
    decision = next((d for d in store.decisions if d["id"] == decision_id), None)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    participants = store.employees_by_ids(decision["participant_ids"])
    return {**decision, "participants": participants}
