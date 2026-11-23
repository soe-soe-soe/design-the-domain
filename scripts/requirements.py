#!/usr/bin/env python3
"""Housekeeping for design-the-domain requirements and planned FRs – deterministic, no model.

Commands (run from the project root, which holds domain-model/config.md):

  requirements.py check    US-0042   base and parallel check of the story's planned FR changes
  requirements.py complete US-0042   merge the story's planned FR changes into the active FRs,
                                    set it done with doneAt and move it out of planned/
  requirements.py cancel   US-0042   drop the story's planned FR changes, set it cancelled and
                                    move it to cancelled/
  requirements.py history  FR-x-NNN  the stories that changed an FR, the latest first
  requirements.py next-fr  <subdomain>  the next free FR id of a subdomain, across active and planned FRs

Exit codes: 0 ok, 1 usage or setup error, 2 conflict (nothing written).
Python 3.9+, standard library only.
"""

from __future__ import annotations

import datetime as _dt
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

CONFIG = Path("domain-model/config.md")
# Any Gherkin dialect: a keyword (letters and spaces) followed by ": S<n>" – the plugin numbers
# scenarios S1, S2, …, so the keyword itself does not matter (‹problem-space-language›).
SCENARIO_RE = re.compile(r"^(\s*)([^\W\d_][^\W\d_ ]*(?: [^\W\d_]+)*):\s*S(\d+)\b")
TAG_LINE_RE = re.compile(r"^\s*@\S")
STORY_TAG_RE = re.compile(r"^@(US-\d+|existing)$")
CHANGE_RE = re.compile(r"^- (US-\d+) · Kind: (new|edit|deletion)(?: · Rule: (changed|unchanged))?\s*$")
OPEN_STATES = ("draft", "ready", "in-progress")


class Conflict(Exception):
    pass


class SetupError(Exception):
    pass


# ---------------------------------------------------------------- config and files


def read_config() -> dict[str, str]:
    if not CONFIG.exists():
        raise SetupError(f"{CONFIG} missing – fill it in first (/design-the-domain:problem-space-initialization does it with you); run from the project root")
    values = {}
    for line in CONFIG.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and cells[0].startswith("`") and cells[0].endswith("`"):
            values[cells[0].strip("`")] = cells[-1].strip("`")
    for key in ("requirements", "problem-space"):
        if key not in values:
            raise SetupError(f"key `{key}` missing in {CONFIG}")
    return values


def find_story(requirements: Path, story: str) -> Path:
    hits = sorted((requirements / "planned").glob(f"{story}-*.md"))
    if not hits:
        raise SetupError(f"{story} not found under {requirements / 'planned'}")
    return hits[0]


def header_fields(text: str) -> dict[str, str]:
    for line in text.splitlines():
        if line.startswith("Status:"):
            return dict(
                (p.split(":", 1)[0].strip(), p.split(":", 1)[1].strip())
                for p in line.split(" · ")
                if ":" in p
            )
    return {}


def set_header_field(text: str, key: str, value: str) -> str:
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith("Status:"):
            end = "\n" if line.endswith("\n") else ""
            parts = line.rstrip("\n").split(" · ")
            for j, p in enumerate(parts):
                if p.split(":", 1)[0].strip() == key:
                    parts[j] = f"{key}: {value}"
                    break
            else:
                parts.append(f"{key}: {value}")
            lines[i] = " · ".join(parts) + end
            return "".join(lines)
    raise SetupError("no header line starting with 'Status:'")


# ---------------------------------------------------------------- FR parsing


@dataclass
class Scenario:
    number: int
    tags: list[str]
    lines: list[str]  # keyword line and body, without trailing blank lines
    indent: str

    def render(self) -> list[str]:
        out = [self.indent + " ".join(self.tags)] if self.tags else []
        return out + self.lines

    @property
    def story_tag(self) -> str | None:
        hits = [t[1:] for t in self.tags if STORY_TAG_RE.match(t)]
        return hits[-1] if hits else None

    @property
    def base(self) -> str | None:
        hits = [t[len("@base-"):] for t in self.tags if t.startswith("@base-")]
        return hits[0] if hits else None


