#!/usr/bin/env python3
"""Renders one round of domain-grilling – deterministic numbering, grouping and references.

  interview-round.py <round.json>      (or the JSON on stdin)

The model decides the content of its own questions; this script adds the open points of the
writers from the files, numbers every question, groups them by story and puts the artifact a
question rests on after its title. Input (keys in English, texts in the session's language):

  {
    "start": 5,                       first question number of this round
    "group": true,                    false for round 1 (no story headings)
    "closing": false,                 true: also ask the open points of the stories
    "stories": ["US-0050", "US-0051"],the session's stories, in heading order
    "deferred": ["US-0051/AC2"],      open points the user deferred – never asked again
    "crosscutting": "Cross-cutting",  heading for questions without a story, in the problem-space language
    "headings": {"fristen": "🧭 Fristen"},
                                      optional, instead of "stories": group by subdomain (or any key)
                                      with these headings, in this order; each question names its
                                      group in "group" (domain-init has no stories)
    "questions": [                    the model's own questions
      {"title": "…", "body": "…", "recommendation": "…",
       "story": "US-0050",            optional; without it the question is cross-cutting
       "ref": "FR-deadlines-006/S9", optional: artifact the question rests on
       "same_as": "FR-deadlines-013/S2" optional: the open point this question also asks}
    ]
  }

Output: the round as Markdown on stdout, nothing else; the next question number on stderr
(`next question number: N`). Exit 1 on a setup error.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from requirements import SetupError, read_config, section  # noqa: E402

OPEN_RE = re.compile(r"^- \*\*((?:AC|S)\d+)\*\* \(([^)]+)\): (.*?) – Recommendation: (.*?)(?: – (.*))?$")
TITLE_RE = re.compile(r"^\s*(?:Szenariogrundriss|Szenario|Scenario Outline|Scenario):\s*((?:AC|S)\d+)\s*–\s*(.*)$")


def icon(ref: str) -> str:
    """The reference with the icon of its artifact type (assets/output-format.md)."""
    if not ref or not ref[0].isascii():
        return ref  # already carries an icon
    if ref.startswith("FR-"):
        return f"📋 {ref}"
    if ref.startswith("US-"):
        return f"📘 {ref}"
    if "glossar" in ref or re.match(r"^[\w-]+\.md: ", ref):
        return f"📄 {ref}"
    if "refactoring" in ref:
        return f"📘 {ref}"
    return f"📄 {ref}"


def fields(rest: str | None) -> dict[str, str]:
    out = {}
    for part in (rest or "").split(" · "):
        if ": " in part:
            k, v = part.split(": ", 1)
            out[k.strip()] = v.strip()
    return out


def titles(lines: list[str]) -> dict[str, str]:
    return {m.group(1): m.group(2).strip() for m in (TITLE_RE.match(l) for l in lines) if m}


def open_points(cfg: dict[str, str], stories: list[str], closing: bool, deferred: set[str]) -> list[dict]:
    """Open points of the session: FR points always, story points only in the closing round."""
    points = []
    planned = Path(cfg["problem-space"])
    for path in sorted(planned.rglob("planned/FR-*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        fr_id = "-".join(path.name.split("-")[:3])
        names = titles(lines)
        for line in section(lines, "Open"):
            m = OPEN_RE.match(line.strip())
            if not m:
                continue
            f = fields(m.group(5))
            ref = f"{fr_id}/{m.group(1)}"
            if f.get("Story") not in stories or ref in deferred:
                continue
            points.append({
                "ref": ref, "source": m.group(2), "question": m.group(3), "recommendation": m.group(4),
                "story": f.get("Story"), "type": f.get("Type"), "glossary": f.get("Glossary"),
                "title": names.get(m.group(1), ref),
            })
    if closing:
        for story in stories:
            for path in sorted((Path(cfg["requirements"]) / "planned").glob(f"{story}-*.md")):
                lines = path.read_text(encoding="utf-8").splitlines()
                names = titles(lines)
                for line in section(lines, "Open"):
                    m = OPEN_RE.match(line.strip())
                    ref = f"{story}/{m.group(1)}" if m else ""
                    if not m or ref in deferred:
                        continue
                    points.append({
                        "ref": ref, "source": m.group(2), "question": m.group(3),
                        "recommendation": m.group(4), "story": story, "type": None, "glossary": None,
                        "title": names.get(m.group(1), ref),
                    })
    return points


def story_title(cfg: dict[str, str], story: str) -> str:
    for path in (Path(cfg["requirements"]) / "planned").glob(f"{story}-*.md"):
        first = path.read_text(encoding="utf-8").splitlines()[0]
        return first.split(":", 1)[1].strip() if ":" in first else first.lstrip("# ")
    return story


def references(refs: list[str | None]) -> str:
    """The artifacts a question rests on, with their icons, after the title: ` (📋 FR-…/S2)`."""
    shown = [icon(r) for r in refs if r]
    return f" ({', '.join(shown)})" if shown else ""


def render(data: dict, cfg: dict[str, str]) -> str:
    headings = data.get("headings") or {}
    stories = list(headings) if headings else list(data.get("stories", []))
    deferred = set(data.get("deferred", []))
    points = open_points(cfg, [] if headings else stories, bool(data.get("closing")), deferred)
    by_ref = {p["ref"]: p for p in points}
    items = []  # (story or None, title, body, recommendation, references)
    for q in data.get("questions", []):
        same = by_ref.pop(q["same_as"], None) if q.get("same_as") else None
        if same:
            refs = references([same["ref"], same.get("glossary")])
            story = q.get("story") or q.get("group") or same.get("story")
        else:
            refs = references([q.get("ref")])
            story = q.get("story") or q.get("group")
        items.append((story, q["title"], q["body"], q["recommendation"], refs))
    for p in by_ref.values():
        items.append((p["story"], p["title"], p["question"], p["recommendation"], references([p["ref"], p.get("glossary")])))

    group = bool(data.get("group", True))
    order = stories + [None] if group else [None]
    out, n = [], int(data.get("start", 1))
    for key in order:
        block = [i for i in items if (i[0] == key if group else True)]
        if group:
            block = [i for i in items if (i[0] if i[0] in stories else None) == key]
        if not block:
            continue
        if group:
            if key and headings:
                out.append(f"### {headings[key]}")
            else:
                out.append(f"### 📘 {key}: {story_title(cfg, key)}" if key else f"### 🌐 {data.get('crosscutting', 'Cross-cutting')}")
            out.append("")
        for k, (_, title, body, rec, refs) in enumerate(block):
            if k:
                out += ["---", ""]
            out += [f"❓ **Q{n}** - **{title}**{refs}: {body}", "", f"➡️ {rec}", ""]
            n += 1
    print(f"next question number: {n}", file=sys.stderr)
    return "\n".join(out).rstrip() + "\n"


def main(argv: list[str]) -> int:
    try:
        raw = Path(argv[1]).read_text(encoding="utf-8") if len(argv) > 1 else sys.stdin.read()
        data = json.loads(raw)
        print(render(data, read_config()), end="")
        return 0
    except (SetupError, json.JSONDecodeError, KeyError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
