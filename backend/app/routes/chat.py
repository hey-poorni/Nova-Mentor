from fastapi import APIRouter

router = APIRouter()

# Chat route – Socratic Q&A
@router.post("/")
def chat(payload: dict):
    return {"message": "chat route placeholder"}
