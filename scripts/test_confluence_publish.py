"""Tests for confluence_publish.py – run with `python3 -m unittest discover scripts`."""

import contextlib
import io
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import confluence_publish as cp  # noqa: E402

CONFIG = """
| Key | Meaning | Value |
|---|---|---|
| `problem-space` | Root | `ps` |
| `domain-map` | Map | `ps/domain-map.md` |
| `confluence-space` | Space | `PRJ` |
| `confluence-parent` | Parent | `–` |
| `confluence-title-prefix` | Prefix | `–` |
"""

DOMAIN_MAP = """<!-- template comment -->
# Domain Map

Software für Fristen.

## Subdomains

| Subdomain | Type | Glossary | Subdomain map | Description |
|---|---|---|---|---|
| Fristen | Core | [fristen.md](../glossaries/fristen.md) | [subdomain-map.md](fristen/subdomain-map.md) | Stichtage und **Verantwortliche**. |
| Genehmigung | Supporting | [genehmigung.md](../glossaries/genehmigung.md) | – | Verfahren. |

## Relationships

| From | To | Description |
|---|---|---|
| Genehmigung | Fristen | Aus einem Nachweis entsteht eine Frist. |
"""

MAP = """# fristen – Subdomain Map

```mermaid
classDiagram
    class Frist["Frist"] {
        Titel: Text
    }
```
"""

GLOSSARY = """# Fristen

Stichtage.

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Subdomain | Fristen | Bounded Context | `deadlines` | Stichtage. |

## Frist

| Problem space | Term | Solution space | Identifier | Description |
|---|---|---|---|---|
| Business Object | Frist | Aggregate Root | `Deadline` | Ein Stichtag, siehe [Genehmigung](genehmigung.md). |
"""

FR = """# FR-fristen-001: Frist anlegen

Subdomain: fristen · Business object: frist · Type: Command · Status: valid

## Rule

Eine Frist hat ein Datum.

## Scenarios

```gherkin
# language: de
Funktionalität: Frist anlegen

  Szenario: S1 – Anlegen
    Wenn eine Frist <a & b> angelegt wird
```
"""


