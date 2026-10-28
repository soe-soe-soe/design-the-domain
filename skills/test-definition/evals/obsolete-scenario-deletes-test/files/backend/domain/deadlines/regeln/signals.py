"""Problem signals of a project (not yet migrated: rule module)."""

from datetime import date


def is_overdue(due_date: date | None, today: date) -> bool:
    if due_date is None:
        return False
    return due_date <= today
