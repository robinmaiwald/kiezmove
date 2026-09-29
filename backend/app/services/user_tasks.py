"""
User task persistence service for KiezMove.

This module manages the relationship between users and
the reusable tasks stored in the database.

It is responsible for:
- Creating UserTask records for applicable tasks.
- Retrieving a user's task records.

The service keeps database operations out of the
FastAPI route definitions.
"""

from sqlalchemy.orm import Session

from backend.app.database_models import UserTaskDB
from backend.app.models import UserTask


def create_user_tasks(
    db: Session,
    user_id: int,
    tasks: list[dict],
):
    """
    Create pending UserTask records for a user's applicable tasks.

    Existing UserTask records are not duplicated.
    """

    created_tasks = []

    for task in tasks:
        existing = (
            db.query(UserTaskDB)
            .filter(
                UserTaskDB.user_id == user_id,
                UserTaskDB.task_id == task["id"],
            )
            .first()
        )

        if existing is not None:
            continue

        user_task = UserTaskDB(
            user_id=user_id,
            task_id=task["id"],
            status="pending",
        )

        db.add(user_task)
        created_tasks.append(user_task)

    db.commit()

    return created_tasks


def get_user_tasks(
    db: Session,
    user_id: int,
):
    """
    Return all UserTask records belonging to a user.
    """

    return (
        db.query(UserTaskDB)
        .filter(UserTaskDB.user_id == user_id)
        .all()
    )

def serialize_user_task(user_task):
    """
    Convert a database UserTask object into the API response format.
    """

    return {
        "user_id": str(user_task.user_id),
        "task_id": user_task.task_id,
        "status": user_task.status,
        "completed_at": (
            user_task.completed_at.isoformat()
            if user_task.completed_at
            else None
        ),
    }


def create_task_plan(
    db: Session,
    user,
):
    """
    Determine and create the applicable tasks for a user.

    Returns:
        All UserTask records belonging to the user.
    """

    from backend.app.services.eligibility import get_applicable_tasks

    user_data = {
        "new_to_berlin": user.new_to_berlin,
        "moving_to_new_address": True,
    }

    applicable_tasks = get_applicable_tasks(user_data)

    create_user_tasks(
        db,
        user.id,
        applicable_tasks,
    )

    return get_user_tasks(
        db,
        user.id,
    )