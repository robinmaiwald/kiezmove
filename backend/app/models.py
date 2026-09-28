"""
Pydantic models used by the KiezMove API.

These models describe the data that enters and leaves the API.
FastAPI uses them to validate incoming requests and structure
responses.

Important:
These are NOT the database models.

Database models live in database_models.py.
"""


from pydantic import BaseModel


# Represents a user's moving situation as handled by the API.
# This is used when receiving user information from the frontend,
# n8n, or another API client.
class User(BaseModel):
    name: str
    address: str
    household_size: int

    move_in_date: str | None = None

    new_to_berlin: bool = False
    has_wohnungsgeberbestaetigung: bool = False

    has_children: bool = False
    children_count: int = 0


# Represents a reusable KiezMove task.
# Tasks describe things a person may need to do when moving.
class Task(BaseModel):
    id: str
    title: str
    description: str
    priority: str

    documents: list[str] = []
    source: str


# Represents a task assigned to a specific user.
# The status tracks whether the user has completed the task.
class UserTask(BaseModel):
    user_id: str
    task_id: str

    status: str = "pending"

    completed_at: str | None = None