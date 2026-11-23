from datetime import date


def is_overdue(due: date | None, today: date, done: bool) -> bool:
    """A deadline is overdue once its due date has passed, unless it is done."""
    if done or due is None:
        return False
    return due < today
