from typing import TYPE_CHECKING, Any, Dict
import logging

# --- TYPE_CHECKING: Stub patterns for linter resolution ---
if TYPE_CHECKING:
    # FastAPI/Pydantic stubs for IDE
    class APIRouter:
        def post(self, path: str, **kwargs: Any) -> Any: ...
    class BaseModel: ...
    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: Any = None): ...

    def generate_quiz(topic: str) -> Dict[str, Any]: ...
else:
    from fastapi import APIRouter, HTTPException
    from pydantic import BaseModel
    from app.services.quiz_service import generate_quiz

logger = logging.getLogger(__name__)

router = APIRouter()


class QuizRequest(BaseModel):
    topic: str


@router.post("/")
def quiz_endpoint(payload: QuizRequest):
    logger.info(f"Quiz request received for topic: {payload.topic}")

    try:
        quiz = generate_quiz(payload.topic)
    except ValueError as e:
        logger.error(f"Quiz generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except RuntimeError as e:
        logger.error(f"Bedrock invocation error: {e}")
        raise HTTPException(status_code=503, detail=str(e))

    return quiz
