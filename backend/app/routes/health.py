from typing import TYPE_CHECKING, Any
import logging

# --- TYPE_CHECKING: Stub patterns for linter resolution ---
if TYPE_CHECKING:
    # FastAPI stubs for IDE
    class APIRouter:
        def get(self, path: str, **kwargs: Any) -> Any: ...
    
    def get_bedrock_client() -> Any: ...
else:
    from fastapi import APIRouter
    from app.services.bedrock_client import get_bedrock_client

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
def health_check():
    # Explicitly use typed structure to avoid linter confusion
    infrastructure = {"bedrock": "unknown"}
    health = {
        "status": "ok",
        "service": "NovaMentor API",
        "infrastructure": infrastructure
    }
    
    try:
        # Just check if client can be initialized
        get_bedrock_client()
        infrastructure["bedrock"] = "connected"
    except Exception as e:
        logger.error(f"Health check failed for Bedrock: {e}")
        health["status"] = "degraded"
        infrastructure["bedrock"] = "failed"
        
    return health


