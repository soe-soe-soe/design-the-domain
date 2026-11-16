from datetime import date
from unittest.mock import patch

from domain.deadlines.service import complete_deadline

DEADLINE = {"permit_id": "P1", "title": "Gutachten"}


def test_completing_a_deadline_marks_it_done():
    with patch("domain.deadlines.service.permits.on_deadline_done"):
        result = complete_deadline(DEADLINE, date(2026, 10, 16))
    assert result["done"] is True


def test_completing_a_deadline_informs_the_permit():
    with patch("domain.deadlines.service.permits.on_deadline_done") as informed:
        complete_deadline(DEADLINE, date(2026, 10, 16))
    informed.assert_called_once_with("P1", "Gutachten", date(2026, 10, 16))
