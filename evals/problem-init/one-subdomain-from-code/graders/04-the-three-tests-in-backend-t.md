---
type: llm
focus: {source: file, path: backend/tests/unit/domain/deadlines/test_rules.py}
weight: 1
---

Each of the three tests carries @pytest.mark.fr("FR-fristen-NNN/Sn"); the test bodies (asserts and calls) are as before: is_overdue for a past date and for no due date, reminder_days("behoerde") == 7
