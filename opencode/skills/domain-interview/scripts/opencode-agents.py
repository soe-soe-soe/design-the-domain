#!/usr/bin/env python3
"""Write the subagent definitions of design-the-domain for OpenCode (refactoring 010, package 2).

Claude Code sets a subagent's model per call; OpenCode's `task` tool has no model parameter, the model
belongs to an agent definition. This writes one agent file per model key of `domain-model/config.md`
into `.opencode/agents/` of the project (run from the project root):

  model-ground  -> domain-ground       (reads the ground in domain-interview)
  model-writer  -> domain-writer       (user-story and functional-requirement, after each round)
  model-init    -> domain-init-worker  (one per subdomain in domain-init)

A value with a slash (`anthropic/claude-sonnet-5-5`) becomes the agent's `model:`. Any other value
(`inherit`, and the Claude names `haiku`, `sonnet`, `opus`, which OpenCode does not know) leaves the
agent without a model, so it runs on the session's model; the script says so. Run it again after the
config changed; OpenCode reads agent files at its start, so restart it then [not tried].

  opencode-agents.py [--dir .opencode/agents]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from requirements import SetupError, read_config  # noqa: E402

AGENTS = {
    "model-ground": ("domain-ground", "Reads the ground of a requirement (domain map, glossaries, subdomain maps, planned files) and reports it; changes nothing."),
    "model-writer": ("domain-writer", "Writes user stories and functional requirement changes from the answers of an interview round and reports open points."),
    "model-init": ("domain-init-worker", "Takes one subdomain's code over into the problem-space model (glossary, subdomain map, FRs)."),
}


def render(agent: str, description: str, model: str | None) -> str:
    lines = ["---", f"description: {description}", "mode: subagent"]
    if model:
        lines.append(f"model: {model}")
    lines += ["---", "", "Do what the brief you receive says, in the skill's rules it names. Your last message is your report.", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", type=Path, default=Path(".opencode/agents"))
    args = ap.parse_args(argv)
    try:
        config = read_config()
    except SetupError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    args.dir.mkdir(parents=True, exist_ok=True)
    for key, (agent, description) in AGENTS.items():
        value = config.get(key, "inherit")
        model = value if "/" in value else None
        (args.dir / f"{agent}.md").write_text(render(agent, description, model), encoding="utf-8")
        note = f"model {model}" if model else (f"{key} = {value}: not a provider/model value, the agent runs on the session's model" if value != "inherit" else "session's model")
        print(f"{args.dir / (agent + '.md')}: {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
