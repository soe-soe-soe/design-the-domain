"""Policy: a rejected Nachweis sends its Antrag into rework."""

from ....evidence.model.events.evidence_rejected import EvidenceRejected
from ...model.repository import ProcedureRepository


async def on_evidence_rejected(procedures: ProcedureRepository, event: EvidenceRejected) -> None:
    raise NotImplementedError
