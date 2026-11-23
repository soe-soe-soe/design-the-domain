from domain.permits.models import Permit


def can_apply(permit: Permit) -> bool:
    """A permit may be applied for only when every evidence has been received."""
    return all(e.received is not None for e in permit.evidence)
