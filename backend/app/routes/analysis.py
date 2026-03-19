from typing import TYPE_CHECKING, Any, Dict
import logging

# --- TYPE_CHECKING: Stub patterns for linter resolution ---
if TYPE_CHECKING:
    # FastAPI stubs for IDE
    class APIRouter:
        def get(self, path: str, **kwargs: Any) -> Any: ...
        def post(self, path: str, **kwargs: Any) -> Any: ...
    
    class _AnalyticsService:
        def get_summary(self) -> Dict[str, Any]: ...
        def reset_analytics(self) -> None: ...
    analytics_service: _AnalyticsService = _AnalyticsService()
else:
    from fastapi import APIRouter
    from app.services import analytics_service

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
def get_analysis_summary():
    """
    Returns the real-time analytics summary for the student session.
    """
    logger.info("Fetching real-time analytics summary")
    summary = analytics_service.get_summary()
    return {
        **summary,
        "status": "success"
    }

@router.post("/reset")
def reset_analysis():
    """
    Resets the analytics session data.
    """
    analytics_service.reset_analytics()
    return {"status": "success", "message": "Analytics reset successfully"}

