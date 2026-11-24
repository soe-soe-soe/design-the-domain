#!/usr/bin/env python3
"""Build the neutral core of design-the-domain: self-contained skill folders (refactoring 010, 1a).

    python3 tools/build.py [--source DIR] [--out DIR] [--target claude|opencode] [--with-evals] [--check]

The source keeps `assets/` and `scripts/` once. The build puts into each skill folder what that skill
needs: it reads the paths its files name (`assets/<file>`, `scripts/<file>`), follows what those
files name themselves (an asset naming another asset, a script importing a script of `scripts/`) and
copies the files to the same relative path inside the skill folder. A path to a file that does not
exist fails the build. Nothing is listed by hand.

It also checks the name rule of refactoring 011: `name:` equals the folder, is lowercase with
hyphens, is on no deny list (`tools/denied-skill-names.txt`) and no other plugin of the repository
(`implement-the-domain/`) has a skill of that name.

`--target opencode` (default out `build/opencode/`) builds the same skill folders for OpenCode: the
`design-the-domain:` namespace is stripped from the cross-references (OpenCode knows only `name:`),
a "Harness notes (OpenCode)" section is appended where a skill starts subagents or asks questions, and
`commands/<name>.md` wrappers give every skill its slash name. A manifest named `design-the-domain-opencode` (apm takes the folder as a package by it), no evals.

Output of the default target (default `build/design-the-domain/`): `.claude-plugin/plugin.json`, `skills/<name>/` (without
`decision-records/`), `LICENSE`, `THIRD_PARTY_LICENSES.md`; with `--with-evals` also `evals/`, so that
`claude plugin eval` finds the cases when run from the output. `--check` builds into a temporary
folder and compares it with `--out`: a stale build is an error (exit 1).
"""
from __future__ import annotations

import argparse
import json
import filecmp
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ("assets", "scripts")
# `assets/glossary.md`, `scripts/requirements.py`, `<base directory>/scripts/…`; not preceded by a path character, so
# `domain-model/assets/x.md` and `../assets/x.md` are not ours. A name needs an extension.
PATH_RE = re.compile(r"(?:(?<![\w./\-])|(?<=<base directory>/))((?:assets|scripts)/[\w\-]+(?:\.[\w\-]+)*\.(?:md|py|sh|json|ya?ml|txt))")
IMPORT_RE = re.compile(r"^\s*(?:from|import)\s+([A-Za-z_]\w*)", re.M)
NAME_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
# Paths that appear in a skill text but are no dependency; none today. A `(skill, path)` pair.
EXCEPTIONS: set[tuple[str, str]] = set()
SKIP_DIRS = {"decision-records", "__pycache__"}
OTHER_PLUGINS = ("implement-the-domain",)
MARKER = ".build-output"
NAMESPACE_RE = re.compile(r"design-the-domain:(?=[a-z])")
# What OpenCode needs said where a skill starts subagents or asks questions (refactoring 010, 1b).
# Only the skills that do; the text is appended to the skill in the OpenCode output.
SUBAGENTS = (
    "Subagents: start them with the `task` tool and the `subagent_type` named below. Their model comes from "
    "the agent file, not from a parameter: if `.opencode/agents/<subagent_type>.md` does not exist yet, or "
    "`domain-model/config.md` changed its `model-…` value, run "
    "`python3 <base directory>/scripts/opencode-agents.py` from the project root first (restart OpenCode "
    "after a changed model). A `model-…` value that is not `provider/model` means the session's model."
)
HARNESS_NOTES = {
    "domain-interview": [SUBAGENTS, "`domain-ground` for the ground (`model-ground`), `domain-writer` for the writers (`model-writer`)."],
    "domain-init": [
        SUBAGENTS,
        "`domain-init-worker` for the subdomain subagents (`model-init`).",
        "Questions to the user with the `question` tool where this skill says AskUserQuestion; if the tool is "
        "missing, ask in plain text and wait for the answer. Do not skip the question.",
    ],
}
SCRIPT_FOR_NOTES = "scripts/opencode-agents.py"


class BuildError(Exception):
    pass


