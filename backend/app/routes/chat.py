from typing import TYPE_CHECKING, Optional, Any, List
import logging

# --- TYPE_CHECKING: Stub patterns for linter resolution ---
if TYPE_CHECKING:
    # FastAPI/Pydantic stubs for IDE
    class APIRouter:
        def post(self, path: str, **kwargs: Any) -> Any: ...
    class BaseModel: ...
    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: Any = None): ...
    
    def invoke_model(prompt: str, system_prompt: Optional[str] = None) -> str: ...
    def generate_socratic_prompt(user_input: str) -> str: ...
else:
    from fastapi import APIRouter, HTTPException
    from pydantic import BaseModel
    from app.services.bedrock_client import invoke_model
    from app.services.socratic_service import generate_socratic_prompt

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/")
def chat_endpoint(payload: ChatRequest):
    """
    Main Socratic chat endpoint.
    Transforms user input into a guided learning prompt.
    """
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    msg_preview: str = "".join([c for i, c in enumerate(payload.message) if i < 50])
    logger.info(f"Received chat message: {msg_preview}...")
    
    try:
        # 1. Generate Socratic prompt
        socratic_prompt = generate_socratic_prompt(payload.message)
        
        # 2. Call AWS Bedrock with the new prompt
        ai_response = invoke_model(socratic_prompt)
        
        # 3. Check for service failure response
        if "temporarily unavailable" in ai_response:
             raise HTTPException(status_code=503, detail="AI Service is currently unavailable")
             
        return {"response": ai_response}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during chat")

