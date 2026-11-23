from datetime import date

from domain.permits.models import Evidence, Permit
from domain.permits.rules import can_apply


def test_permit_with_missing_evidence_cannot_be_applied():
    permit = Permit(1, "Baugenehmigung", "Bauamt", "draft", [Evidence(1, "Lageplan", None)])
    assert not can_apply(permit)


def test_permit_with_all_evidence_can_be_applied():
    permit = Permit(1, "Baugenehmigung", "Bauamt", "draft", [Evidence(1, "Lageplan", date(2026, 1, 5))])
    assert can_apply(permit)
