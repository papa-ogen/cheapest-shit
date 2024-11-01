from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_products() -> None:
    response = client.get("/search/?query=skridskor")
    assert response.status_code == 200
