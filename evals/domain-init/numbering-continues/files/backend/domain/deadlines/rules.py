from datetime import date


def is_overdue(due: date | None, today: date, done: bool) -> bool:
    """A deadline is overdue once its due date has passed, unless it is done."""
    if done or due is None:
        return False
    return due < today


def escalation_level(days_overdue: int) -> str:
    """Overdue deadlines escalate: after 14 days to the team lead, after 30 days to the management."""
    if days_overdue >= 30:
        return "management"
    if days_overdue >= 14:
        return "team-lead"
    return "none"
