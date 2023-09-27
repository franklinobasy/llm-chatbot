from fastapi.testclient import TestClient
from api import app


client = TestClient(app)


def test_read_root():
    response = client.get("/api/v1")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
