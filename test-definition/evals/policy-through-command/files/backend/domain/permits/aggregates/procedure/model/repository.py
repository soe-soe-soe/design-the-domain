from typing import Protocol

from .root import Procedure


class ProcedureRepository(Protocol):
    async def get(self, procedure_id: str) -> Procedure: ...
    async def save(self, procedure: Procedure) -> None: ...
