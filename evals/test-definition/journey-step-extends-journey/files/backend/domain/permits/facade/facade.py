"""Interface of the bounded context permits for other contexts."""

from ..aggregates.evidence.model.root import Evidence
from ..aggregates.procedure.model.root import Procedure


class PermitsFacade:
    def __init__(self, evidences, procedures):
        self._evidences = evidences
        self._procedures = procedures

    async def get_problem_evidences(self, project_id: str) -> list[tuple[str, str]]:
        """Non-archived evidences flagged with a problem, as (evidence_id, title)."""
        ...

    async def get_procedure(self, procedure_id: str) -> Procedure:
        return await self._procedures.get(procedure_id)

    async def get_evidence(self, evidence_id: str) -> Evidence:
        return await self._evidences.get(evidence_id)
