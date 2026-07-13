from fastapi import APIRouter

from mcp_connectors.registry import CONNECTOR_REGISTRY

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


@router.get("")
def list_integrations():
    return [
        {
            "id": key,
            "name": connector.display_name,
            "category": connector.category,
            "status": connector.status(),
            "mode": connector.mode,
        }
        for key, connector in CONNECTOR_REGISTRY.items()
    ]


@router.post("/{connector_id}/sync")
def sync_connector(connector_id: str):
    connector = CONNECTOR_REGISTRY.get(connector_id)
    if not connector:
        return {"error": "unknown connector"}
    return connector.sync()