@dataclass
class FrFile:
    path: Path
    before: list[str]  # lines up to and including the gherkin header (fence, language, Feature line)
    scenarios: list[Scenario]
    after: list[str]  # closing fence and everything below
    changes: dict[str, tuple[str, str]] = field(default_factory=dict)  # story -> (kind, rule)

    @classmethod
    def read(cls, path: Path) -> "FrFile":
        lines = path.read_text(encoding="utf-8").splitlines()
        try:
            start = next(i for i, l in enumerate(lines) if l.strip().startswith("```gherkin"))
            end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "```")
        except StopIteration:
            start, end = len(lines), len(lines)
        body = lines[start + 1 : end]
        first = next((i for i, l in enumerate(body) if TAG_LINE_RE.match(l) or SCENARIO_RE.match(l)), len(body))
        scenarios: list[Scenario] = []
        i = first
        while i < len(body):
            tags: list[str] = []
            while i < len(body) and TAG_LINE_RE.match(body[i]):
                tags += body[i].split()
                i += 1
            m = SCENARIO_RE.match(body[i]) if i < len(body) else None
            if not m:
                raise SetupError(f"{path}: tags without a scenario numbered Sn near line {start + 2 + i}")
            block = [body[i]]
            i += 1
            while i < len(body) and not TAG_LINE_RE.match(body[i]) and not SCENARIO_RE.match(body[i]):
                block.append(body[i])
                i += 1
            while block and not block[-1].strip():
                block.pop()
            scenarios.append(Scenario(int(m.group(3)), tags, block, m.group(1)))
        fr = cls(path, lines[: start + 1] + _trim(body[:first]), scenarios, lines[end:])
        for line in section(lines, "Changes"):
            cm = CHANGE_RE.match(line)
            if cm:
                fr.changes[cm.group(1)] = (cm.group(2), cm.group(3) or "unchanged")
        return fr

    def by_number(self) -> dict[int, Scenario]:
        return {s.number: s for s in self.scenarios}

    def of_story(self, story: str) -> list[Scenario]:
        return [s for s in self.scenarios if f"@{story}" in s.tags]

    def text(self) -> str:
        body: list[str] = []
        for s in sorted(self.scenarios, key=lambda s: s.number):
            body += [""] + s.render()
        return "\n".join(self.before + body + self.after) + "\n"


def _trim(lines: list[str]) -> list[str]:
    while lines and not lines[-1].strip():
        lines = lines[:-1]
    return lines


def section(lines: list[str], name: str) -> list[str]:
    out, inside = [], False
    for line in lines:
        if line.startswith("## "):
            inside = line[3:].strip() == name
            continue
        if inside:
            out.append(line)
    return out


def replace_section(text: str, name: str, new_body: list[str] | None) -> str:
    """Replace the body of `## name`; None removes the section."""
    lines = text.rstrip("\n").split("\n")
    out, i, done = [], 0, False
    while i < len(lines):
        if lines[i].startswith("## ") and lines[i][3:].strip() == name and not done:
            i += 1
            while i < len(lines) and not lines[i].startswith("## "):
                i += 1
            if new_body is not None:
                out += [f"## {name}", ""] + _trim(new_body) + [""]
            done = True
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(_trim(out)) + "\n"


def set_status(text: str, status: str) -> str:
    return re.sub(r"(· Status: )\w[\w-]*", rf"\g<1>{status}", text, count=1)


# ---------------------------------------------------------------- planned FRs of a story


def planned_files(problem_space: Path, story: str) -> list[FrFile]:
    files = []
    for path in sorted(problem_space.rglob("planned/FR-*.md")):
        fr = FrFile.read(path)
        if story in fr.changes or fr.of_story(story):
            files.append(fr)
    return files


def active_path(planned: Path) -> Path:
    return planned.parent.parent / planned.name


