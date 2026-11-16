"""Tests for requirements.py – run with `python3 -m unittest discover scripts`."""

import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import requirements as req  # noqa: E402

CONFIG = """
| Key | Meaning | Value |
|---|---|---|
| `problem-space` | Root | `ps` |
| `requirements` | Stories | `ps/requirements` |
"""

ACTIVE = """# FR-deadlines-003: Deadline reminder

Subdomain: deadlines · Business object: deadline · Type: Policy · Status: valid

## Rule

Reminds 7 days before the due date.

## Scenarios

```gherkin
# language: en
Feature: Deadline reminder

  @US-0050
  Scenario: S1 – Reminder 7 days before
    Given a deadline
    When 7 days before
    Then a reminder is sent

  @US-0050
  Scenario: S2 – No reminder for done deadlines
    Given a done deadline
    When 7 days before
    Then nobody is reminded

  @existing
  Scenario: S3 – Reminder to the deputy
    Given a deputy
    When 7 days before
    Then the deputy is reminded
```
"""

PLANNED = """# FR-deadlines-003: Deadline reminder

Subdomain: deadlines · Business object: deadline · Type: Policy · Status: planned

## Changes

- US-0060 · Kind: edit · Rule: changed

## Rule

Reminds 3 days before the due date.

## Scenarios

```gherkin
# language: en
Feature: Deadline reminder

  @US-0060 @planned @base-US-0050
  Scenario: S1 – Reminder 3 days before
    Given a deadline
    When 3 days before
    Then a reminder is sent

  @US-0060 @planned @obsolete @base-existing
  Scenario: S3 – dropped: Reminder to the deputy

  @US-0060 @planned
  Scenario: S4 – Weekly digest
    Given unsubscribed reminders
    When Monday
    Then a digest is sent
```
"""

STORY = """# US-0060: Reminder 3 days before

Status: in-progress · Topic: reminder · createdAt: 2026-10-30

## Functional requirements

- FR-deadlines-003 (edit): AC1 → S1, AC2 → S3 obsolete, AC3 → S4
"""

NEW_FR = """# FR-deadlines-010: Digest

Subdomain: deadlines · Business object: deadline · Type: Policy · Status: planned

## Changes

- US-0060 · Kind: new · Rule: changed

## Rule

Weekly digest.

## Scenarios

```gherkin
# language: en
Feature: Digest

  @US-0060 @planned
  Scenario: S1 – Digest on Monday
    Given unsubscribed reminders
    When Monday
    Then a digest is sent
```
"""


class RequirementsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = os.getcwd()
        os.chdir(self.tmp.name)
        self.write(".claude/pts.md", CONFIG)
        self.write("ps/deadlines/deadline/policies/FR-deadlines-003-reminder.md", ACTIVE)
        self.write("ps/deadlines/deadline/policies/planned/FR-deadlines-003-reminder.md", PLANNED)
        self.write("ps/deadlines/deadline/policies/planned/FR-deadlines-010-digest.md", NEW_FR)
        self.write("ps/requirements/planned/US-0060-reminder.md", STORY)

    def tearDown(self):
        os.chdir(self.old)
        self.tmp.cleanup()

    def write(self, path, text):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(text, encoding="utf-8")

    def run_cmd(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = req.main(["requirements.py", *args])
        return code, out.getvalue()

    def test_complete_merges_moves_and_dates(self):
        code, out = self.run_cmd("complete", "US-0060")
        self.assertEqual(code, 0, out)
        active = Path("ps/deadlines/deadline/policies/FR-deadlines-003-reminder.md").read_text()
        self.assertIn("Reminds 3 days before the due date.", active)
        self.assertIn("@US-0060\n  Scenario: S1 – Reminder 3 days before", active)
        self.assertIn("@US-0050\n  Scenario: S2", active)
        self.assertIn("@US-0060 @obsolete\n  Scenario: S3 – dropped", active)
        self.assertIn("Scenario: S4 – Weekly digest", active)
        self.assertNotIn("@planned", active)
        self.assertNotIn("@base-", active)
        new = Path("ps/deadlines/deadline/policies/FR-deadlines-010-digest.md").read_text()
        self.assertIn("Status: valid", new)
        self.assertNotIn("## Changes", new)
        self.assertFalse(Path("ps/deadlines/deadline/policies/planned").exists())
        story = Path("ps/requirements/US-0060-reminder.md").read_text()
        self.assertRegex(story, r"Status: done · .* · doneAt: \d{4}-\d\d-\d\d")
        self.assertFalse(Path("ps/requirements/planned/US-0060-reminder.md").exists())

    def test_stale_base_is_a_conflict_and_writes_nothing(self):
        self.write(
            "ps/deadlines/deadline/policies/FR-deadlines-003-reminder.md",
            ACTIVE.replace("@US-0050\n  Scenario: S1", "@US-0058\n  Scenario: S1"),
        )
        code, out = self.run_cmd("complete", "US-0060")
        self.assertEqual(code, 2)
        self.assertIn("last changed by @US-0058", out)
        self.assertTrue(Path("ps/deadlines/deadline/policies/planned/FR-deadlines-003-reminder.md").exists())
        self.assertIn("in-progress", Path("ps/requirements/planned/US-0060-reminder.md").read_text())

    def test_parallel_story_in_same_planned_file(self):
        text = PLANNED.replace(
            "- US-0060 · Kind: edit · Rule: changed",
            "- US-0060 · Kind: edit · Rule: changed\n- US-0061 · Kind: edit · Rule: unchanged",
        ).replace(
            "```\n",
            "\n  @US-0061 @planned @base-US-0050\n  Scenario: S1 – Reminder 5 days before\n    Then x\n```\n",
        )
        self.write("ps/deadlines/deadline/policies/planned/FR-deadlines-003-reminder.md", text)
        code, out = self.run_cmd("check", "US-0061")
        self.assertEqual(code, 2)
        self.assertIn("also changed by @US-0060", out)

    def test_cancel_removes_changes_and_moves_story(self):
        code, out = self.run_cmd("cancel", "US-0060")
        self.assertEqual(code, 0, out)
        self.assertFalse(Path("ps/deadlines/deadline/policies/planned").exists())
        self.assertIn("Status: cancelled", Path("ps/requirements/cancelled/US-0060-reminder.md").read_text())
        self.assertEqual(Path("ps/deadlines/deadline/policies/FR-deadlines-003-reminder.md").read_text(), ACTIVE)

    def test_history_latest_first(self):
        self.run_cmd("complete", "US-0060")
        self.write(
            "ps/requirements/US-0050-reminder.md",
            "# US-0050: Reminder\n\nStatus: done · createdAt: 2026-09-01 · doneAt: 2026-09-10\n\n"
            "## Functional requirements\n\n- FR-deadlines-003 (new): AC1 → S1, AC2 → S2\n",
        )
        code, out = self.run_cmd("history", "FR-deadlines-003")
        self.assertEqual(code, 0)
        self.assertLess(out.index("US-0060"), out.index("US-0050"))

    def test_history_names_scenarios_taken_from_code(self):
        code, out = self.run_cmd("history", "FR-deadlines-003")
        self.assertEqual(code, 0)
        self.assertIn("existing: taken over from code", out)

    def test_next_fr_counts_across_active_and_planned(self):
        code, out = self.run_cmd("next-fr", "deadlines")
        self.assertEqual((code, out.strip()), (0, "FR-deadlines-011"))

    def test_next_fr_of_a_new_subdomain_starts_at_one(self):
        code, out = self.run_cmd("next-fr", "permits")
        self.assertEqual((code, out.strip()), (0, "FR-permits-001"))

    def test_next_fr_does_not_mix_subdomains_with_a_common_prefix(self):
        self.write("ps/deadline/FR-deadline-007-other.md", "# FR-deadline-007: Other\n")
        code, out = self.run_cmd("next-fr", "deadline")
        self.assertEqual(out.strip(), "FR-deadline-008")


if __name__ == "__main__":
    unittest.main()