def write(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


class Project(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        write(self.root, "domain-model/config.md", CONFIG)
        write(self.root, "ps/domain-map.md", DOMAIN_MAP)
        write(self.root, "ps/fristen/subdomain-map.md", MAP)
        write(self.root, "glossaries/fristen.md", GLOSSARY)
        write(self.root, "glossaries/genehmigung.md", "# Genehmigung\n\nVerfahren.\n")
        write(self.root, "ps/fristen/frist/commands/FR-fristen-001-frist-anlegen.md", FR)
        write(self.root, "ps/fristen/frist/commands/planned/FR-fristen-002-geplant.md", FR.replace("001", "002"))
        self.old = os.getcwd()
        os.chdir(self.root)
        self.addCleanup(self.cleanup)

    def cleanup(self):
        os.chdir(self.old)
        self.tmp.cleanup()

    def build(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = cp.main(["build", "--out", "out", *args])
        manifest = json.loads(Path("out/manifest.json").read_text(encoding="utf-8")) if rc == 0 else None
        return rc, manifest, out.getvalue()


class BuildTree(Project):
    def test_tree_and_titles(self):
        rc, m, _ = self.build("--no-render")
        self.assertEqual(rc, 0)
        self.assertEqual(m["space"], "PRJ")
        self.assertIsNone(m["parent"])
        titles = [(p["title"], p["parent"]) for p in m["pages"]]
        self.assertEqual([t for t, _ in titles], [
            "Domain Map", "Fristen", "Fristen – Glossary", "Fristen / Frist",
            "FR-fristen-001: Frist anlegen", "Genehmigung", "Genehmigung – Glossary",
        ])
        keys = {p["key"]: p for p in m["pages"]}
        for p in m["pages"][1:]:
            self.assertIn(p["parent"], keys)
            self.assertLess(m["pages"].index(keys[p["parent"]]), m["pages"].index(p), "parent before child")

    def test_planned_frs_are_not_published(self):
        _, m, _ = self.build("--no-render")
        self.assertFalse([p for p in m["pages"] if "002" in p["title"]])

    def test_labels(self):
        _, m, _ = self.build("--no-render")
        fr = next(p for p in m["pages"] if p["kind"] == "fr")
        self.assertEqual(fr["labels"], ["dtd", "dtd-fr", "sd-fristen", "fr-fristen-001", "bo-fristen-frist", "status-valid"])

    def test_prefix(self):
        write(self.root, "domain-model/config.md", CONFIG.replace("| `confluence-title-prefix` | Prefix | `–` |", "| `confluence-title-prefix` | Prefix | `ACME` |"))
        _, m, _ = self.build("--no-render")
        self.assertEqual(m["pages"][0]["title"], "ACME Domain Map")
        self.assertEqual(m["pages"][1]["title"], "ACME Fristen")

    def test_missing_space_warns(self):
        write(self.root, "domain-model/config.md", CONFIG.replace("`PRJ`", "`–`"))
        _, m, _ = self.build("--no-render")
        self.assertIsNone(m["space"])
        self.assertTrue(any("confluence-space" in w for w in m["warnings"]))

    def test_missing_config_is_a_setup_error(self):
        Path("domain-model/config.md").unlink()
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = cp.main(["build", "--out", "out"])
        self.assertEqual(rc, 1)
        self.assertIn("config.md missing", err.getvalue())


class Bodies(Project):
    def body(self, kind, title=None):
        _, m, _ = self.build("--no-render")
        page = next(p for p in m["pages"] if p["kind"] == kind and (title is None or p["title"] == title))
        return Path("out", page["body_file"]).read_text(encoding="utf-8")

    def test_links_become_page_links(self):
        body = self.body("domain-map")
        self.assertIn('<ri:page ri:content-title="Fristen – Glossary" />', body)
        self.assertIn('<ri:page ri:content-title="Genehmigung" />', body)
        self.assertIn("<strong>Verantwortliche</strong>", body)

    def test_glossary_link_between_glossaries(self):
        body = self.body("glossary", "Fristen – Glossary")
        self.assertIn('<ri:page ri:content-title="Genehmigung – Glossary" />', body)
        self.assertIn("<code>Deadline</code>", body)

    def test_unresolvable_link_warns_and_stays_text(self):
        write(self.root, "glossaries/fristen.md", GLOSSARY.replace("genehmigung.md", "gibtsnicht.md"))
        _, m, _ = self.build("--no-render")
        self.assertTrue(any("gibtsnicht.md" in w for w in m["warnings"]))

    def test_fr_page_keeps_gherkin_in_a_code_macro_without_h1(self):
        body = self.body("fr")
        self.assertNotIn("<h1>", body)
        self.assertIn("<![CDATA[# language: de", body)
        self.assertIn("Wenn eine Frist <a & b> angelegt wird", body)  # CDATA: no escaping
        self.assertIn("<h2>Rule</h2>", body)

    def test_business_object_page_lists_its_frs(self):
        body = self.body("business-object")
        self.assertIn("FR-fristen-001: Frist anlegen", body)
        self.assertIn("Eine Frist hat ein Datum.", body)
        self.assertIn("Command", body)

    def test_subdomain_page_has_map_objects_and_relationships(self):
        body = self.body("subdomain", "Fristen")
        self.assertIn("classDiagram", body)
        self.assertIn('<ri:page ri:content-title="Fristen / Frist" />', body)
        self.assertIn("Relationships to other subdomains", body)

    def test_subdomain_without_map_has_no_diagram(self):
        body = self.body("subdomain", "Genehmigung")
        self.assertNotIn("Subdomain map", body)

    def test_domain_map_diagram_source(self):
        body = self.body("domain-map")
        self.assertIn("flowchart LR", body)
        self.assertIn('n0["Fristen<br/>Core"]:::core', body)
        self.assertIn("n1 -->|1| n0", body)

    def test_html_escaping_in_text(self):
        write(self.root, "glossaries/fristen.md", GLOSSARY.replace("Ein Stichtag", "Ein <Stichtag> & mehr"))
        body = self.body("glossary", "Fristen – Glossary")
        self.assertIn("Ein &lt;Stichtag&gt; &amp; mehr", body)


class Safety(Project):
    def test_cdata_breakout_in_a_label_is_neutralised(self):
        write(self.root, "ps/domain-map.md", DOMAIN_MAP.replace("| Fristen | Core", "| Fr]]><b>x | Core"))
        _, m, _ = self.build("--no-render")
        body = Path("out", m["pages"][0]["body_file"]).read_text(encoding="utf-8")
        self.assertNotIn("<![CDATA[Fr]]><b>", body)
        self.assertIn("Fr]]]]><![CDATA[><b>x", body)

    def test_links_outside_the_project_are_ignored(self):
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        secret = Path(outside.name) / "secret.md"
        secret.write_text("# Geheim\n\nTOPSECRET\n", encoding="utf-8")
        write(self.root, "ps/domain-map.md", DOMAIN_MAP.replace("../glossaries/fristen.md", os.path.relpath(secret, self.root / "ps")))
        _, m, _ = self.build("--no-render")
        self.assertTrue(any("outside the project" in w for w in m["warnings"]))
        for p in m["pages"]:
            self.assertNotIn("TOPSECRET", Path("out", p["body_file"]).read_text(encoding="utf-8"))

    def test_symlinked_fr_is_ignored(self):
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        target = Path(outside.name) / "FR-fristen-077-x.md"
        target.write_text(FR.replace("001", "077").replace("Eine Frist hat", "TOPSECRET"), encoding="utf-8")
        (self.root / "ps/fristen/frist/FR-fristen-077-x.md").symlink_to(target)
        _, m, _ = self.build("--no-render")
        self.assertFalse([p for p in m["pages"] if "077" in p["title"]])


class Rendering(Project):
    def fake_mmdc(self, body: str) -> Path:
        script = self.root / "fake-mmdc"
        script.write_text("#!/bin/sh\n" + body, encoding="utf-8")
        script.chmod(script.stat().st_mode | stat.S_IEXEC)
        return script

    def test_render_attaches_svg_and_embeds_image(self):
        # fake mmdc: copies the input file to the -o path
        script = self.fake_mmdc('in=""; out=""; while [ $# -gt 0 ]; do case "$1" in -i) in="$2"; shift;; -o) out="$2"; shift;; esac; shift; done; echo "<svg/>" > "$out"\n')
        os.environ["MMDC"] = str(script)
        self.addCleanup(os.environ.pop, "MMDC", None)
        _, m, _ = self.build()
        root = m["pages"][0]
        self.assertEqual([a["name"] for a in root["attachments"]], ["domain-map.svg"])
        self.assertTrue(Path("out", root["attachments"][0]["file"]).exists())
        self.assertIn('<ri:attachment ri:filename="domain-map.svg" />', Path("out", root["body_file"]).read_text(encoding="utf-8"))
        fristen = next(p for p in m["pages"] if p["title"] == "Fristen")
        self.assertEqual([a["name"] for a in fristen["attachments"]], ["fristen-subdomain-map.svg"])
        self.assertFalse(list(Path("out/attachments").glob("*.mmd")))

    def test_failing_renderer_falls_back_to_code_block(self):
        script = self.fake_mmdc("echo boom >&2; exit 1\n")
        os.environ["MMDC"] = str(script)
        self.addCleanup(os.environ.pop, "MMDC", None)
        _, m, _ = self.build()
        self.assertEqual(m["pages"][0]["attachments"], [])
        self.assertTrue(any("rendering failed" in w for w in m["warnings"]))

    def test_missing_renderer_warns_once(self):
        os.environ["MMDC"] = "no-such-mmdc-binary"
        self.addCleanup(os.environ.pop, "MMDC", None)
        _, m, _ = self.build()
        self.assertEqual(len([w for w in m["warnings"] if "not found" in w and "no-such" in w]), 1)


class Hashes(Project):
    def test_hash_is_stable_and_changes_with_content(self):
        _, m1, _ = self.build("--no-render")
        _, m2, _ = self.build("--no-render")
        self.assertEqual([p["sha256"] for p in m1["pages"]], [p["sha256"] for p in m2["pages"]])
        fr = Path("ps/fristen/frist/commands/FR-fristen-001-frist-anlegen.md")
        fr.write_text(fr.read_text(encoding="utf-8").replace("ein Datum", "zwei Daten"), encoding="utf-8")
        _, m3, _ = self.build("--no-render")
        changed = [p["title"] for p, q in zip(m1["pages"], m3["pages"]) if p["sha256"] != q["sha256"]]
        self.assertEqual(changed, ["Fristen / Frist", "FR-fristen-001: Frist anlegen"])


if __name__ == "__main__":
    unittest.main()
