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
from backend.app.models import User

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