from datetime import date

from domain.permits import facade


def test_done_deadline_appears_in_the_evidence_history():
    facade.evidence_history.clear()
    facade.on_deadline_done("P1", "Gutachten", date(2026, 10, 16))
    assert facade.evidence_history == [
        {"permit_id": "P1", "text": "Deadline done: Gutachten", "on": date(2026, 10, 16)}
    ]
