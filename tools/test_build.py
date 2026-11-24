import importlib.util
import tempfile
import unittest
from pathlib import Path

_spec = importlib.util.spec_from_file_location("build", Path(__file__).parent / "build.py")
b = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b)


def make_source(root: Path, skill_text: str, with_asset: bool = True) -> None:
    (root / "skills" / "demo-skill").mkdir(parents=True)
    (root / "skills" / "demo-skill" / "SKILL.md").write_text(skill_text)
    (root / "assets").mkdir()
    (root / "scripts").mkdir()
    if with_asset:
        (root / "assets" / "a.md").write_text("see `assets/b.md` and design-the-domain:other\n")
        (root / "assets" / "b.md").write_text("b\n")
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin" / "plugin.json").write_text('{"name": "x", "version": "1"}')


HEAD = "---\nname: demo-skill\ndescription: Does a demo.\n---\n\n# Demo\n\n"


class Build(unittest.TestCase):
    def build(self, text, target="claude", with_asset=True):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        src, out = Path(tmp.name) / "src", Path(tmp.name) / "out"
        make_source(src, text, with_asset)
        b.build(src, out, False, target)
        return out

    def test_follows_references_between_assets(self):
        out = self.build(HEAD + "Read `assets/a.md`.\n")
        self.assertTrue((out / "skills/demo-skill/assets/b.md").is_file())
        self.assertFalse((out / "assets").exists())

    def test_missing_file_fails(self):
        with self.assertRaises(b.BuildError):
            self.build(HEAD + "Read `assets/a.md`.\n", with_asset=False)

    def test_base_directory_script_path_counts(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        src = Path(tmp.name) / "src"
        make_source(src, HEAD + "Run `python3 <base directory>/scripts/s.py`.\n")
        (src / "scripts" / "s.py").write_text("import helper\n")
        (src / "scripts" / "helper.py").write_text("")
        b.build(src, Path(tmp.name) / "out", False)
        self.assertTrue((Path(tmp.name) / "out/skills/demo-skill/scripts/helper.py").is_file())

    def test_opencode_strips_namespace_and_writes_command(self):
        out = self.build(HEAD + "Call `design-the-domain:other` or /design-the-domain:other.\nRead `assets/a.md`.\n", "opencode")
        text = (out / "skills/demo-skill/SKILL.md").read_text()
        self.assertNotIn("design-the-domain:", text)
        self.assertNotIn("design-the-domain:", (out / "skills/demo-skill/assets/a.md").read_text())
        cmd = (out / "commands/demo-skill.md").read_text()
        self.assertIn("$ARGUMENTS", cmd)
        self.assertIn('description: "Does a demo."', cmd)
        self.assertIn("-opencode", (out / ".claude-plugin/plugin.json").read_text())

    def test_notes_pull_in_the_agent_script(self):
        text = b.opencode_text("domain-init", HEAD)
        self.assertIn("Harness notes (OpenCode)", text)
        self.assertIn("scripts/opencode-agents.py", text)
        self.assertEqual(b.opencode_text("glossary", HEAD), HEAD)

    def test_refuses_to_delete_a_foreign_folder(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        src, out = Path(tmp.name) / "src", Path(tmp.name) / "out"
        make_source(src, HEAD)
        out.mkdir()
        (out / "precious.txt").write_text("x")
        with self.assertRaises(b.BuildError):
            b.build(src, out, False)
        self.assertTrue((out / "precious.txt").exists())


if __name__ == "__main__":
    unittest.main()
