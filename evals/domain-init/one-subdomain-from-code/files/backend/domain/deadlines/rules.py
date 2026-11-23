from datetime import date


def is_overdue(due: date | None, today: date, done: bool) -> bool:
    """A deadline is overdue once its due date has passed, unless it is done."""
    if done:
        return False
    if due is None:
        return False
    return due < today


def reminder_days(kind: str) -> int:
    """Days before the due date a reminder goes out."""
    # TODO: 0 for "intern" – nobody decided this, it was a quick fix.
    if kind == "intern":
        return 0
    return 7
