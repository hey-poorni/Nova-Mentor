import logging
from typing import TYPE_CHECKING, Any

# ── TYPE_CHECKING stubs: IDE/linter resolution for path-with-spaces issue ────
if TYPE_CHECKING:
    class FastAPI:
        """Stub for fastapi.FastAPI."""
        def __init__(self, title: str = "", version: str = "") -> None: ...  # type: ignore[empty-body]
        def get(self, path: str, **kwargs: Any) -> Any: ...  # type: ignore[empty-body]
        def add_middleware(self, middleware_class: Any, **options: Any) -> None: ...  # type: ignore[empty-body]
        def include_router(self, router: Any, prefix: str = "", tags: Any = None) -> None: ...  # type: ignore[empty-body]

    class CORSMiddleware:
        """Stub for fastapi.middleware.cors.CORSMiddleware."""
        def __init__(self, **kwargs: Any) -> None: ...  # type: ignore[empty-body]

    class _RouterModule:
        """Stub for a routes module that exposes a .router attribute."""
        router: Any

    # Assign instances so linter sees these as bound with known types
    chat     = _RouterModule()
    health   = _RouterModule()
    quiz     = _RouterModule()
    analysis = _RouterModule()

else:
    # Real runtime imports
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from .routes import chat, health, quiz, analysis


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="NovaMentor API", version="1.0.0")

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Starting NovaMentor API...")


# --- Root Route ---
@app.get("/", tags=["Root"])
def root() -> dict:
    return {
        "app": "NovaMentor API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/chat (POST)",
            "docs": "/docs",
        },
    }


# --- Include Routers ---
app.include_router(health.router,   prefix="/health",   tags=["Health"])
app.include_router(chat.router,     prefix="/chat",     tags=["Chat"])
app.include_router(quiz.router,     prefix="/quiz",     tags=["Quiz"])
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
