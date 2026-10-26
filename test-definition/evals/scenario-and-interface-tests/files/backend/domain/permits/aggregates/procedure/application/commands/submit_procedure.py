from ...model.root import ProcedureStatus


async def submit_procedure(repo, procedure_id: str) -> None:
    procedure = await repo.get(procedure_id)
    procedure.status = ProcedureStatus.SUBMITTED
    await repo.save(procedure)
