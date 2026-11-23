from dataclasses import dataclass, field
from datetime import date


@dataclass
class Evidence:
    """A document that proves a requirement of a permit; exists only inside its permit."""

    id: int
    title: str
    received: date | None


@dataclass
class Permit:
    id: int
    title: str
    authority: str
    status: str  # draft | applied | granted | rejected
    evidence: list[Evidence] = field(default_factory=list)
