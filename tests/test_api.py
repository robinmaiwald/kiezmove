"""
API tests for KiezMove.

These tests verify that the FastAPI application exposes
the expected HTTP endpoints and returns valid responses.
"""

from fastapi.testclient import TestClient

from backend.app.database import SessionLocal
from backend.app.database_models import (
    TaskDB,
    UserDB,
    UserTaskDB,
)
from backend.app.main import app


# Create a test client for sending HTTP requests
# directly to the FastAPI application.
client = TestClient(app)


def test_get_tasks():
    """
    Verify that the /tasks endpoint returns
    the available task definitions.
    """

    response = client.get("/tasks")

    # The endpoint should respond successfully.
    assert response.status_code == 200

    tasks = response.json()

    # The task list should not be empty.
    assert len(tasks) > 0

    # Anmeldung should be one of the available tasks.
    assert "anmeldung" in [
        task["id"]
        for task in tasks
    ]


def test_get_next_task():
    """
    Verify that the /users/{user_id}/next-task endpoint
    returns the user's first incomplete task.
    """

    # Open a database session for creating test data.
    db = SessionLocal()

    try:
        # Create a test user.
        user = UserDB(
            name="API Test User",
            address="Berlin",
            household_size=1,
            new_to_berlin=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # Create a task that will be assigned to the user.
        task = TaskDB(
            id="api_next_task_test",
            title="API Next Task",
            description="API test task",
            priority="high",
            source="test",
        )

        db.add(task)
        db.commit()

        # Connect the task to the test user.
        # The task starts as pending, so it should be returned
        # by the next-task endpoint.
        user_task = UserTaskDB(
            user_id=user.id,
            task_id=task.id,
            status="pending",
        )

        db.add(user_task)
        db.commit()

        # Request the user's next incomplete task.
        response = client.get(
            f"/users/{user.id}/next-task"
        )

        # The endpoint should respond successfully.
        assert response.status_code == 200

        data = response.json()

        # Verify that the expected task was returned.
        assert data["id"] == "api_next_task_test"
        assert data["title"] == "API Next Task"
        assert data["priority"] == "high"

    finally:
        # Always close the database session,
        # even if the test fails.
        db.close()
