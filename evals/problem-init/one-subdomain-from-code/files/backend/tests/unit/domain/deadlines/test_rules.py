from datetime import date

from domain.deadlines.rules import is_overdue, reminder_days


def test_past_due_date_is_overdue():
    assert is_overdue(date(2026, 10, 15), date(2026, 10, 16), done=False)


def test_without_due_date_never_overdue():
    assert not is_overdue(None, date(2026, 10, 16), done=False)


def test_reminder_seven_days_before():
    assert reminder_days("behoerde") == 7
