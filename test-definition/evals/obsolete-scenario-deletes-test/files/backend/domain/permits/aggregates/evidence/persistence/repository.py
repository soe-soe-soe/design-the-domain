"""SQLAlchemy adapter of EvidenceRepository (bodies omitted in this fixture)."""

from ..model.root import Evidence


class SqlEvidenceRepository:
    def __init__(self, session):
        self._session = session

    async def get(self, evidence_id: str) -> Evidence: ...
    async def list_for_procedure(self, procedure_id: str) -> list[Evidence]: ...
    async def save(self, evidence: Evidence) -> None: ...
