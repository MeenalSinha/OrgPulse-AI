from fastapi import APIRouter, HTTPException

from app.services.data_loader import store
from app.services import graph_service

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("")
def list_projects():
    return store.projects


@router.get("/{project_id}")
def get_project(project_id: str):
    project = next((p for p in store.projects if p["id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    related_releases = [r for r in store.releases if r["project"] == project["name"]]
    related_tickets = [t for t in store.tickets if t["status"] != "Done"][:10]
    return {
        "project": project,
        "releases": related_releases,
        "open_tickets": related_tickets,
    }