def frontmatter_name(skill_md: Path) -> str:
    text = skill_md.read_text()
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        raise BuildError(f"{skill_md}: no frontmatter")
    n = re.search(r"^name:\s*(\S+)\s*$", m.group(1), re.M)
    if not n:
        raise BuildError(f"{skill_md}: no name: in the frontmatter")
    return n.group(1).strip("\"'")


def denied_names() -> set[str]:
    out = set()
    for line in (ROOT / "tools" / "denied-skill-names.txt").read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            out.add(line)
    return out


def check_names(source: Path) -> list[str]:
    errors, seen = [], {}
    denied = denied_names()
    other = {}
    for plugin in OTHER_PLUGINS:
        for md in sorted((source / plugin / "skills").glob("*/SKILL.md")):
            other[frontmatter_name(md)] = plugin
    for md in sorted((source / "skills").glob("*/SKILL.md")):
        folder, name = md.parent.name, frontmatter_name(md)
        if name != folder:
            errors.append(f"skill {folder}: name: is {name!r}, folder and name must be the same")
        if not NAME_RE.match(name):
            errors.append(f"skill {folder}: name {name!r} is not lowercase words joined by hyphens")
        if name in denied:
            errors.append(f"skill {folder}: name {name!r} is on the deny list (tools/denied-skill-names.txt)")
        if name in other:
            errors.append(f"skill {folder}: name {name!r} also exists in {other[name]}")
        if name in seen:
            errors.append(f"skill {folder}: name {name!r} doubles {seen[name]}")
        seen[name] = folder
    return errors


def referenced(path: Path, rel: str, source: Path, texts: dict[Path, str]) -> set[str]:
    """Shared files one file names: by path, and (for a script) by import."""
    text = texts.get(path) or path.read_text()
    found = set(PATH_RE.findall(text))
    if path.suffix == ".py":
        for mod in IMPORT_RE.findall(text):
            if (source / "scripts" / f"{mod}.py").exists():
                found.add(f"scripts/{mod}.py")
    return found


def skill_files(skill: Path) -> list[Path]:
    return [p for p in sorted(skill.rglob("*")) if p.is_file() and not (SKIP_DIRS & set(p.relative_to(skill).parts))]


def dependencies(skill: Path, source: Path, texts: dict[Path, str]) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    deps: set[str] = set()
    queue = [(p, str(p.relative_to(skill))) for p in skill_files(skill) if p.suffix in (".md", ".py", ".sh")]
    visited: set[str] = set()
    while queue:
        path, label = queue.pop()
        for rel in sorted(referenced(path, label, source, texts)):
            if (skill.name, rel) in EXCEPTIONS:
                continue
            if not (source / rel).is_file():
                errors.append(f"skill {skill.name}: {label} names {rel}, which does not exist")
                continue
            if rel in deps or rel in visited:
                continue
            deps.add(rel)
            visited.add(rel)
            queue.append((source / rel, rel))
    return deps, errors


def frontmatter_description(skill_md: Path) -> str:
    m = re.search(r"^description:\s*(.+)$", skill_md.read_text().split("\n---", 1)[0], re.M)
    if not m:
        raise BuildError(f"{skill_md}: no one-line description: in the frontmatter")
    return m.group(1).strip()


def opencode_text(name: str, text: str) -> str:
    """The skill text for OpenCode: no Claude namespace, plus the harness notes where the skill needs them."""
    text = NAMESPACE_RE.sub("", text)
    notes = HARNESS_NOTES.get(name)
    if notes:
        text = text.rstrip("\n") + "\n\n## Harness notes (OpenCode)\n\n" + "\n".join(f"- {n}" for n in notes) + "\n"
    return text


def command_wrapper(name: str, description: str) -> str:
    return f"---\ndescription: {json.dumps(description, ensure_ascii=False)}\n---\n\nLoad the skill `{name}` with the `skill` tool and follow it. Arguments: $ARGUMENTS\n"


