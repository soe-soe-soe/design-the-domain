#!/usr/bin/env python3
"""Builds a Confluence page tree from the problem space – deterministic, no model, no network.

Run from the project root, which holds domain-model/config.md:

  confluence_publish.py build [--out DIR] [--diagram-format svg|png] [--no-render]

Reads the domain map, the subdomain maps, the glossaries and the active FRs, and writes into DIR
(default build/confluence):

  manifest.json         the pages in creation order (parents first), see below
  pages/NNN-*.html      one page body each, Confluence storage format
  attachments/*.svg     the diagrams, rendered from Mermaid with mmdc (env MMDC overrides the command)

The manifest is what a Confluence connector (or any client) syncs; this script never talks to
Confluence. The page tree:

  Domain Map                       domain map: diagram of the subdomains, tables
  └─ <Subdomain>                   subdomain map diagram, business objects, relationships
     ├─ <Subdomain> – Glossary     the glossary
     └─ <Subdomain> / <Object>     one page per business object: its FRs as a table
        └─ FR-x-NNN: <title>       one page per active FR (planned FR changes are not published)

Without mmdc (or with --no-render) a diagram goes into the page as a Mermaid code block and the
build says so. Exit codes: 0 ok (warnings possible), 1 usage or setup error.
Python 3.9+, standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

CONFIG = Path("domain-model/config.md")
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
FR_FILE_RE = re.compile(r"^FR-[a-z0-9-]+-\d+.*\.md$")
UMLAUTS = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "Ä": "ae", "Ö": "oe", "Ü": "ue"})


class SetupError(Exception):
    pass


# ---------------------------------------------------------------- small helpers


def slug(text: str) -> str:
    s = text.translate(UMLAUTS).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def attr(text: str) -> str:
    return html.escape(text, quote=True)


def posix(path: Path) -> str:
    return Path(os.path.normpath(path)).as_posix()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_config() -> dict[str, str]:
    if not CONFIG.exists():
        raise SetupError(f"{CONFIG} missing – fill it in first (/design-the-domain:domain-init does it with you); run from the project root")
    values: dict[str, str] = {}
    for line in CONFIG.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and cells[0].startswith("`") and cells[0].endswith("`"):
            values[cells[0].strip("`")] = cells[-1].strip("`")
    for key in ("problem-space", "domain-map"):
        if key not in values:
            raise SetupError(f"key `{key}` missing in {CONFIG}")
    return values


def optional(values: dict[str, str], key: str) -> str | None:
    v = values.get(key, "").strip()
    if not v or v in ("–", "-") or (v.startswith("<") and v.endswith(">")):
        return None
    return v


# ---------------------------------------------------------------- markdown reading


def split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", s)]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c) for c in cells)


def strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->\s*", "", text, flags=re.S)


def split_sections(text: str, level: int = 2) -> tuple[list[str], list[tuple[str, list[str]]]]:
    """Lines before the first heading of `level`, then (heading, lines) per heading of that level."""
    marker = "#" * level + " "
    pre: list[str] = []
    sections: list[tuple[str, list[str]]] = []
    in_code = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if not in_code and line.startswith(marker):
            sections.append((line[len(marker):].strip(), []))
        elif sections:
            sections[-1][1].append(line)
        else:
            pre.append(line)
    return pre, sections


def table_rows(lines: list[str]) -> list[dict[str, str]]:
    """The first table of the lines as one dict per row, keyed by the lower-cased header cells."""
    rows: list[list[str]] = []
    for line in lines:
        if line.strip().startswith("|"):
            rows.append(split_row(line))
        elif rows:
            break
    if len(rows) < 2 or not is_separator(rows[1]):
        return []
    head = [h.lower() for h in rows[0]]
    return [dict(zip(head, r)) for r in rows[2:]]


def mermaid_of(path: Path) -> str | None:
    m = re.search(r"```mermaid\n(.*?)```", path.read_text(encoding="utf-8"), flags=re.S)
    return m.group(1).strip("\n") if m else None


# ---------------------------------------------------------------- the model


@dataclass
class Fr:
    path: Path
    id: str
    title: str
    type: str
    status: str
    bo_slug: str | None
    rule: str


@dataclass
class BusinessObject:
    slug: str
    name: str
    description: str
    dir: Path
    frs: list[Fr] = field(default_factory=list)


@dataclass
class Subdomain:
    name: str
    slug: str
    type: str
    description: str
    dir: Path | None
    glossary: Path | None
    map_file: Path | None
    objects: list[BusinessObject] = field(default_factory=list)
    direct_frs: list[Fr] = field(default_factory=list)


@dataclass
class Relationship:
    source: str
    target: str
    description: str


def parse_fr(path: Path, bo_slug: str | None) -> Fr:
    lines = path.read_text(encoding="utf-8").splitlines()
    title = next((ln[2:].strip() for ln in lines if ln.startswith("# ")), path.stem)
    fields: dict[str, str] = {}
    for ln in lines:
        if " · " in ln and ":" in ln and not ln.startswith("#"):
            for part in ln.split(" · "):
                k, _, v = part.partition(":")
                fields[k.strip().lower()] = v.strip()
            break
    _, sections = split_sections("\n".join(lines))
    rule = ""
    for heading, body in sections:
        if heading.lower() == "rule":
            para = " ".join(x.strip() for x in "\n".join(body).strip().split("\n\n")[0].splitlines())
            rule = para if len(para) <= 200 else para[:197].rstrip() + "…"
    return Fr(path, title.split(":")[0].strip(), title, fields.get("type", ""), fields.get("status", ""), bo_slug, rule)


def read_model(cfg: dict[str, str], warnings: list[str]) -> tuple[Path, str, list[Subdomain], list[Relationship]]:
    map_path = Path(cfg["domain-map"])
    if not map_path.exists():
        raise SetupError(f"domain map {map_path} missing")
    text = strip_comments(map_path.read_text(encoding="utf-8"))
    pre, sections = split_sections(text)
    intro = "\n".join(ln for ln in pre if not ln.startswith("# ")).strip()
    by_heading = {h.lower(): body for h, body in sections}
    subdomains: list[Subdomain] = []
    for row in table_rows(by_heading.get("subdomains", [])):
        name = row.get("subdomain", "").strip()
        if not name or name.startswith("<"):
            continue
        glossary_link = LINK_RE.search(row.get("glossary", ""))
        map_link = LINK_RE.search(row.get("subdomain map", ""))
        glossary = Path(os.path.normpath(map_path.parent / glossary_link.group(2))) if glossary_link else None
        map_file = Path(os.path.normpath(map_path.parent / map_link.group(2))) if map_link else None
        sub_dir = map_file.parent if map_file else map_path.parent / slug(name)
        if not sub_dir.is_dir():
            warnings.append(f"subdomain {name}: folder {sub_dir.as_posix()} not found, no FRs published")
            sub_dir = None
        if glossary and not glossary.exists():
            warnings.append(f"subdomain {name}: glossary {glossary.as_posix()} not found")
            glossary = None
        if map_file and not map_file.exists():
            warnings.append(f"subdomain {name}: subdomain map {map_file.as_posix()} not found")
            map_file = None
        subdomains.append(Subdomain(name, slug(name), row.get("type", ""), row.get("description", ""), sub_dir, glossary, map_file))
    relationships = [
        Relationship(r.get("from", ""), r.get("to", ""), r.get("description", ""))
        for r in table_rows(by_heading.get("relationships", []))
        if r.get("from") and not r["from"].startswith("<")
    ]
    for sub in subdomains:
        read_subdomain(sub, warnings)
    return map_path, intro, subdomains, relationships


def read_subdomain(sub: Subdomain, warnings: list[str]) -> None:
    objects: dict[str, BusinessObject] = {}
    descriptions: dict[str, tuple[str, str]] = {}
    if sub.glossary:
        _, sections = split_sections(sub.glossary.read_text(encoding="utf-8"))
        for heading, body in sections:
            row = next((r for r in table_rows(body) if r.get("problem space", "").lower() == "business object"), None)
            if row:
                descriptions[slug(heading)] = (heading, row.get("description", ""))
    if not sub.dir:
        return
    for path in sorted(sub.dir.rglob("*.md")):
        rel = path.relative_to(sub.dir)
        if "planned" in rel.parts or not FR_FILE_RE.match(path.name):
            continue
        bo_slug = rel.parts[0] if len(rel.parts) > 1 else None
        fr = parse_fr(path, bo_slug)
        if bo_slug is None:
            sub.direct_frs.append(fr)
            continue
        if bo_slug not in objects:
            name, desc = descriptions.get(bo_slug, (bo_slug.replace("-", " ").title(), ""))
            if bo_slug not in descriptions:
                warnings.append(f"{sub.name}: business object folder {bo_slug} has no section in the glossary, named from the folder")
            objects[bo_slug] = BusinessObject(bo_slug, name, desc, sub.dir / bo_slug)
        objects[bo_slug].frs.append(fr)
    for bo in objects.values():
        bo.frs.sort(key=lambda f: f.id)
    sub.direct_frs.sort(key=lambda f: f.id)
    sub.objects = sorted(objects.values(), key=lambda b: b.name)


# ---------------------------------------------------------------- markdown → storage format


class Ctx:
    """Link targets (source path → page title) and the warnings of one build."""

    def __init__(self, warnings: list[str]):
        self.titles: dict[str, str] = {}
        self.warnings = warnings

    def resolve(self, src: Path, href: str) -> str | None:
        path = href.split("#")[0]
        if not path:
            return None
        key = posix(src.parent / path)
        if key in self.titles:
            return self.titles[key]
        self.warnings.append(f"{src.as_posix()}: link {href} points to no published page, written as plain text")
        return None


def page_link(title: str, label: str) -> str:
    return (
        f'<ac:link><ri:page ri:content-title="{attr(title)}" />'
        f"<ac:plain-text-link-body><![CDATA[{label}]]></ac:plain-text-link-body></ac:link>"
    )


def emphasis(text: str) -> str:
    t = esc(text)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)


def inline(text: str, ctx: Ctx, src: Path) -> str:
    out: list[str] = []
    for i, part in enumerate(re.split(r"(`[^`]+`)", text)):
        if i % 2 == 1:
            out.append(f"<code>{esc(part[1:-1])}</code>")
            continue
        pos = 0
        for m in LINK_RE.finditer(part):
            out.append(emphasis(part[pos:m.start()]))
            label, href = m.group(1), m.group(2)
            if re.match(r"(https?://|mailto:)", href):
                out.append(f'<a href="{attr(href)}">{esc(label)}</a>')
            else:
                target = ctx.resolve(src, href)
                out.append(page_link(target, label) if target else esc(label))
            pos = m.end()
        out.append(emphasis(part[pos:]))
    return "".join(out)


def code_macro(code: str, title: str | None = None) -> str:
    code = code.replace("]]>", "]]]]><![CDATA[>")
    t = f'<ac:parameter ac:name="title">{esc(title)}</ac:parameter>' if title else ""
    return f'<ac:structured-macro ac:name="code">{t}<ac:plain-text-body><![CDATA[{code}]]></ac:plain-text-body></ac:structured-macro>'


def table_html(rows: list[list[str]]) -> str:
    """rows[0] is the header; cells are ready HTML."""
    head = "".join(f"<th>{c}</th>" for c in rows[0])
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows[1:])
    return f"<table><tbody><tr>{head}</tr>{body}</tbody></table>"


def md_to_storage(text: str, src: Path, ctx: Ctx, skip_h1: bool = True) -> str:
    lines = strip_comments(text).splitlines()
    out: list[str] = []
    para: list[str] = []
    i = 0

    def flush() -> None:
        if para:
            out.append(f"<p>{inline(' '.join(para), ctx, src)}</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush()
            i += 1
            code: list[str] = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            out.append(code_macro("\n".join(code)))
        elif re.match(r"#{1,6} ", line):
            flush()
            level = len(line) - len(line.lstrip("#"))
            if not (skip_h1 and level == 1):
                out.append(f"<h{level}>{inline(line[level:].strip(), ctx, src)}</h{level}>")
        elif line.strip().startswith("|"):
            flush()
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = split_row(lines[i])
                if not is_separator(cells):
                    rows.append([inline(c, ctx, src) for c in cells])
                i += 1
            i -= 1
            if rows:
                out.append(table_html(rows))
        elif re.match(r"\s*([-*]|\d+\.) ", line):
            flush()
            ordered = bool(re.match(r"\s*\d+\. ", line))
            items: list[str] = []
            while i < len(lines) and re.match(r"\s*([-*]|\d+\.) ", lines[i]):
                items.append(re.sub(r"^\s*([-*]|\d+\.) ", "", lines[i]))
                i += 1
            i -= 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(it, ctx, src)}</li>" for it in items) + f"</{tag}>")
        elif not line.strip():
            flush()
        else:
            para.append(line.strip())
        i += 1
    flush()
    return "\n".join(out)


# ---------------------------------------------------------------- diagrams


def domain_map_mermaid(subdomains: list[Subdomain], relationships: list[Relationship], warnings: list[str]) -> str:
    ids = {s.name: f"n{i}" for i, s in enumerate(subdomains)}
    out = ["flowchart LR"]
    for s in subdomains:
        label = s.name.replace('"', "'") + (f"<br/>{s.type}" if s.type else "")
        cls = slug(s.type) if slug(s.type) in ("core", "supporting", "generic") else "open"
        out.append(f'    {ids[s.name]}["{label}"]:::{cls}')
    for n, r in enumerate(relationships, 1):
        if r.source in ids and r.target in ids:
            out.append(f"    {ids[r.source]} -->|{n}| {ids[r.target]}")
        else:
            warnings.append(f"domain map: relationship {n} ({r.source} → {r.target}) names a subdomain that is not in the table, left out of the diagram")
    out += [
        "    classDef core fill:#d6e4ff,stroke:#2f54eb,color:#10239e",
        "    classDef supporting fill:#d9f7be,stroke:#389e0d,color:#135200",
        "    classDef generic fill:#f0f0f0,stroke:#8c8c8c,color:#262626",
        "    classDef open fill:#fff7e6,stroke:#d48806,color:#873800",
    ]
    return "\n".join(out)


class Renderer:
    def __init__(self, out: Path, fmt: str, enabled: bool, warnings: list[str]):
        self.out, self.fmt, self.enabled, self.warnings = out, fmt, enabled, warnings
        self.cmd = shlex.split(os.environ.get("MMDC", "mmdc"))
        self.available = enabled and shutil.which(self.cmd[0]) is not None
        if enabled and not self.available:
            warnings.append(f"{self.cmd[0]} not found: diagrams are published as Mermaid code blocks (install @mermaid-js/mermaid-cli or set MMDC)")

    def render(self, name: str, source: str) -> Path | None:
        if not self.available:
            return None
        att = self.out / "attachments"
        att.mkdir(parents=True, exist_ok=True)
        src, dst = att / f"{name}.mmd", att / f"{name}.{self.fmt}"
        src.write_text(source + "\n", encoding="utf-8")
        try:
            subprocess.run(self.cmd + ["-i", str(src), "-o", str(dst), "-b", "transparent"], check=True, capture_output=True, text=True, timeout=120)
        except (subprocess.SubprocessError, OSError) as e:
            detail = getattr(e, "stderr", "") or str(e)
            self.warnings.append(f"diagram {name}: rendering failed ({detail.strip().splitlines()[-1] if detail.strip() else e}), published as a Mermaid code block")
            return None
        finally:
            src.unlink(missing_ok=True)
        return dst if dst.exists() else None


def diagram_block(r: Renderer, name: str, source: str, alt: str, attachments: list[Path]) -> str:
    image = r.render(name, source)
    if image is None:
        return code_macro(source, f"{alt} (Mermaid)")
    attachments.append(image)
    return (
        f'<p><ac:image ac:alt="{attr(alt)}"><ri:attachment ri:filename="{attr(image.name)}" /></ac:image></p>'
        f'<ac:structured-macro ac:name="expand"><ac:parameter ac:name="title">Mermaid source</ac:parameter>'
        f"<ac:rich-text-body>{code_macro(source)}</ac:rich-text-body></ac:structured-macro>"
    )


# ---------------------------------------------------------------- pages


@dataclass
class Page:
    key: str
    title: str
    parent: str | None
    kind: str
    labels: list[str]
    body: str = ""
    attachments: list[Path] = field(default_factory=list)


def plan_pages(prefix: str, map_path: Path, subdomains: list[Subdomain], ctx: Ctx) -> list[Page]:
    """Keys, titles, parents and labels of all pages, parents first; link targets go into ctx."""
    pages: list[Page] = []
    root = Page(posix(map_path), f"{prefix}Domain Map", None, "domain-map", ["dtd", "dtd-domain-map"])
    pages.append(root)
    ctx.titles[root.key] = root.title
    for sub in subdomains:
        key = posix(sub.dir) if sub.dir else f"subdomain:{sub.slug}"
        sp = Page(key, f"{prefix}{sub.name}", root.key, "subdomain", ["dtd", "dtd-subdomain", f"sd-{sub.slug}"])
        pages.append(sp)
        ctx.titles[key] = sp.title
        if sub.map_file:
            ctx.titles[posix(sub.map_file)] = sp.title
        if sub.glossary:
            gp = Page(posix(sub.glossary), f"{prefix}{sub.name} – Glossary", sp.key, "glossary", ["dtd", "dtd-glossary", f"sd-{sub.slug}"])
            pages.append(gp)
            ctx.titles[gp.key] = gp.title
        for fr in sub.direct_frs:
            add_fr(pages, ctx, prefix, sub, None, fr, sp.key)
        for bo in sub.objects:
            bp = Page(posix(bo.dir), f"{prefix}{sub.name} / {bo.name}", sp.key, "business-object", ["dtd", "dtd-business-object", f"sd-{sub.slug}", f"bo-{sub.slug}-{bo.slug}"])
            pages.append(bp)
            ctx.titles[bp.key] = bp.title
            for fr in bo.frs:
                add_fr(pages, ctx, prefix, sub, bo, fr, bp.key)
    titles = [p.title for p in pages]
    for t in {t for t in titles if titles.count(t) > 1}:
        ctx.warnings.append(f"page title '{t}' occurs twice – titles are unique per Confluence space; set confluence-title-prefix or rename")
    return pages


def add_fr(pages: list[Page], ctx: Ctx, prefix: str, sub: Subdomain, bo: BusinessObject | None, fr: Fr, parent: str) -> None:
    labels = ["dtd", "dtd-fr", f"sd-{sub.slug}", fr.id.lower()]
    if bo:
        labels.append(f"bo-{sub.slug}-{bo.slug}")
    if fr.status:
        labels.append(f"status-{slug(fr.status)}")
    page = Page(posix(fr.path), f"{prefix}{fr.title}", parent, "fr", labels)
    pages.append(page)
    ctx.titles[page.key] = page.title


def fill_bodies(pages: list[Page], map_path: Path, intro: str, subdomains: list[Subdomain], relationships: list[Relationship], ctx: Ctx, renderer: Renderer) -> None:
    by_key = {p.key: p for p in pages}
    root = pages[0]
    sub_title = {s.name: ctx.titles[posix(s.dir) if s.dir else f"subdomain:{s.slug}"] for s in subdomains}

    # domain map
    parts = [md_to_storage(intro, map_path, ctx)] if intro else []
    parts.append("<h2>Subdomain overview</h2>")
    parts.append(diagram_block(renderer, "domain-map", domain_map_mermaid(subdomains, relationships, ctx.warnings), "Domain map", root.attachments))
    parts.append("<h2>Subdomains</h2>")
    rows = [["Subdomain", "Type", "Glossary", "Description"]]
    for s in subdomains:
        gl = page_link(ctx.titles[posix(s.glossary)], "Glossary") if s.glossary else "–"
        rows.append([page_link(sub_title[s.name], s.name), esc(s.type), gl, inline(s.description, ctx, map_path)])
    parts.append(table_html(rows))
    if relationships:
        parts.append("<h2>Relationships</h2>")
        rows = [["#", "From", "To", "Description"]]
        for n, r in enumerate(relationships, 1):
            rows.append([str(n)] + [page_link(sub_title[x], x) if x in sub_title else esc(x) for x in (r.source, r.target)] + [inline(r.description, ctx, map_path)])
        parts.append(table_html(rows))
    root.body = "\n".join(parts)

    for s in subdomains:
        sp = by_key[posix(s.dir) if s.dir else f"subdomain:{s.slug}"]
        parts = [f"<p>{inline(s.description, ctx, map_path)}</p>"] if s.description else []
        if s.type:
            parts.append(f"<p><strong>Type:</strong> {esc(s.type)}</p>")
        if s.glossary:
            parts.append(f"<p>{page_link(ctx.titles[posix(s.glossary)], 'Glossary')} of this subdomain.</p>")
        if s.map_file:
            source = mermaid_of(s.map_file)
            parts.append("<h2>Subdomain map</h2>")
            if source:
                parts.append(diagram_block(renderer, f"{s.slug}-subdomain-map", source, f"{s.name} – subdomain map", sp.attachments))
            else:
                ctx.warnings.append(f"{s.map_file.as_posix()}: no mermaid block found")
        if s.objects:
            parts.append("<h2>Business objects</h2>")
            rows = [["Business object", "Description", "FRs"]]
            for bo in s.objects:
                rows.append([page_link(ctx.titles[posix(bo.dir)], bo.name), inline(bo.description, ctx, map_path), str(len(bo.frs))])
            parts.append(table_html(rows))
        if s.direct_frs:
            parts.append("<h2>Functional requirements</h2>" + fr_table(s.direct_frs, ctx))
        related = [r for r in relationships if s.name in (r.source, r.target)]
        if related:
            parts.append("<h2>Relationships to other subdomains</h2>")
            rows = [["From", "To", "Description"]]
            for r in related:
                rows.append([page_link(sub_title[x], x) if x in sub_title else esc(x) for x in (r.source, r.target)] + [inline(r.description, ctx, map_path)])
            parts.append(table_html(rows))
        sp.body = "\n".join(parts)
        if s.glossary:
            by_key[posix(s.glossary)].body = md_to_storage(s.glossary.read_text(encoding="utf-8"), s.glossary, ctx)
        for bo in s.objects:
            bp = by_key[posix(bo.dir)]
            parts = [f"<p>{inline(bo.description, ctx, map_path)}</p>"] if bo.description else []
            parts.append("<h2>Functional requirements</h2>" + fr_table(bo.frs, ctx))
            bp.body = "\n".join(parts)
        for fr in s.direct_frs + [f for bo in s.objects for f in bo.frs]:
            by_key[posix(fr.path)].body = md_to_storage(fr.path.read_text(encoding="utf-8"), fr.path, ctx)


def fr_table(frs: list[Fr], ctx: Ctx) -> str:
    rows = [["FR", "Type", "Status", "Rule"]]
    for fr in frs:
        rows.append([page_link(ctx.titles[posix(fr.path)], fr.title), esc(fr.type), esc(fr.status), esc(fr.rule)])
    return table_html(rows)


# ---------------------------------------------------------------- build


def build(out: Path, fmt: str, render: bool) -> int:
    cfg = read_config()
    warnings: list[str] = []
    prefix = optional(cfg, "confluence-title-prefix")
    prefix = f"{prefix} " if prefix and not prefix.endswith(" ") else (prefix or "")
    map_path, intro, subdomains, relationships = read_model(cfg, warnings)
    ctx = Ctx(warnings)
    pages = plan_pages(prefix, map_path, subdomains, ctx)

    for sub in ("pages", "attachments"):
        shutil.rmtree(out / sub, ignore_errors=True)
    (out / "pages").mkdir(parents=True, exist_ok=True)
    fill_bodies(pages, map_path, intro, subdomains, relationships, ctx, Renderer(out, fmt, render, warnings))

    entries = []
    for n, p in enumerate(pages, 1):
        body_file = f"pages/{n:03d}-{slug(p.key.rsplit('/', 1)[-1]) or 'page'}.html"
        (out / body_file).write_text(p.body + "\n", encoding="utf-8")
        digest = hashlib.sha256(p.body.encode("utf-8"))
        atts = []
        for a in p.attachments:
            data = a.read_bytes()
            digest.update(data)
            atts.append({"file": a.relative_to(out).as_posix(), "name": a.name, "sha256": sha256(data)})
        entries.append({
            "key": p.key, "kind": p.kind, "title": p.title, "parent": p.parent, "labels": p.labels,
            "body_file": body_file, "sha256": digest.hexdigest(), "attachments": atts,
        })
    space, parent = optional(cfg, "confluence-space"), optional(cfg, "confluence-parent")
    if not space:
        warnings.append("confluence-space is not set in domain-model/config.md: fill it in before syncing")
    manifest = {"version": 1, "space": space, "parent": parent, "title_prefix": prefix, "pages": entries, "warnings": warnings}
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts: dict[str, int] = {}
    for p in pages:
        counts[p.kind] = counts.get(p.kind, 0) + 1
    print(f"{len(pages)} pages -> {out / 'manifest.json'}: " + ", ".join(f"{n} {k}" for k, n in counts.items()))
    for w in warnings:
        print(f"warning: {w}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="command", required=True)
    b = sub.add_parser("build", help="write manifest, page bodies and diagrams")
    b.add_argument("--out", type=Path, default=Path("build/confluence"))
    b.add_argument("--diagram-format", choices=("svg", "png"), default="svg")
    b.add_argument("--no-render", action="store_true", help="no mmdc: diagrams become Mermaid code blocks")
    args = ap.parse_args(argv)
    try:
        return build(args.out, args.diagram_format, not args.no_render)
    except SetupError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
