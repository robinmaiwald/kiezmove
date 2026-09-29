"""
User task status service for KiezMove.

This module handles changes to the status of a user's task.
"""

from datetime import datetime, UTC

from sqlalchemy.orm import Session

from backend.app.database_models import UserTaskDB


ALLOWED_STATUSES = {
    "pending",
    "completed",
}


def update_user_task_status(
    db: Session,
    user_id: int,
    task_id: str,
    status: str,
):
    """
    Update the status of a user's task.

    When a task becomes completed, completed_at is recorded.
    When a task becomes pending again, completed_at is cleared.

    Returns the updated UserTaskDB object, or None if the
    user-task relationship does not exist.
    """

    if status not in ALLOWED_STATUSES:
        raise ValueError("Invalid task status")

    user_task = (
        db.query(UserTaskDB)
        .filter(
            UserTaskDB.user_id == user_id,
            UserTaskDB.task_id == task_id,
        )
        .first()
    )

    if user_task is None:
        return None

    user_task.status = status

    if status == "completed":
        user_task.completed_at = datetime.now(UTC)
    else:
        user_task.completed_at = None

    db.commit()
    db.refresh(user_task)

    return user_task