def build(source: Path, out: Path, with_evals: bool, target: str = "claude") -> None:
    errors = check_names(source)
    if errors:
        raise BuildError("\n".join(errors))
    if out.exists():
        if not out.is_dir() or (any(out.iterdir()) and not (out / MARKER).is_file()):
            raise BuildError(f"{out} exists and is not an earlier build output; refusing to delete it")
        shutil.rmtree(out)
    out.mkdir(parents=True)
    plan: dict[str, set[str]] = {}
    texts: dict[Path, str] = {}
    for md in sorted((source / "skills").glob("*/SKILL.md")):
        if target == "opencode":
            texts[md] = opencode_text(md.parent.name, md.read_text())
    for md in sorted((source / "skills").glob("*/SKILL.md")):
        skill = md.parent
        deps, errs = dependencies(skill, source, texts)
        errors += errs
        plan[skill.name] = deps
    if errors:
        shutil.rmtree(out)
        raise BuildError("\n".join(errors))
    for name, deps in plan.items():
        src = source / "skills" / name
        for f in skill_files(src):
            dst = out / "skills" / name / f.relative_to(src)
            dst.parent.mkdir(parents=True, exist_ok=True)
            if f in texts:
                dst.write_text(texts[f])
            else:
                shutil.copy2(f, dst)
        for rel in sorted(deps):
            dst = out / "skills" / name / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            if target == "opencode":
                dst.write_text(NAMESPACE_RE.sub("", (source / rel).read_text()))
                shutil.copymode(source / rel, dst)
            else:
                shutil.copy2(source / rel, dst)
    (out / MARKER).write_text(f"built by tools/build.py, target {target}\n")
    if target == "opencode":
        # apm needs a manifest to take the folder as a package; the name keeps it apart from the Claude plugin
        manifest = json.loads((source / ".claude-plugin" / "plugin.json").read_text())
        manifest["name"] += "-opencode"
        (out / ".claude-plugin").mkdir()
        (out / ".claude-plugin" / "plugin.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        (out / "commands").mkdir()
        for name in plan:
            (out / "commands" / f"{name}.md").write_text(command_wrapper(name, frontmatter_description(source / "skills" / name / "SKILL.md")))
    else:
        (out / ".claude-plugin").mkdir()
        shutil.copy2(source / ".claude-plugin" / "plugin.json", out / ".claude-plugin" / "plugin.json")
    for f in ("LICENSE", "THIRD_PARTY_LICENSES.md"):
        if (source / f).exists():
            shutil.copy2(source / f, out / f)
    if with_evals and target == "claude":
        shutil.copytree(source / "evals", out / "evals", ignore=shutil.ignore_patterns("results", ".pts-eval-project", "__pycache__"))
    for name, deps in plan.items():
        print(f"{name}: {len(deps)} shared file(s)" + (": " + ", ".join(sorted(deps)) if deps else ""))


def diff(a: Path, b: Path) -> list[str]:
    cmp = filecmp.dircmp(a, b)
    problems = [f"only in {a}: {n}" for n in cmp.left_only] + [f"only in {b}: {n}" for n in cmp.right_only]
    problems += [f"differs: {a / n}" for n in cmp.diff_files]
    for sub in cmp.common_dirs:
        problems += diff(a / sub, b / sub)
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", type=Path, default=ROOT)
    ap.add_argument("--target", choices=("claude", "opencode"), default="claude")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--with-evals", action="store_true")
    ap.add_argument("--check", action="store_true", help="compare --out with a fresh build instead of writing it")
    args = ap.parse_args()
    if args.out is None:
        args.out = ROOT / "build" / ("design-the-domain" if args.target == "claude" else "opencode")
    try:
        if args.check:
            with tempfile.TemporaryDirectory() as tmp:
                fresh = Path(tmp) / "fresh"
                build(args.source, fresh, args.with_evals, args.target)
                if not args.out.exists():
                    raise BuildError(f"{args.out} does not exist; build it first")
                problems = diff(fresh, args.out)
            if problems:
                raise BuildError("build output is stale:\n" + "\n".join(problems))
            print("build output matches the source")
        else:
            build(args.source, args.out, args.with_evals, args.target)
    except BuildError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
