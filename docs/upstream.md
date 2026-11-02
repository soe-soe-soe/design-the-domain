# Upstream: mattpocock/skills

Five craft skills of pts are taken over from [mattpocock/skills](https://github.com/mattpocock/skills)
(MIT, see [THIRD_PARTY_LICENSES.md](../THIRD_PARTY_LICENSES.md)) instead of being installed next to
the plugin, so the workflow works on its own and an upstream change cannot alter it unnoticed.
Upstream changes are still worth knowing: a weekly check reports them, and the user decides what
to take over.

## Taken over

Last synced: commit `4ae2317` (2026-10-31).

| pts skill | Upstream | Status | Changed for pts |
|---|---|---|---|
| `grilling` | `skills/productivity/grilling` | unchanged | – (grouping, numbering and the provenance line live in `problem-definition`) |
| `codebase-design` | `skills/engineering/codebase-design` (+ `DEEPENING.md`, `DESIGN-IT-TWICE.md`) | unchanged | – |
| `domain-modeling` | `skills/engineering/domain-modeling` (+ `ADR-FORMAT.md`) | adapted | one glossary per subdomain as a table (format in `templates/glossary.md`, upstream `GLOSSARY-FORMAT.md` dropped), domain map for new subdomains and relationships, paths from `.claude/pts.md`, ADR numbering and rules as the project keeps them |
| `tdd` | `skills/engineering/tdd` (+ `tests.md`, `mocking.md`) | adapted | seams agreed once in `‹structure›` instead of per session; scenario tests of `test-definition` written before the loop as a named exception to horizontal slicing; Dann literals as source of truth; migration tests may read stored data; `pts:codebase-design` |
| `code-review` | `skills/engineering/code-review` | adapted | spec = the story with its FR scenarios (planned files), standards include `‹project-rules›`, `‹structure›`, test strategy and architecture ADRs; no issue tracker setup |

Not taken over: `implement` (used by projects for work without a story; install mattpocock/skills
for it), `agents/openai.yaml` of each skill.

## Weekly check

Runs once a week (a scheduled task, wherever the user keeps it) with this brief:

> In `mattpocock/skills`, list the commits since the commit named under *Last checked* below that
> touch `skills/productivity/grilling`, `skills/engineering/domain-modeling`,
> `skills/engineering/tdd`, `skills/engineering/code-review` or
> `skills/engineering/codebase-design`, or add a skill that overlaps a step of the pts workflow.
> For each relevant change, compare it with the pts skill named in *Taken over* of
> `docs/upstream.md` in `soe-soe-soe/problem-test-solution-skills` and report: what changed
> upstream, whether pts already covers it, contradicts it on purpose (the column *Changed for
> pts*), or should take it over – with a recommendation. Change nothing. Report "no upstream
> changes" when there are none.

When the user takes a change over, update the skill, the row above and *Last synced*. After every
check, update *Last checked*.

Last checked: commit `4ae2317` (2026-11-01).
