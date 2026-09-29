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