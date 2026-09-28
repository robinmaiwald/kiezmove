"""
Initialize the KiezMove SQLite database.

This script creates all database tables defined by the
SQLAlchemy models.

It is mainly used during local development or when setting
up a fresh KiezMove environment.

It does not insert application data.
"""

from backend.app.database import Base, engine

# Import the database models so SQLAlchemy knows about
# all tables before create_all() is called.
from backend.app.database_models import (
    UserDB,
    TaskDB,
    UserTaskDB,
)


def init_database():
    # Create any tables that do not already exist.
    # Existing tables are left unchanged.
    Base.metadata.create_all(bind=engine)

    print("Database initialized.")


# Run database initialization when this file is executed directly.
if __name__ == "__main__":
    init_database()