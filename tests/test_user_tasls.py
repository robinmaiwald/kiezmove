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