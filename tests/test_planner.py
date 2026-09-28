"""
Tests for the KiezMove task planner.

These tests verify that tasks are ordered correctly
and that the planner can identify the next incomplete task.
"""

from backend.app.services.planner import (
    create_plan,
    get_next_task,
)


def test_create_plan_orders_tasks_by_priority():
    """
    Higher-priority tasks should appear before lower-priority tasks.
    """

    tasks = [
        {"id": "internet", "priority": "medium"},
        {"id": "anmeldung", "priority": "high"},
        {"id": "address_updates", "priority": "low"},
    ]

    plan = create_plan(tasks)

    task_ids = [task["id"] for task in plan]

    assert task_ids == [
        "anmeldung",
        "internet",
        "address_updates",
    ]


def test_get_next_task_returns_first_incomplete_task():
    """
    The planner should return the first task that has not
    already been completed.
    """

    tasks = [
        {"id": "anmeldung", "priority": "high"},
        {"id": "internet", "priority": "medium"},
        {"id": "address_updates", "priority": "low"},
    ]

    completed_task_ids = ["anmeldung"]

    next_task = get_next_task(
        tasks,
        completed_task_ids,
    )

    assert next_task["id"] == "internet"


def test_get_next_task_returns_none_when_all_tasks_are_complete():
    """
    When every task is completed, there should be no next task.
    """

    tasks = [
        {"id": "anmeldung", "priority": "high"},
        {"id": "internet", "priority": "medium"},
    ]

    completed_task_ids = [
        "anmeldung",
        "internet",
    ]

    next_task = get_next_task(
        tasks,
        completed_task_ids,
    )

    assert next_task is None