"""
Eligibility and rule logic for KiezMove.

This module contains deterministic business rules used to
decide which moving-in tasks may apply to a user.

Keep domain rules here rather than putting them directly
inside FastAPI endpoints or n8n workflows.

The functions in this module currently work with user data
represented as dictionaries.
"""


import json
from pathlib import Path


# Location of the reusable task definitions used by the planner.
DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "tasks.json"


def load_tasks():
    """
    Load the reusable task definitions from tasks.json.
    """
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_applicable_tasks(user):
    """
    Determine which tasks apply to a user's moving situation.

    The current rules are deterministic:
    - New Berlin residents or people moving to a new address
      receive the Anmeldung task.
    - Basic move-in tasks are currently always included.
    """
    tasks = load_tasks()

    applicable = []

    # Anmeldung applies when the user is new to Berlin
    # or moving to a new address.
    if user.get("new_to_berlin") or user.get("moving_to_new_address"):
        applicable.append("anmeldung")

    # Basic move-in tasks currently included for all users.
    applicable.extend([
        "rundfunkbeitrag",
        "electricity",
        "internet",
        "address_updates"
    ])

    # Return the full task definitions matching the applicable IDs.
    return [
        task for task in tasks
        if task["id"] in applicable
    ]