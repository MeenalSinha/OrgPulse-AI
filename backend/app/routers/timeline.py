from fastapi import APIRouter

from app.services.data_loader import store

router = APIRouter(prefix="/api/timeline", tags=["timeline"])


@router.get("")
def organizational_timeline():
    events = []
    for d in store.decisions:
        events.append({"date": d["date"], "type": "decision", "title": d["title"], "id": d["id"]})
    for r in store.releases:
        events.append({"date": r["date"], "type": "release", "title": r["name"], "id": r["id"]})
    for i in store.incidents:
        events.append({"date": i["date"], "type": "incident", "title": i["title"], "id": i["id"]})
    events.sort(key=lambda e: e["date"], reverse=True)
    return events[:80]
