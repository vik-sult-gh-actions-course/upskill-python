"""
Unit tests for the FastAPI application's health check endpoint.
"""

from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def test_main():
    """
    Test the /healthy endpoint to ensure it returns a 200 status and the expected JSON response.
    """
    response = client.get("/healthy")
    assert response.status_code == 200
    assert response.json() == {
        "status": "Healthy"
    }  # pylint: disable=missing-final-newline
