import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, health

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="NovaMentor API", version="1.0.0")

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Starting NovaMentor API...")

# --- Include Routers ---
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
