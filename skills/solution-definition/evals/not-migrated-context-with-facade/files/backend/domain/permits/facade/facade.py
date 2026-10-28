"""Interface of the bounded context permits for other contexts."""


class PermitsFacade:
    def __init__(self, evidences, procedures):
        self._evidences = evidences
        self._procedures = procedures

    async def get_problem_evidences(self, project_id: str) -> list[tuple[str, str]]:
        """Non-archived evidences flagged with a problem, as (evidence_id, title)."""
        ...
