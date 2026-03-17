# API route tests – placeholder
def test_health():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    response = client.get("/health/")
    assert response.status_code == 200