def check(problem_space: Path, story: str) -> list[str]:
    """Problems that block closing the story; empty when it may close."""
    problems = []
    for fr in planned_files(problem_space, story):
        rel = fr.path.as_posix()
        if story not in fr.changes:
            problems.append(f"{rel}: scenarios tagged @{story} but no line for {story} under ## Changes")
            continue
        kind = fr.changes[story][0]
        active = FrFile.read(active_path(fr.path)) if active_path(fr.path).exists() else None
        if kind != "new" and active is None:
            problems.append(f"{rel}: Kind {kind}, but the active FR {active_path(fr.path).as_posix()} does not exist")
        if kind == "new" and active is not None:
            problems.append(f"{rel}: Kind new, but the active FR already exists")
        lines = fr.path.read_text(encoding="utf-8").splitlines()
        if any(story in l for l in section(lines, "Open") if l.strip()):
            problems.append(f"{rel}: open point of {story} under ## Open")
        current = active.by_number() if active else {}
        for s in fr.of_story(story):
            ref = f"{rel} S{s.number}"
            if "@open" in s.tags:
                problems.append(f"{ref}: tagged @open")
            if s.base is None and s.number in current:
                problems.append(f"{ref}: new scenario, but S{s.number} already exists in the active FR (parallel change)")
            if s.base is not None:
                now = current.get(s.number)
                if now is None:
                    problems.append(f"{ref}: base @{s.base}, but the active FR has no S{s.number}")
                elif now.story_tag != s.base:
                    problems.append(
                        f"{ref}: base @{s.base}, but the active scenario was last changed by @{now.story_tag} (parallel change)"
                    )
            others = [o for o in fr.scenarios if o.number == s.number and o is not s]
            for o in others:
                problems.append(f"{ref}: also changed by @{o.story_tag} in the same planned file (parallel change)")
    return problems


# ---------------------------------------------------------------- commands


def cmd_check(cfg: dict[str, str], story: str) -> int:
    problems = check(Path(cfg["problem-space"]), story)
    if problems:
        print(f"Conflicts {story}:")
        print("\n".join(f"- {p}" for p in problems))
        return 2
    print(f"Check {story}: ok")
    return 0


def merge(fr: FrFile, story: str) -> tuple[Path, str]:
    """Return the active FR's path and its new text."""
    target_path = active_path(fr.path)
    kind, rule = fr.changes[story]
    planned_text = fr.path.read_text(encoding="utf-8")
    if kind == "new":
        target = FrFile.read(fr.path)
        target.scenarios = []
        text = target.text()
        text = replace_section(text, "Changes", None)
        text = replace_section(text, "Open", None)
        target = _reparse(target_path, set_status(text, "valid"))
    else:
        target = FrFile.read(target_path)
    if kind == "deletion":
        for s in target.scenarios:
            s.tags = [t for t in s.tags if not STORY_TAG_RE.match(t)] + [f"@{story}"]
            if "@obsolete" not in s.tags:
                s.tags.append("@obsolete")
        return target_path, set_status(target.text(), "obsolete")
    current = {s.number: i for i, s in enumerate(target.scenarios)}
    for s in fr.of_story(story):
        merged = Scenario(s.number, [t for t in s.tags if t != "@planned" and not t.startswith("@base-")], s.lines, s.indent)
        if s.number in current:
            target.scenarios[current[s.number]] = merged
        else:
            target.scenarios.append(merged)
    text = target.text()
    if rule == "changed":
        text = replace_section(text, "Rule", section(planned_text.splitlines(), "Rule"))
    return target_path, text


def _reparse(path: Path, text: str) -> FrFile:
    tmp = path.with_name(path.name + ".tmp")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(text, encoding="utf-8")
    try:
        fr = FrFile.read(tmp)
    finally:
        tmp.unlink()
    fr.path = path
    return fr


def strip_story(fr: FrFile, story: str) -> str | None:
    """The planned file without the story's changes; None when nothing is left."""
    del fr.changes[story]
    if not fr.changes:
        return None
    fr.scenarios = [s for s in fr.scenarios if f"@{story}" not in s.tags]
    text = fr.text()
    lines = text.splitlines()
    changes = [l for l in section(lines, "Changes") if not l.startswith(f"- {story} ")]
    text = replace_section(text, "Changes", changes)
    open_lines = [l for l in section(lines, "Open") if story not in l]
    text = replace_section(text, "Open", open_lines if any(l.strip() for l in open_lines) else None)
    if all(rule != "changed" for _, rule in fr.changes.values()):
        text = replace_section(text, "Rule", None)
    return text


def write_all(writes: dict[Path, str | None], moves: list[tuple[Path, Path, str]]) -> None:
    for path, text in writes.items():
        if text is None:
            path.unlink()
            if path.parent.name == "planned" and not any(path.parent.iterdir()):
                path.parent.rmdir()
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    for src, dst, text in moves:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8")
        src.unlink()


