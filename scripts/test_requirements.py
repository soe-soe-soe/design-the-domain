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

ACTIVE = """# FR-fristen-003: Fristerinnerung

Subdomain: fristen · Business object: frist · Type: Policy · Status: valid

## Rule

Erinnert 7 Tage vor Fälligkeit.

## Scenarios

```gherkin
# language: de
Funktionalität: Fristerinnerung

  @US-0050
  Szenario: S1 – Erinnerung 7 Tage vorher
    Angenommen eine Frist
    Wenn 7 Tage vorher
    Dann wird erinnert

  @US-0050
  Szenario: S2 – Keine Erinnerung für erledigte Fristen
    Angenommen eine erledigte Frist
    Wenn 7 Tage vorher
    Dann wird nicht erinnert

  @existing
  Szenario: S3 – Erinnerung an Vertretung
    Angenommen eine Vertretung
    Wenn 7 Tage vorher
    Dann wird die Vertretung erinnert
```
"""

PLANNED = """# FR-fristen-003: Fristerinnerung

Subdomain: fristen · Business object: frist · Type: Policy · Status: planned

## Changes

- US-0060 · Kind: edit · Rule: changed

## Rule

Erinnert 3 Tage vor Fälligkeit.

## Scenarios

```gherkin
# language: de
Funktionalität: Fristerinnerung

  @US-0060 @planned @base-US-0050
  Szenario: S1 – Erinnerung 3 Tage vorher
    Angenommen eine Frist
    Wenn 3 Tage vorher
    Dann wird erinnert

  @US-0060 @planned @obsolete @base-existing
  Szenario: S3 – entfällt: Erinnerung an Vertretung

  @US-0060 @planned
  Szenario: S4 – Wöchentliche Sammelmail
    Angenommen abbestellte Erinnerungen
    Wenn Montag
    Dann kommt eine Sammelmail
```
"""

STORY = """# US-0060: Erinnerung 3 Tage vorher

Status: in-progress · Topic: Erinnerung · createdAt: 2026-10-30

## Functional requirements

- FR-fristen-003 (edit): AC1 → S1, AC2 → S3 obsolete, AC3 → S4
"""

NEW_FR = """# FR-fristen-010: Sammelmail

Subdomain: fristen · Business object: frist · Type: Policy · Status: planned

## Changes

- US-0060 · Kind: new · Rule: changed

## Rule

Wöchentliche Sammelmail.

## Scenarios

```gherkin
# language: de
Funktionalität: Sammelmail

  @US-0060 @planned
  Szenario: S1 – Sammelmail am Montag
    Angenommen abbestellte Erinnerungen
    Wenn Montag
    Dann kommt eine Sammelmail
```
"""


class RequirementsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = os.getcwd()
        os.chdir(self.tmp.name)
        self.write(".claude/pts.md", CONFIG)
        self.write("ps/fristen/frist/FR-fristen-003-erinnerung.md", ACTIVE)
        self.write("ps/fristen/frist/planned/FR-fristen-003-erinnerung.md", PLANNED)
        self.write("ps/fristen/frist/planned/FR-fristen-010-sammelmail.md", NEW_FR)
        self.write("ps/requirements/planned/US-0060-erinnerung.md", STORY)

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

    def test_close_merges_moves_and_dates(self):
        code, out = self.run_cmd("close", "US-0060")
        self.assertEqual(code, 0, out)
        active = Path("ps/fristen/frist/FR-fristen-003-erinnerung.md").read_text()
        self.assertIn("Erinnert 3 Tage vor Fälligkeit.", active)
        self.assertIn("@US-0060\n  Szenario: S1 – Erinnerung 3 Tage vorher", active)
        self.assertIn("@US-0050\n  Szenario: S2", active)
        self.assertIn("@US-0060 @obsolete\n  Szenario: S3 – entfällt", active)
        self.assertIn("Szenario: S4 – Wöchentliche Sammelmail", active)
        self.assertNotIn("@planned", active)
        self.assertNotIn("@base-", active)
        new = Path("ps/fristen/frist/FR-fristen-010-sammelmail.md").read_text()
        self.assertIn("Status: valid", new)
        self.assertNotIn("## Changes", new)
        self.assertFalse(Path("ps/fristen/frist/planned").exists())
        story = Path("ps/requirements/US-0060-erinnerung.md").read_text()
        self.assertRegex(story, r"Status: done · .* · doneAt: \d{4}-\d\d-\d\d")
        self.assertFalse(Path("ps/requirements/planned/US-0060-erinnerung.md").exists())

    def test_stale_base_is_a_conflict_and_writes_nothing(self):
        self.write(
            "ps/fristen/frist/FR-fristen-003-erinnerung.md",
            ACTIVE.replace("@US-0050\n  Szenario: S1", "@US-0058\n  Szenario: S1"),
        )
        code, out = self.run_cmd("close", "US-0060")
        self.assertEqual(code, 2)
        self.assertIn("last changed by @US-0058", out)
        self.assertTrue(Path("ps/fristen/frist/planned/FR-fristen-003-erinnerung.md").exists())
        self.assertIn("in-progress", Path("ps/requirements/planned/US-0060-erinnerung.md").read_text())

    def test_parallel_story_in_same_planned_file(self):
        text = PLANNED.replace(
            "- US-0060 · Kind: edit · Rule: changed",
            "- US-0060 · Kind: edit · Rule: changed\n- US-0061 · Kind: edit · Rule: unchanged",
        ).replace(
            "```\n",
            "\n  @US-0061 @planned @base-US-0050\n  Szenario: S1 – Erinnerung 5 Tage vorher\n    Dann x\n```\n",
        )
        self.write("ps/fristen/frist/planned/FR-fristen-003-erinnerung.md", text)
        code, out = self.run_cmd("check", "US-0061")
        self.assertEqual(code, 2)
        self.assertIn("also changed by @US-0060", out)

    def test_cancel_removes_changes_and_moves_story(self):
        code, out = self.run_cmd("cancel", "US-0060")
        self.assertEqual(code, 0, out)
        self.assertFalse(Path("ps/fristen/frist/planned").exists())
        self.assertIn("Status: cancelled", Path("ps/requirements/cancelled/US-0060-erinnerung.md").read_text())
        self.assertEqual(Path("ps/fristen/frist/FR-fristen-003-erinnerung.md").read_text(), ACTIVE)

    def test_history_latest_first(self):
        self.run_cmd("close", "US-0060")
        self.write(
            "ps/requirements/US-0050-erinnerung.md",
            "# US-0050: Erinnerung\n\nStatus: done · createdAt: 2026-09-01 · doneAt: 2026-09-10\n\n"
            "## Functional requirements\n\n- FR-fristen-003 (new): AC1 → S1, AC2 → S2\n",
        )
        code, out = self.run_cmd("history", "FR-fristen-003")
        self.assertEqual(code, 0)
        self.assertLess(out.index("US-0060"), out.index("US-0050"))

    def test_history_names_scenarios_taken_from_code(self):
        code, out = self.run_cmd("history", "FR-fristen-003")
        self.assertEqual(code, 0)
        self.assertIn("existing: taken over from code", out)


if __name__ == "__main__":
    unittest.main()
