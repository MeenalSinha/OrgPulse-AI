from fastapi import APIRouter, Query

from app.services.data_loader import store

router = APIRouter(prefix="/api/knowledge-graph", tags=["knowledge-graph"])


@router.get("/graph")
def get_knowledge_graph():
    """
    Returns a lightweight entity-relationship graph suitable for
    React Flow / Cytoscape rendering: people, teams, decisions, docs,
    services connected by authored/owns/relates_to edges.
    """
    nodes = []
    edges = []

    for t in store.teams:
        nodes.append({"id": t["id"], "label": t["name"], "type": "team"})

    for d in store.decisions[:20]:
        nodes.append({"id": d["id"], "label": d["title"], "type": "decision"})
        for pid in d["participant_ids"][:3]:
            edges.append({"source": pid, "target": d["id"], "relation": "participated_in"})

    for doc in store.docs[:20]:
        nodes.append({"id": doc["id"], "label": doc["title"], "type": "doc"})

    for emp in store.employees[:40]:
        nodes.append({"id": emp["id"], "label": emp["name"], "type": "person", "team_id": emp["team_id"]})
        edges.append({"source": emp["team_id"], "target": emp["id"], "relation": "member_of"})

    return {"nodes": nodes, "edges": edges}


@router.get("/highlights")
def highlights():
    return store.dashboard_summary["knowledge_graph_highlights"]


@router.get("/search")
def search(q: str = Query(..., min_length=1, max_length=200)):
    from app.services.rag_service import retrieve_evidence
    return retrieve_evidence(q, top_k=10)
