from fastapi import APIRouter
from pydantic import BaseModel
import logging
from app.services.bedrock_client import invoke_model

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/")
def chat_endpoint(payload: ChatRequest):
    logger.info(f"Received chat message: {payload.message}")
    
    # Call AWS Bedrock
    ai_response = invoke_model(payload.message)
    
    return {"response": ai_response}
