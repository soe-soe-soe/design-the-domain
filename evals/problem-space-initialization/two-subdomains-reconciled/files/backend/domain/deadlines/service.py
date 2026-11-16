from datetime import date

from domain.permits import facade as permits


def complete_deadline(deadline: dict, done_on: date) -> dict:
    """A deadline is done on the given day; the permit it belongs to learns about it."""
    deadline = {**deadline, "done": True, "done_on": done_on}
    permits.on_deadline_done(deadline["permit_id"], deadline["title"], done_on)
    return deadline
