from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def test_main():
    response = client.get("/healthy")
    assert response.status_code == 200
    assert response.json() == {'status': 'Healthy'}