from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
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
