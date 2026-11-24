import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
_spec = importlib.util.spec_from_file_location("opencode_agents", Path(__file__).parent / "opencode-agents.py")
agents = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(agents)

CONFIG = """# Config
| Key | Meaning | Value |
|---|---|---|
| `requirements` | stories | `domain-model/requirements` |
| `problem-space` | root | `domain-model/problem-space` |
| `model-ground` | ground | `{ground}` |
| `model-writer` | writer | `{writer}` |
| `model-init` | init | `{init}` |
"""


class OpencodeAgents(unittest.TestCase):
    def run_in(self, **models):
        old = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                Path("domain-model").mkdir()
                Path("domain-model/config.md").write_text(CONFIG.format(**models))
                code = agents.main([])
                files = {p.name: p.read_text() for p in Path(".opencode/agents").glob("*.md")}
            finally:
                os.chdir(old)
        return code, files

    def test_provider_model_becomes_the_agent_model(self):
        code, files = self.run_in(ground="anthropic/claude-haiku-5-5", writer="inherit", init="anthropic/claude-sonnet-5-5")
        self.assertEqual(code, 0)
        self.assertIn("model: anthropic/claude-haiku-5-5", files["domain-ground.md"])
        self.assertIn("model: anthropic/claude-sonnet-5-5", files["domain-init-worker.md"])
        self.assertNotIn("model:", files["domain-writer.md"])
        self.assertIn("mode: subagent", files["domain-writer.md"])

    def test_claude_names_leave_the_agent_without_model(self):
        _, files = self.run_in(ground="haiku", writer="sonnet", init="opus")
        for text in files.values():
            self.assertNotIn("model:", text)

    def test_missing_config_fails(self):
        old = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                self.assertEqual(agents.main([]), 1)
            finally:
                os.chdir(old)


if __name__ == "__main__":
    unittest.main()
