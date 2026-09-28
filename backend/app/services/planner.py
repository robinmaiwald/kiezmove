"""
Moving-in task planner for KiezMove.

This module turns a user's situation into an ordered list
of tasks they may need to complete after moving.

The planner currently uses deterministic rules and task data.
Later, AI agents and n8n can orchestrate this logic without
duplicating the underlying business rules.

The functions in this module currently work with task data
represented as dictionaries.
"""


def create_plan(tasks):
    """
    Order applicable tasks by priority.

    Tasks are sorted from highest to lowest priority:
    high -> medium -> low.

    Unknown priorities are placed at the end of the plan.
    """
    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2
    }

    return sorted(
        tasks,
        key=lambda task: priority_order.get(
            task["priority"],
            99
        )
    )


def get_next_task(tasks, completed_task_ids=None):
    """
    Return the first task that has not been completed.

    Args:
        tasks: Ordered list of task dictionaries.
        completed_task_ids: IDs of tasks already completed.

    Returns:
        The next incomplete task, or None when all tasks
        have been completed.
    """
    completed_task_ids = completed_task_ids or []

    # Find the first task that is not in the completed list.
    for task in tasks:
        if task["id"] not in completed_task_ids:
            return task

    # No incomplete tasks remain.
    return None