def cmd_complete(cfg: dict[str, str], story: str, today: str) -> int:
    requirements, problem_space = Path(cfg["requirements"]), Path(cfg["problem-space"])
    story_path = find_story(requirements, story)
    story_text = story_path.read_text(encoding="utf-8")
    status = header_fields(story_text).get("Status")
    if status != "in-progress":
        print(f"{story} has status {status}; only an in-progress story can be completed")
        return 2
    problems = check(problem_space, story)
    if problems:
        print(f"Conflicts {story} – nothing written:")
        print("\n".join(f"- {p}" for p in problems))
        return 2
    writes: dict[Path, str | None] = {}
    merged = []
    for fr in planned_files(problem_space, story):
        target, text = merge(fr, story)
        writes[target] = text
        writes[fr.path] = strip_story(FrFile.read(fr.path), story)
        merged.append(f"{target.as_posix()} ({fr.changes[story][0]})")
    story_text = set_header_field(set_header_field(story_text, "Status", "done"), "doneAt", today)
    write_all(writes, [(story_path, requirements / story_path.name, story_text)])
    print(f"Completed {story}: {requirements / story_path.name}")
    print("\n".join(f"- {m}" for m in merged) or "- no planned FR changes")
    return 0


def cmd_cancel(cfg: dict[str, str], story: str) -> int:
    requirements, problem_space = Path(cfg["requirements"]), Path(cfg["problem-space"])
    story_path = find_story(requirements, story)
    story_text = story_path.read_text(encoding="utf-8")
    status = header_fields(story_text).get("Status")
    if status not in OPEN_STATES:
        print(f"{story} has status {status}; only {', '.join(OPEN_STATES)} can be cancelled")
        return 2
    writes: dict[Path, str | None] = {}
    for fr in planned_files(problem_space, story):
        fr.changes.setdefault(story, ("edit", "unchanged"))
        writes[fr.path] = strip_story(fr, story)
    story_text = set_header_field(story_text, "Status", "cancelled")
    write_all(writes, [(story_path, requirements / "cancelled" / story_path.name, story_text)])
    print(f"Cancelled {story}: {requirements / 'cancelled' / story_path.name}")
    print("\n".join(f"- {p.as_posix()} ({'deleted' if t is None else 'changes removed'})" for p, t in writes.items()))
    return 0


def cmd_history(cfg: dict[str, str], fr_id: str) -> int:
    requirements, problem_space = Path(cfg["requirements"]), Path(cfg["problem-space"])
    entries = []
    for path in requirements.glob("US-*.md"):
        lines = path.read_text(encoding="utf-8").splitlines()
        refs = [l.strip() for l in section(lines, "Functional requirements") if fr_id in l]
        if refs:
            head = header_fields("\n".join(lines))
            entries.append((head.get("doneAt", ""), lines[0].lstrip("# ").strip(), refs))
    print(f"History {fr_id} (latest first):")
    for done_at, title, refs in sorted(entries, reverse=True):
        print(f"- {done_at} {title}")
        for r in refs:
            print(f"  {r}")
    active = [p for p in problem_space.rglob(f"{fr_id}-*.md") if p.parent.name != "planned"]
    if active and "@existing" in active[0].read_text(encoding="utf-8"):
        print("- existing: taken over from code (problem-space-initialization)")
    if not entries and not active:
        print("- none")
    return 0


def cmd_next_fr(cfg: dict[str, str], subdomain: str) -> int:
    """Highest number across the active and planned FR files of the subdomain, plus one."""
    base = Path(cfg["problem-space"]) / subdomain
    pattern = re.compile(rf"^FR-{re.escape(subdomain)}-(\d+)-")
    numbers = [int(m.group(1)) for p in base.rglob("FR-*.md") if (m := pattern.match(p.name))]
    print(f"FR-{subdomain}-{max(numbers, default=0) + 1:03d}")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) != 3 or argv[1] not in ("check", "complete", "cancel", "history", "next-fr"):
        print(__doc__)
        return 1
    try:
        cfg = read_config()
        if argv[1] == "check":
            return cmd_check(cfg, argv[2])
        if argv[1] == "complete":
            return cmd_complete(cfg, argv[2], _dt.date.today().isoformat())
        if argv[1] == "cancel":
            return cmd_cancel(cfg, argv[2])
        if argv[1] == "next-fr":
            return cmd_next_fr(cfg, argv[2])
        return cmd_history(cfg, argv[2])
    except SetupError as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
