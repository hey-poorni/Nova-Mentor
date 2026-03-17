from fastapi import APIRouter

router = APIRouter()

# Analysis / analytics route
@router.get("/")
def get_analysis():
    return {"message": "analysis route placeholder"}
