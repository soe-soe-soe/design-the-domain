---
type: llm
focus: trace
weight: 1
---

backend/tests/unit/domain/deadlines/test_signals.py still contains exactly one test marked @pytest.mark.fr("FR-fristen-001/S1"), and it now asserts that is_overdue(date(2026, 10, 16), date(2026, 10, 16)) is False
