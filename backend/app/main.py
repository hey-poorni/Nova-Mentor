from fastapi import FastAPI
from app.routes import chat, quiz, analysis, health

app = FastAPI(title="NovaMentor API", version="1.0.0")

app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
