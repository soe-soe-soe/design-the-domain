# DR 001: Context block with artifact icons, type icon instead of 🏷️

**Status:** Accepted · **Date:** 2026-10-27

## Context

The skill opened a session with a sentence like "I read the issue, the glossary of the area, the
refactoring plan …". The user could not tell what "the issue" was, and the list was hard to
scan. Questions referred to the same artifacts with a generic 🏷️.

## Decision

Every message after reading artifacts not listed yet starts with a `**Kontext**` block, one
item per artifact with an icon from a table in `.claude/skills/assets/output-format.md`, a file shared by
the project's skills: one example and one table instead of prose rules. The reference entry of the
provenance line uses the same icon, so a question points visibly at a listed artifact.

The table is split into problem and solution space. Types carry the artifact's name in the
repository (`glossary`, `context-map`, `ADR`); icons group them: stories and refactorings (📘),
FRs (📋), problem-space documents (📄), solution-space documents (🗂️), decisions (🏛️), code
(⚙️), tests (🧪), the web (🔗). Subdomain, business object, rule or variant are terms in a
glossary or an FR, not artifact types, and a reference never points at a term. An artifact
of a type the table lacks is a document (📄); folder index files like `README.md` are not listed. What the user passed in – idea text, ticket link, images – is
the prompt and is not listed.

## Considered alternatives

- **Prose sentence as before:** rejected, see context.
- **Keep 🏷️ for every reference:** rejected, the reader cannot see whether a question rests on
  an FR, a story or a UI part without reading the ID.
- **One icon per artifact kind (18 icons):** rejected as too many to recognise; within
  a space, glossary and domain map, or structure and context map, are all "a document".
- **Listing the ticket and attached images:** rejected, they are the prompt the user knows,
  not context the skill fetched.
- **Icon table in `SKILL.md`:** every further skill would copy it, and format rules would crowd
  the skill's logic. Rejected for the shared file.
- **Icon table in `_methodology.md`:** the icons are an output format, not domain-model
  methodology. Rejected.
- **A "rule" type for `CLAUDE.md`:** a domain rule is an FR or a scenario in it, and
  `CLAUDE.md` is always loaded like the prompt. Rejected.
- **One icon for all documents:** hides whether a question rests on the problem or the solution
  space. Rejected for 📄 and 🗂️.
