"""
KiezMove FastAPI application.

This module exposes the HTTP API used by:
- the frontend,
- n8n workflows,
- and eventually KiezMove's AI agents.

The API is responsible for receiving validated requests
and passing work to the appropriate backend services.
"""


from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from backend.app import database
from backend.app.services.users import (
    create_user,
    get_user_by_id,
    serialize_user,
)
from backend.app.models import Task, User, UserTask, UserTaskUpdate
from backend.app.services.eligibility import load_tasks
from backend.app.services.next_task import get_next_user_task
from backend.app.services.user_task_status import update_user_task_status
from backend.app.services.user_tasks import (
    create_task_plan,
    get_user_tasks,
    serialize_user_task,
)

app = FastAPI(
    title="KiezMove API",
    description="AI-powered Berlin moving concierge",
    version="0.1.0",
)


def get_db():
    db = database.SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return load_tasks()


@app.post("/users")
def create_user_endpoint(
    user: User,
    db: Session = Depends(get_db),
):
    db_user = create_user(db, user)

    return {
        "id": db_user.id,
        "name": db_user.name,
        "address": db_user.address,
    }


@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, user_id)

    if user is None:
        return {"error": "User not found"}

    return serialize_user(user)

@app.post("/users/{user_id}/tasks", response_model=list[UserTask])
def create_user_task_plan(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, user_id)

    if user is None:
        return {"error": "User not found"}

    user_tasks = create_task_plan(
        db,
        user,
    )

    return [
        serialize_user_task(user_task)
        for user_task in user_tasks
    ]


@app.get("/users/{user_id}/tasks", response_model=list[UserTask])
def get_user_task_plan(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, user_id)

    if user is None:
        return {"error": "User not found"}

    user_tasks = get_user_tasks(
        db,
        user_id,
    )

    return [
        serialize_user_task(user_task)
        for user_task in user_tasks
    ]

@app.patch(
    "/users/{user_id}/tasks/{task_id}",
    response_model=UserTask,
)
def update_task_status(
    user_id: int,
    task_id: str,
    update: UserTaskUpdate,
    db: Session = Depends(get_db),
):
    user_task = update_user_task_status(
        db,
        user_id,
        task_id,
        update.status,
    )

    if user_task is None:
        return {"error": "User task not found"}

    return serialize_user_task(user_task)

@app.get("/users/{user_id}/next-task")
def get_next_task_for_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Return the next incomplete task for a user.

    Returns None when the user has no tasks
    or all of their tasks are completed.
    """

    user = get_user_by_id(db, user_id)

    if user is None:
        return {"error": "User not found"}

    next_task = get_next_user_task(
        db,
        user_id,
    )

    if next_task is None:
        return None

    return next_task