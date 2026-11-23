from dataclasses import dataclass, field
from datetime import date


@dataclass
class Extension:
    """One postponement of a deadline; exists only inside its deadline."""

    id: int
    reason: str
    new_due: date


@dataclass
class Deadline:
    id: int
    title: str
    due: date | None
    reminder: date | None
    done: bool
    responsible_id: int  # the Responsible who owns this deadline
    permit_id: int | None  # permit this deadline belongs to (subdomain permits)
    extensions: list[Extension] = field(default_factory=list)


@dataclass
class Responsible:
    """Person who answers for deadlines; has a life of its own (create, rename, deactivate)."""

    id: int
    name: str
    email: str
    active: bool
