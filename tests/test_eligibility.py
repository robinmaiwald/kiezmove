"""
Tests for KiezMove eligibility rules.

These tests verify that the eligibility service assigns
the correct tasks based on a user's moving situation.
"""

from backend.app.services.eligibility import get_applicable_tasks


def test_new_berlin_user_gets_anmeldung():

    #A person who is new to Berlin and moving to a new address
    #should receive the Anmeldung task.
  

    # Example user situation used by the eligibility rules.
    user = {
        "new_to_berlin": True,
        "moving_to_new_address": True
    }

    # Run the eligibility logic.
    tasks = get_applicable_tasks(user)

    # Extract task IDs so we can check whether Anmeldung
    # was included in the result.
    task_ids = [task["id"] for task in tasks]

    # Verify the expected business rule.
    assert "anmeldung" in task_ids


