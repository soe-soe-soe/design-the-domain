"""Wiring fixtures: contexts wired with SQL repositories on the test database."""

import pytest_asyncio

from domain.deadlines.repository import DeadlineRepository
from domain.deadlines.service import DeadlineService
from domain.permits.aggregates.evidence.persistence.repository import SqlEvidenceRepository
from domain.permits.aggregates.procedure.persistence.repository import SqlProcedureRepository
from domain.permits.facade.facade import PermitsFacade


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
async def api_client(db_session):
    """HTTP client against the app, wired to the test database."""
    ...
