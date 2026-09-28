"""
Database configuration for KiezMove.

This module is responsible for:
- Creating the SQLAlchemy database engine.
- Creating database sessions.
- Providing the shared SQLAlchemy Base class.

The rest of the backend uses these objects to communicate
with the SQLite database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Location and type of database used by KiezMove.
# The SQLite file is created in the project root.
DATABASE_URL = "sqlite:///./kiezmove.db"


# The engine manages the connection between SQLAlchemy and SQLite.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# SessionLocal is used to create database sessions.
# Each session represents a unit of work with the database.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class for all SQLAlchemy database models.
# Database models such as UserDB and TaskDB inherit from this class.
class Base(DeclarativeBase):
    pass