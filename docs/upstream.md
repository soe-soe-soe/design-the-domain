# Upstream: mattpocock/skills

Craft skills of design-the-domain and implement-the-domain are taken over from [mattpocock/skills](https://github.com/mattpocock/skills)
(MIT, see [THIRD_PARTY_LICENSES.md](../THIRD_PARTY_LICENSES.md)) instead of being installed next to
the plugins, so the workflow works on its own and an upstream change cannot alter it unnoticed.
Upstream changes are still worth knowing: a weekly check reports them, and the user decides what
to take over.

## Taken over

Last synced: commit `4ae2317` (2026-10-31).

| Our skill | Upstream | Status | Changed by us |
|---|---|---|---|
| `design-the-domain:domain-grilling` | `skills/productivity/grilling` | adapted | name (collides with upstream `grilling`), a narrow description; upstream text unchanged, plus the section *Rounds in this project*: rendering by `interview-round.py`, numbering across rounds, grouping, open points of the writers, deferring, closing round, references after the title |
| `design-the-domain:domain-interview` | `skills/engineering/grill-with-docs` | adapted | composes `domain-grilling` and `glossary` like upstream, and adds the ground read by a subagent, the writers after every round, parallel changes and the close through `story-workflow ready` |
| `implement-the-domain:codebase-design` | `skills/engineering/codebase-design` (+ `DEEPENING.md`, `DESIGN-IT-TWICE.md`) | unchanged | – |
| `design-the-domain:glossary`, `implement-the-domain:solution-definition` | `skills/engineering/domain-modeling` (+ `ADR-FORMAT.md`) | adapted, split | see *Split skills* below |
| `implement-the-domain:tdd` | `skills/engineering/tdd` (+ `tests.md`, `mocking.md`) | adapted | seams agreed once in `‹structure›` instead of per session; scenario tests of `test-definition` written before the loop as a named exception to horizontal slicing; Dann literals as source of truth; migration tests may read stored data; `implement-the-domain:codebase-design` |
| `implement-the-domain:code-review` | `skills/engineering/code-review` | adapted | spec = the story with its FR scenarios (planned files), standards include `‹project-rules›`, `‹structure›`, test strategy and architecture ADRs; no issue tracker setup |

### Split skills

An upstream skill whose parts went into several of our skills (refactoring 011). A change upstream
goes to the skill that holds the changed part.

**`skills/engineering/domain-modeling`**

| Upstream part | Our skill | Changed by us |
|---|---|---|
| Challenge against the glossary, sharpen fuzzy language, discuss concrete scenarios, cross-reference with code, update the glossary inline, file structure | `design-the-domain:glossary` | one glossary per subdomain as a table (format in `assets/glossary.md`, upstream `GLOSSARY-FORMAT.md` dropped), domain map for new subdomains and relationships, paths from `domain-model/config.md`; solution-space columns set through its interface; scenarios become ACs and FR scenarios, a confirmed difference to the code is the delta to implement |
| Offer ADRs sparingly, `ADR-FORMAT.md` | `implement-the-domain:solution-definition` (section ADRs, `ADR-FORMAT.md`) | ADRs belong to the solution space only; folder `‹adr›`, rules of `‹project-rules›` win |

Not taken over: `implement` (used by projects for work without a story; install mattpocock/skills
for it), `agents/openai.yaml` of each skill.

## Weekly check

Runs once a week (a scheduled task, wherever the user keeps it) with this brief:

> In `mattpocock/skills`, list the commits since the commit named under *Last checked* below that
> touch `skills/productivity/grilling`, `skills/engineering/domain-modeling`,
> `skills/engineering/tdd`, `skills/engineering/code-review` or
> `skills/engineering/codebase-design`, or add a skill that overlaps a step of the design-the-domain
> or implement-the-domain workflow. For each relevant change, find our skill in *Taken over* of
> `docs/upstream.md` in `soe-soe-soe/design-the-domain` – for a split skill the one that holds the
> changed part, by the table under *Split skills* – compare it and report: what changed
> upstream, whether design-the-domain already covers it, contradicts it on purpose (the column *Changed for
> design-the-domain*), or should take it over – with a recommendation. Change nothing. Report "no upstream
> changes" when there are none.

When the user takes a change over, update the skill, its row above (for a split skill the row in
*Split skills*) and *Last synced*. After every
check, update *Last checked*.

Last checked: commit `5863806` (2026-11-16).
