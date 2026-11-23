"""Database fixture: a fresh in-memory database per test."""

import pytest_asyncio


@pytest_asyncio.fixture
async def db_session():
    """Fresh in-memory database with all tables."""
    ...
