from datetime import date

from domain.deadlines.rules import is_overdue


def test_past_due_date_is_overdue():
    assert is_overdue(date(2026, 10, 15), date(2026, 10, 16), done=False)


def test_done_deadline_is_never_overdue():
    assert not is_overdue(date(2026, 10, 15), date(2026, 10, 16), done=True)
