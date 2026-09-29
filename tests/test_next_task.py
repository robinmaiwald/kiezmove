from backend.app.database_models import TaskDB, UserDB, UserTaskDB
from backend.app.services.next_task import get_next_user_task


def create_test_data(db):
    # Create the user that will own the test tasks.
    user = UserDB(
        name="Next Task Test",
        address="Test Address",
        household_size=1,
        new_to_berlin=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Create three tasks with different priorities.
    # These IDs are safe to reuse because every test gets
    # its own isolated test database.
    tasks = [
        TaskDB(
            id="next_test_high",
            title="High Task",
            description="High priority test task",
            priority="high",
            source="test",
        ),
        TaskDB(
            id="next_test_medium",
            title="Medium Task",
            description="Medium priority test task",
            priority="medium",
            source="test",
        ),
        TaskDB(
            id="next_test_low",
            title="Low Task",
            description="Low priority test task",
            priority="low",
            source="test",
        ),
    ]

    db.add_all(tasks)
    db.commit()

    # Associate all three tasks with the test user.
    # They initially start as pending so get_next_user_task()
    # can determine which one should be returned.
    user_tasks = [
        UserTaskDB(
            user_id=user.id,
            task_id="next_test_high",
            status="pending",
        ),
        UserTaskDB(
            user_id=user.id,
            task_id="next_test_medium",
            status="pending",
        ),
        UserTaskDB(
            user_id=user.id,
            task_id="next_test_low",
            status="pending",
        ),
    ]

    db.add_all(user_tasks)
    db.commit()

    return user


def test_next_task_returns_highest_priority_pending_task(db):
    # Arrange: create a user with high, medium, and low priority tasks.
    user = create_test_data(db)

    # Act: ask the service for the user's next task.
    next_task = get_next_user_task(
        db,
        user.id,
    )

    # Assert: the highest-priority pending task should be returned.
    assert next_task["id"] == "next_test_high"


def test_next_task_skips_completed_task(db):
    # Arrange: create the test user and tasks.
    user = create_test_data(db)

    # Mark the highest-priority task as completed.
    high_task = (
        db.query(UserTaskDB)
        .filter(
            UserTaskDB.user_id == user.id,
            UserTaskDB.task_id == "next_test_high",
        )
        .first()
    )

    high_task.status = "completed"
    db.commit()

    # Act: ask for the next available task.
    next_task = get_next_user_task(
        db,
        user.id,
    )

    # Assert: the completed high-priority task is skipped
    # and the medium-priority task is returned.
    assert next_task["id"] == "next_test_medium"


def test_next_task_returns_none_when_all_completed(db):
    # Arrange: create the test user and tasks.
    user = create_test_data(db)

    # Retrieve all tasks belonging to the test user.
    user_tasks = (
        db.query(UserTaskDB)
        .filter(UserTaskDB.user_id == user.id)
        .all()
    )

    # Mark every task as completed.
    for user_task in user_tasks:
        user_task.status = "completed"

    db.commit()

    # Act: ask for the user's next task.
    next_task = get_next_user_task(
        db,
        user.id,
    )

    # Assert: there are no pending tasks left.
    assert next_task is None