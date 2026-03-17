from fastapi import APIRouter

router = APIRouter()

# Quiz generation route
@router.post("/generate")
def generate_quiz(payload: dict):
    return {"message": "quiz route placeholder"}
