from fastapi import APIRouter
from pydantic import BaseModel
import logging
from app.services.bedrock_client import invoke_model
from app.services.socratic_service import generate_socratic_prompt

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/")
def chat_endpoint(payload: ChatRequest):
    logger.info(f"Received chat message: {payload.message}")
    
    # 1. Generate Socratic prompt
    socratic_prompt = generate_socratic_prompt(payload.message)
    
    # 2. Call AWS Bedrock with the new prompt
    ai_response = invoke_model(socratic_prompt)
    
    return {"response": ai_response}
