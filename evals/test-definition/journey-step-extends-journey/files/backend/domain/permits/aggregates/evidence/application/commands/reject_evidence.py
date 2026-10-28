"""Command: reject a Nachweis with a reason."""

from ...model.repository import EvidenceRepository


async def reject_evidence(repo: EvidenceRepository, evidence_id: str, reason: str) -> None:
    raise NotImplementedError
