"""Status transitions a Nachweis may take (ADR 007)."""

from ..value_objects.evidence_status import EvidenceStatus

PERMITTED: dict[EvidenceStatus, set[EvidenceStatus]] = {
    EvidenceStatus.OPEN: {EvidenceStatus.COMMISSIONED},
    EvidenceStatus.COMMISSIONED: {EvidenceStatus.DELIVERED},
    EvidenceStatus.DELIVERED: {EvidenceStatus.IN_REVIEW},
    EvidenceStatus.IN_REVIEW: {EvidenceStatus.APPROVED},
    EvidenceStatus.APPROVED: set(),
}


class TransitionNotPermitted(Exception):
    pass


def check_permitted_transition(current: EvidenceStatus, target: EvidenceStatus) -> None:
    if target not in PERMITTED[current]:
        raise TransitionNotPermitted(f"{current} -> {target}")
