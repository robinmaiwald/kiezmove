"""
API tests for KiezMove.

These tests verify that the FastAPI application exposes
the expected HTTP endpoints and returns valid responses.
"""

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200

    tasks = response.json()

    assert len(tasks) > 0
    assert "anmeldung" in [task["id"] for task in tasks]