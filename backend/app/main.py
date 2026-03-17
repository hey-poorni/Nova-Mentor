import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# --- Routes ---

@app.get("/health", tags=["Health"])
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok"}

@app.post("/chat", tags=["Chat"])
def chat_endpoint():
    logger.info("Chat endpoint called")
    return {"message": "working"}
