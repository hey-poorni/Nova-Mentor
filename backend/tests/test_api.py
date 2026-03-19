import sys
import os
from typing import TYPE_CHECKING, Any

# ─── Fix Path Resolution (Ensures app modules can be found despite space in path) ───
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ─── TYPE_CHECKING Guard ──────────────────────────────────────────────────
if TYPE_CHECKING:
    # Stubs for the IDE/linter to resolve types despite "Projects E" path spaces issue
    class FastAPI: ...
    class TestClient:
        def __init__(self, app: Any, **kwargs: Any) -> None: ...
        def get(self, url: str, **kwargs: Any) -> Any: ...
        def post(self, url: str, **kwargs: Any) -> Any: ...
    app: FastAPI = ... # type: ignore
else:
    # Real runtime imports
    from fastapi.testclient import TestClient
    from app.main import app

# Initialize test client
client = TestClient(app)

def test_health_endpoint() -> None:
    """Verify health check returns connectivity status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "infrastructure" in data

def test_root_endpoint() -> None:
    """Verify documentation links on root."""
    response = client.get("/")
    assert response.status_code == 200
    assert "endpoints" in response.json()

def test_analysis_summary() -> None:
    """Verify initial analytics state."""
    response = client.get("/analysis")
    assert response.status_code == 200
    data = response.json()
    assert data["total_attempts"] == 0
    assert data["accuracy"] == 0.0

def test_quiz_endpoint_invalid() -> None:
    """Verify bad request handling for empty quiz topic."""
    response = client.post("/quiz", json={})
    assert response.status_code == 422 # Marshalling error if topic missing

def test_chat_empty_message() -> None:
    """Verify validation for empty chat message."""
    response = client.post("/chat", json={"message": "   "})
    assert response.status_code == 400
