"""
Service for determining a user's next incomplete KiezMove task.
"""

from sqlalchemy.orm import Session

from backend.app.database_models import TaskDB, UserTaskDB
from backend.app.services.planner import create_plan, get_next_task


def get_next_user_task(
    db: Session,
    user_id: int,
):
    """
    Determine the next incomplete task for a user.

    Returns:
        A task dictionary, or None if all tasks are completed.
    """

    user_tasks = (
        db.query(UserTaskDB)
        .filter(UserTaskDB.user_id == user_id)
        .all()
    )

    if not user_tasks:
        return None

    task_ids = [user_task.task_id for user_task in user_tasks]

    tasks = (
        db.query(TaskDB)
        .filter(TaskDB.id.in_(task_ids))
        .all()
    )

    task_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "source": task.source,
        }
        for task in tasks
    ]

    completed_task_ids = [
        user_task.task_id
        for user_task in user_tasks
        if user_task.status == "completed"
    ]

    ordered_tasks = create_plan(task_data)

    return get_next_task(
        ordered_tasks,
        completed_task_ids,
    )