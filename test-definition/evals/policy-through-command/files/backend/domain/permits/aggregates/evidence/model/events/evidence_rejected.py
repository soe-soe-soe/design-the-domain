"""Domain event: a Nachweis was rejected."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceRejected:
    evidence_id: str
    procedure_id: str
