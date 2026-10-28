"""POST /evidences/{evidence_id}/reject -> reject_evidence"""

from fastapi import APIRouter

from ..schemas.evidence import RejectEvidenceRequest

router = APIRouter()


@router.post("/evidences/{evidence_id}/reject")
async def reject_evidence(evidence_id: str, body: RejectEvidenceRequest) -> None:
    raise NotImplementedError
