
"""
Shared pytest configuration for KiezMove.

Tests use a separate in-memory SQLite database instead of the
real development database.

A fresh database schema is created for every test so tests
cannot interfere with one another.
"""

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app import database
from backend.app.database import Base


# Use an in-memory SQLite database for tests.
#
# This database is completely separate from the real
# kiezmove.db development database.
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


# Create database sessions connected to the test database.
TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


# Replace the application's database configuration with
# the isolated test database.
database.engine = test_engine
database.SessionLocal = TestSessionLocal


@pytest.fixture(autouse=True)
def reset_database():
    """
    Create a clean database schema before every test.

    This prevents data created by one test from affecting
    another test.
    """

    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db():
    """
    Provide a database session to tests that need direct
    database access.

    The session uses the isolated in-memory test database.
    """

    session = TestSessionLocal()

    try:
        yield session
    finally:
        session.close()
