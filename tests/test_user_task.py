"""
Tests for KiezMove user task persistence.

These tests verify that applicable tasks can be assigned
to a user and that duplicate assignments are prevented.
"""

from backend.app.database import SessionLocal
from backend.app.database_models import UserDB
from backend.app.services.user_tasks import (
    create_user_tasks,
    get_user_tasks,
)


def test_create_user_tasks():
    db = SessionLocal()

    user = UserDB(
        name="Task Test User",
        address="Berlin",
        household_size=1,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    tasks = [
        {"id": "anmeldung"},
        {"id": "internet"},
    ]

    create_user_tasks(
        db,
        user.id,
        tasks,
    )

    user_tasks = get_user_tasks(
        db,
        user.id,
    )

    assert len(user_tasks) == 2

    task_ids = [task.task_id for task in user_tasks]

    assert "anmeldung" in task_ids
    assert "internet" in task_ids

    db.close()


def test_duplicate_user_tasks_are_not_created():
    db = SessionLocal()

    user = UserDB(
        name="Duplicate Test User",
        address="Berlin",
        household_size=1,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    tasks = [
        {"id": "anmeldung"},
    ]

    create_user_tasks(
        db,
        user.id,
        tasks,
    )

    create_user_tasks(
        db,
        user.id,
        tasks,
    )

    user_tasks = get_user_tasks(
        db,
        user.id,
    )

    assert len(user_tasks) == 1

    db.close()


def test_create_user_tasks_creates_tasks(db):
    """
    Create UserTask records for the supplied tasks.

    The same task should not be created twice for the same user.
    """

    # Create a test user.
    user = UserDB(
        name="Task Test User",
        address="Berlin",
        household_size=1,
        new_to_berlin=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    tasks = [
        {
            "id": "test_anmeldung",
            "title": "Anmeldung",
            "description": "Register your new address.",
            "priority": "high",
            "source": "test",
        },
        {
            "id": "test_internet",
            "title": "Internet",
            "description": "Set up internet.",
            "priority": "medium",
            "source": "test",
        },
    ]

    # Create the user's tasks.
    created_tasks = create_user_tasks(
        db,
        user.id,
        tasks,
    )

    # Two tasks should have been created.
    assert len(created_tasks) == 2

    # Retrieve the persisted records.
    user_tasks = get_user_tasks(
        db,
        user.id,
    )

    assert len(user_tasks) == 2

    # All newly created tasks should be pending.
    assert all(
        user_task.status == "pending"
        for user_task in user_tasks
    )

    # Calling the service again should not create duplicates.
    created_again = create_user_tasks(
        db,
        user.id,
        tasks,
    )

    assert created_again == []

    user_tasks = get_user_tasks(
        db,
        user.id,
    )

    assert len(user_tasks) == 2

