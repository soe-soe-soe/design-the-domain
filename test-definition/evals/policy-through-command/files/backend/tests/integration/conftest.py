"""Integration fixtures: a fresh database per test, contexts wired with SQL repositories."""

import pytest_asyncio

from domain.deadlines.repository import DeadlineRepository
from domain.deadlines.service import DeadlineService
from domain.permits.aggregates.evidence.persistence.repository import SqlEvidenceRepository
from domain.permits.aggregates.procedure.persistence.repository import SqlProcedureRepository
from domain.permits.application.event_bus import build_event_bus
from domain.permits.facade.facade import PermitsFacade


@pytest_asyncio.fixture
async def db_session():
    """Fresh in-memory database with all tables."""
    ...


@pytest_asyncio.fixture
async def evidences(db_session):
    return SqlEvidenceRepository(db_session)


@pytest_asyncio.fixture
async def permits_facade(db_session, evidences):
    return PermitsFacade(evidences, SqlProcedureRepository(db_session))


@pytest_asyncio.fixture
async def deadline_service(db_session, permits_facade):
    return DeadlineService(DeadlineRepository(), permits_facade)


@pytest_asyncio.fixture
async def procedures(db_session):
    return SqlProcedureRepository(db_session)


@pytest_asyncio.fixture
async def event_bus(procedures):
    """The event bus of permits with all its policies wired."""
    return build_event_bus(procedures)
