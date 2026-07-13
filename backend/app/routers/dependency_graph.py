from fastapi import APIRouter, HTTPException

from app.services import graph_service

router = APIRouter(prefix="/api/dependency-graph", tags=["dependency-graph"])


@router.get("/graph")
def get_graph():
    return graph_service.get_graph_payload()


@router.get("/blocker-chains")
def blocker_chains():
    return graph_service.find_blocker_chains()


@router.get("/critical-path")
def critical_path():
    chain = graph_service.critical_path()
    if not chain:
        raise HTTPException(status_code=404, detail="No active blocker chains")
    return chain


@router.get("/impact/{node_id}")
def impact(node_id: str):
    downstream = graph_service.downstream_impact(node_id)
    upstream = graph_service.upstream_dependencies(node_id)
    return {
        "node_id": node_id,
        "downstream_impact": downstream,
        "upstream_dependencies": upstream,
        "risk_score": graph_service.risk_score_for_node(node_id),
    }
