"""Aggregate root of a Nachweis."""

from dataclasses import dataclass, field

from .value_objects.evidence_status import EvidenceStatus


@dataclass
class Evidence:
    id: str
    procedure_id: str
    title: str
    status: EvidenceStatus = EvidenceStatus.OPEN
    has_problem: bool = False
    archived: bool = False
    rejection_reason: str | None = None
    history: list[str] = field(default_factory=list)
