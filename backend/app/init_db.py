"""
Initialize the KiezMove SQLite database.

This script:
- Creates all SQLAlchemy database tables.
- Loads reusable task definitions from tasks.json.
- Inserts missing tasks into the tasks table.

It is safe to run multiple times because existing
tasks are not inserted again.
"""

import json
from pathlib import Path

from backend.app.database import Base, SessionLocal, engine
from backend.app.database_models import (
    UserDB,
    TaskDB,
    UserTaskDB,
)


DATA_PATH = (
    Path(__file__).resolve().parents[2]
    / "backend"
    / "data"
    / "tasks.json"
)


def load_task_data():
    """Load reusable task definitions from tasks.json."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_tasks():
    """Insert tasks from tasks.json that do not already exist."""
    db = SessionLocal()

    try:
        tasks = load_task_data()

        for task in tasks:
            existing_task = db.get(TaskDB, task["id"])

            if existing_task is None:
                db.add(
                    TaskDB(
                        id=task["id"],
                        title=task["title"],
                        description=task["description"],
                        priority=task["priority"],
                        source=task["source"],
                    )
                )

        db.commit()

    finally:
        db.close()


def init_database():
    """Create database tables and seed reusable tasks."""
    Base.metadata.create_all(bind=engine)
    seed_tasks()

    print("Database initialized.")


if __name__ == "__main__":
    init_database()