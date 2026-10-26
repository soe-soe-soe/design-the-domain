"""Deadlines and problem signals (not yet migrated: classic layering)."""

from domain.permits.facade.facade import PermitsFacade

from .repository import DeadlineRepository


class DeadlineService:
    def __init__(self, repo: DeadlineRepository, permits: PermitsFacade):
        self._repo = repo
        self._permits = permits

    async def get_signals(self, project_id: str) -> dict[str, int]:
        overdue = await self._repo.count_overdue(project_id)
        problems = await self._permits.get_problem_evidences(project_id)
        return {"overdue": overdue, "problems": len(problems)}
