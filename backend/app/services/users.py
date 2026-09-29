"""
User persistence service for KiezMove.

This module manages database operations related to users.

It keeps user database logic out of the FastAPI route definitions.
"""

from sqlalchemy.orm import Session

from backend.app.database_models import UserDB
from backend.app.models import User


def create_user(
    db: Session,
    user: User,
):
    """
    Create a new user in the database.

    Returns:
        The newly created UserDB object.
    """

    db_user = UserDB(
        name=user.name,
        address=user.address,
        household_size=user.household_size,
        move_in_date=user.move_in_date,
        new_to_berlin=user.new_to_berlin,
        has_wohnungsgeberbestaetigung=(
            user.has_wohnungsgeberbestaetigung
        ),
        has_children=user.has_children,
        children_count=user.children_count,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_id(
    db: Session,
    user_id: int,
):
    """
    Retrieve a user by database ID.

    Returns:
        UserDB object, or None if the user does not exist.
    """

    return db.get(UserDB, user_id)


def serialize_user(user: UserDB):
    """
    Convert a database UserDB object into the API response format.
    """

    return {
        "id": user.id,
        "name": user.name,
        "address": user.address,
        "household_size": user.household_size,
        "move_in_date": user.move_in_date,
        "new_to_berlin": user.new_to_berlin,
        "has_wohnungsgeberbestaetigung": (
            user.has_wohnungsgeberbestaetigung
        ),
        "has_children": user.has_children,
        "children_count": user.children_count,
    }

