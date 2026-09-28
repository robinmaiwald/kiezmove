"""
SQLAlchemy database models for KiezMove.

This module defines the structure of the data stored in SQLite.

These classes represent database tables:
- UserDB       -> users
- TaskDB       -> tasks
- UserTaskDB   -> user_tasks

These are database models, not API request/response models.
API models are defined separately in models.py.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database import Base


class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    household_size: Mapped[int] = mapped_column(Integer)

    move_in_date: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    new_to_berlin: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )


    has_wohnungsgeberbestaetigung: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    has_children: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    children_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )


class TaskDB(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True
    )

    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    priority: Mapped[str] = mapped_column(String)
    source: Mapped[str] = mapped_column(String)


class UserTaskDB(Base):
    __tablename__ = "user_tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    task_id: Mapped[str] = mapped_column(
        ForeignKey("tasks.id")
    )

    status: Mapped[str] = mapped_column(
        String,
        default="pending"
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )