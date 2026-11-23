from datetime import date

from domain.deadlines.rules import escalation_level, is_overdue


def test_past_due_date_is_overdue():
    assert is_overdue(date(2026, 10, 15), date(2026, 10, 16), done=False)


def test_after_14_days_the_team_lead_is_informed():
    assert escalation_level(14) == "team-lead"


def test_after_30_days_the_management_is_informed():
    assert escalation_level(30) == "management"
