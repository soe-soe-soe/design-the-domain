"""Tests for interview-round.py – run with `python3 -m unittest discover scripts`."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("interview_round", Path(__file__).parent / "interview-round.py")
rnd = importlib.util.module_from_spec(_spec)
sys.modules["interview_round"] = rnd
_spec.loader.exec_module(rnd)

CONFIG = """
| Key | Meaning | Value |
|---|---|---|
| `user` | Person | Alex |
| `problem-space` | Root | `ps` |
| `requirements` | Stories | `ps/requirements` |
"""

STORY = """# US-0050: Erinnerung vor Fristablauf

Status: draft · Topic: Erinnerung · createdAt: 2026-11-01

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Erinnerung

  Szenario: AC1 – Erinnerung sieben Tage vorher
    Dann erhält Petra eine E-Mail

  @open
  Szenario: AC2 – Sammelmail
```

## Open

- **AC2** (problem-space-story): Gibt es eine Sammelmail? – Recommendation: Nein. – Changes: welche Mails Petra erhält
"""

PLANNED = """# FR-fristen-013: Fristerinnerung

Subdomain: fristen · Business object: frist · Type: Policy · Status: planned

## Changes

- US-0050 · Kind: new · Rule: changed

## Scenarios

```gherkin
# language: de
Funktionalität: Fristerinnerung

  @US-0050 @planned @open
  Szenario: S2 – Abgeleitete Frist sieben Tage vor Fälligkeit
    Angenommen eine abgeleitete Frist
```

## Open

- **S2** (problem-space-fr): Gilt die Erinnerung auch für abgeleitete Fristen? – Recommendation: Ja. – Story: US-0050 · Case: glossary · Type: Policy · Glossary: fristen.md: Abgeleitete Frist
"""


class RoundTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = os.getcwd()
        os.chdir(self.tmp.name)
        for path, text in {
            "domain-model/config.md": CONFIG,
            "ps/requirements/planned/US-0050-erinnerung.md": STORY,
            "ps/fristen/frist/planned/FR-fristen-013-fristerinnerung.md": PLANNED,
        }.items():
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(text, encoding="utf-8")
        self.cfg = rnd.read_config()

    def tearDown(self):
        os.chdir(self.old)
        self.tmp.cleanup()

    def own(self, **kw):
        q = {"title": "Absender", "body": "Von welcher Adresse?", "recommendation": "No-Reply."}
        q.update(kw)
        return q

    def test_round_one_has_no_headings_and_grilling_provenance(self):
        out = rnd.render({"start": 1, "group": False, "stories": [], "questions": [self.own(), self.own(title="Vorlauf")]}, self.cfg)
        self.assertNotIn("###", out)
        self.assertIn("❓ **Q1** - **Absender**: Von welcher Adresse?", out)
        self.assertIn("❓ **Q2** - **Vorlauf**", out)
        self.assertEqual(out.count("🗣️ grilling 🧩 grilling\n"), 2)
        self.assertNotIn("next question number", out)

    def test_fr_open_point_is_asked_under_its_story_with_full_provenance(self):
        out = rnd.render({"start": 5, "stories": ["US-0050"], "questions": [self.own()]}, self.cfg)
        self.assertIn("### 📘 US-0050: Erinnerung vor Fristablauf", out)
        self.assertIn("**Q5** - **Abgeleitete Frist sieben Tage vor Fälligkeit**", out)
        self.assertIn("🗣️ Alex 🧩 problem-space-fr 📋 FR-fristen-013/S2 📄 fristen.md: Abgeleitete Frist 📐 Policy", out)
        self.assertLess(out.index("US-0050"), out.index("### 🌐 Cross-cutting"))
        self.assertIn("**Q6** - **Absender**", out)
        self.assertNotIn("Sammelmail", out)  # story points wait for the closing round

    def test_questions_grouped_by_subdomain_headings(self):
        qs = [self.own(title="Lead time", group="genehmigung", source="problem-space-initialization", ref="FR-genehmigung-001/S2", type="Domain Service"),
              self.own(title="Overdue", group="fristen", source="problem-space-initialization")]
        out = rnd.render({"start": 1, "headings": {"fristen": "🧭 Fristen", "genehmigung": "🧭 Genehmigung"}, "questions": qs}, self.cfg)
        self.assertLess(out.index("### 🧭 Fristen"), out.index("### 🧭 Genehmigung"))
        self.assertLess(out.index("**Q1** - **Overdue**"), out.index("**Q2** - **Lead time**"))
        self.assertIn("🗣️ Alex 🧩 problem-space-initialization 📋 FR-genehmigung-001/S2 📐 Domain Service", out)
        self.assertNotIn("Sammelmail", out)

    def test_shared_question_is_asked_once(self):
        q = self.own(title="Abgeleitete Fristen", story="US-0050", same_as="FR-fristen-013/S2")
        out = rnd.render({"start": 1, "stories": ["US-0050"], "questions": [q]}, self.cfg)
        self.assertEqual(out.count("❓"), 1)
        self.assertIn("🗣️ Alex/grilling 🧩 grilling + problem-space-fr 📋 FR-fristen-013/S2", out)

    def test_closing_round_asks_story_points_and_skips_deferred(self):
        out = rnd.render({"start": 9, "stories": ["US-0050"], "closing": True, "deferred": ["FR-fristen-013/S2"], "questions": []}, self.cfg)
        self.assertIn("**Q9** - **Sammelmail**: Gibt es eine Sammelmail?", out)
        self.assertIn("🗣️ Alex 🧩 problem-space-story 📘 US-0050/AC2", out)
        self.assertNotIn("FR-fristen-013/S2", out)

    def test_parallel_change_from_writer(self):
        q = self.own(title="Parallele Änderung", story="US-0050", source="problem-space-fr", ref="FR-fristen-009/S6", type="Command")
        out = rnd.render({"start": 1, "stories": ["US-0050"], "deferred": ["FR-fristen-013/S2"], "questions": [q]}, self.cfg)
        self.assertIn("🗣️ Alex 🧩 problem-space-fr 📋 FR-fristen-009/S6 📐 Command", out)

    def test_provenance_is_the_last_line_of_each_question(self):
        out = rnd.render({"start": 1, "group": False, "stories": [], "questions": [self.own(), self.own()]}, self.cfg)
        blocks = [b.strip() for b in out.split("---")]
        for b in blocks:
            lines = [l for l in b.splitlines() if l]
            self.assertTrue(lines[-1].startswith("🗣️"), lines[-1])


if __name__ == "__main__":
    unittest.main()
