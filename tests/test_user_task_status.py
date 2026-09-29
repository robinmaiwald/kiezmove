"""
Tests for KiezMove user task status updates.
"""

from backend.app.database import SessionLocal
from backend.app.database_models import UserDB
from backend.app.services.user_tasks import create_user_tasks
from backend.app.services.user_task_status import (
    update_user_task_status,
)


def create_test_user(db):
    user = UserDB(
        name="Status Test User",
        address="Berlin",
        household_size=1,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def test_complete_user_task():
    db = SessionLocal()

    user = create_test_user(db)

    create_user_tasks(
        db,
        user.id,
        [{"id": "anmeldung"}],
    )

    updated_task = update_user_task_status(
        db,
        user.id,
        "anmeldung",
        "completed",
    )

    assert updated_task is not None
    assert updated_task.status == "completed"
    assert updated_task.completed_at is not None

    db.close()


def test_reopen_user_task():
    db = SessionLocal()

    user = create_test_user(db)

    create_user_tasks(
        db,
        user.id,
        [{"id": "internet"}],
    )

    update_user_task_status(
        db,
        user.id,
        "internet",
        "completed",
    )

    updated_task = update_user_task_status(
        db,
        user.id,
        "internet",
        "pending",
    )

    assert updated_task is not None
    assert updated_task.status == "pending"
    assert updated_task.completed_at is None

    db.close()

def test_invalid_task_status():
    db = SessionLocal()

    user = create_test_user(db)

    create_user_tasks(
        db,
        user.id,
        [{"id": "anmeldung"}],
    )

    try:
        update_user_task_status(
            db,
            user.id,
            "anmeldung",
            "banana",
        )
        assert False, "Expected ValueError"
    except ValueError:
        pass

    db.close()