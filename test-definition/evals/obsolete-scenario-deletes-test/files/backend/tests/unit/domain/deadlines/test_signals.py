"""
Unit-Tests für die Problemsignale eines Projekts.
"""

from datetime import date

import pytest

from domain.deadlines.regeln import signals

HEUTE = date(2026, 10, 16)


class TestUeberfaellig:
    @pytest.mark.fr("FR-fristen-001/S1")
    def test_heute_faellig_ist_ueberfaellig(self):
        """Wie die Dringlichkeit im Frontend: fällig heute oder früher."""
        assert signals.is_overdue(HEUTE, HEUTE) is True

    @pytest.mark.fr("FR-fristen-001/S2")
    def test_gestern_faellig_ist_ueberfaellig(self):
        assert signals.is_overdue(date(2026, 10, 15), HEUTE) is True

    @pytest.mark.fr("FR-fristen-001/S3")
    def test_morgen_faellig_ist_es_nicht(self):
        assert signals.is_overdue(date(2026, 10, 17), HEUTE) is False

    @pytest.mark.fr("FR-fristen-001/S4")
    def test_ohne_datum_nicht(self):
        assert signals.is_overdue(None, HEUTE) is False
