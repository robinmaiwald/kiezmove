"""
Manual database smoke test for KiezMove.

This script creates one example user, saves the user to SQLite,
and prints the generated database ID.

It is intended for local development only.
Automated tests belong in the tests/ directory.

Note:
Running this script inserts a real test user into the local
kiezmove.db database.
"""

from backend.app.database import SessionLocal
from backend.app.database_models import UserDB


def main():
    # Open a database session for this test.
    db = SessionLocal()

    # Create a Python database-model object.
    # The user is not stored in SQLite until db.commit() is called.
    user = UserDB(
        name="Alex",
        address="Karl-Marx-Straße 123, 12043 Berlin",
        household_size=1,
        move_in_date="2026-10-01",
        new_to_berlin=True,
        has_wohnungsgeberbestaetigung=True,
        has_children=False,
        children_count=0,
    )

    # Add the user to the current database transaction.
    db.add(user)

    # Persist the transaction to SQLite.
    db.commit()

    # Reload the object so generated values, such as the ID,
    # are available on the Python object.
    db.refresh(user)

    print(f"Created user: {user.id} - {user.name}")

    # Close the database session when the test is finished.
    db.close()


# Run the smoke test when this file is executed directly.
if __name__ == "__main__":
    main()