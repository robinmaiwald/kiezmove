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

from backend.app.database import SessionLocal
from backend.app.database_models import UserDB
from backend.app.models import UserTask
from backend.app.models import User, Task, UserTask
from backend.app.services.eligibility import (
    load_tasks,
    get_applicable_tasks,
)
from backend.app.services.user_tasks import (
    create_user_tasks,
    get_user_tasks,
)

app = FastAPI(
    title="KiezMove API",
    description="AI-powered Berlin moving concierge",
    version="0.1.0",
)


def get_db():
    db = SessionLocal()

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
def create_user(
    user: User,
    db: Session = Depends(get_db),
):
    db_user = UserDB(
        name=user.name,
        address=user.address,
        household_size=user.household_size,
        move_in_date=user.move_in_date,
        new_to_berlin=user.new_to_berlin,
        has_wohnungsgeberbestaetigung=user.has_wohnungsgeberbestaetigung,
        has_children=user.has_children,
        children_count=user.children_count,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

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
    user = db.get(UserDB, user_id)

    if user is None:
        return {"error": "User not found"}

    return {
        "id": user.id,
        "name": user.name,
        "address": user.address,
        "household_size": user.household_size,
        "move_in_date": user.move_in_date,
        "new_to_berlin": user.new_to_berlin,
        "has_wohnungsgeberbestaetigung": user.has_wohnungsgeberbestaetigung,
        "has_children": user.has_children,
        "children_count": user.children_count,
    }

@app.post("/users/{user_id}/tasks", response_model=list[UserTask])
def create_user_task_plan(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.get(UserDB, user_id)

    if user is None:
        return {"error": "User not found"}

    user_data = {
        "new_to_berlin": user.new_to_berlin,
        "moving_to_new_address": True,
    }

    applicable_tasks = get_applicable_tasks(user_data)

    create_user_tasks(
        db,
        user_id,
        applicable_tasks,
    )

    user_tasks = get_user_tasks(
        db,
        user_id,
    )

    return [
        UserTask(
            user_id=str(user_task.user_id),
            task_id=user_task.task_id,
            status=user_task.status,
            completed_at=(
                user_task.completed_at.isoformat()
                if user_task.completed_at
                else None
            ),
        )
        for user_task in user_tasks
    ]


@app.get("/users/{user_id}/tasks", response_model=list[UserTask])
def get_user_task_plan(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.get(UserDB, user_id)

    if user is None:
        return {"error": "User not found"}

    user_tasks = get_user_tasks(
        db,
        user_id,
    )

    return [
        UserTask(
            user_id=str(user_task.user_id),
            task_id=user_task.task_id,
            status=user_task.status,
            completed_at=(
                user_task.completed_at.isoformat()
                if user_task.completed_at
                else None
            ),
        )
        for user_task in user_tasks
    ]