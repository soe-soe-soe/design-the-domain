# Refactoring 004: problem-space-initialization describes only its delta

Status: Proposed · Date: 2026-11-16 · Skills: problem-space-initialization, problem-space-fr,
requirement, domain-modeling · Script: requirements.py, interview-round.py

## Goal

Each piece of knowledge about the problem space stands in exactly one place, in the core skills and
assets. `problem-space-initialization` describes only what is different when the model is taken over
from existing code instead of grilled from a requirement. The domain map is the only index of
subdomains and glossaries.

## Why

`skills/problem-space-initialization/subdomain.md` repeats rules the core skills own: layout, folder
and ID naming, numbering, template, scenario format, glossary rules, the question format. Two rules
stand only there although they hold for every FR: how a plain create/change/delete is cut (one
Command FR per business object) and how a folder name is spelled. Numbering is described in two
places; `subdomain.md` says "from 001" while `problem-space-fr` counts across active and planned FRs,
so a subdomain with a planned new FR gets a duplicate number.

The glossary map was needed because Pocock's `domain-modeling` looked for it in the project root.
The plugin has its own `domain-modeling` since November 2026, so two indexes of the same facts remain
with nobody comparing them (see `refactorings/problem-space/glossary-map-and-domain-map.md`).

## Current state

| Step of `subdomain.md` | Owner today | Owner after |
|---|---|---|
| Sources: tests, rules, facade and routers | init | init (delta) |
| Sources: cross-check (glossary, methodology, domain map, ADRs) | init and `requirement` step 1 | one definition of the "ground", both refer to it |
| Business object = aggregate root, entities belong to it | `assets/glossary.md` | unchanged |
| Heuristic: own repository, service or router | init | init (delta) |
| Folder name: language, lower case, special letters spelled out, hyphens | init | `problem-space-fr`, section Layout |
| Glossary rows from code, nothing unbacked, no change to existing rows | init | init (delta); format by `domain-modeling` and `assets/glossary.md` |
| Cut FRs: code construct → FR type | init | init (delta) |
| Cut FRs: one Command FR per business object, scenarios for validations and permissions only | init | `assets/functional-requirement-types.md` |
| Layout, template, numbering, subdomain name rule | init (copy) | `problem-space-fr`, refer only |
| Scenarios: format | `assets/acceptance-criteria.md` | unchanged |
| Scenarios: one per test, test values, active FR directly, `@existing @unconfirmed` | init | init (delta) |
| Marker in the tests, `test-collect` check | init | **dropped**, see below |
| Findings → questions: five cases | init | init (delta) |
| Question format | init (described again) | `interview-round.py` |
| Report | init | init (delta) |

Global index: `GLOSSARY-MAP.md` (`‹glossary-map›`) and `domain-map.md` both list the glossaries.

## Target state

**Core first** (init refers to these, so they must hold the rules before init is cut):

1. `assets/functional-requirement-types.md`: granularity of Command FRs (one per business object for
   plain create/change/delete, scenarios only for validations and permissions; no FR per endpoint).
2. `problem-space-fr`, Layout: the folder-name rule.
3. `requirements.py next-fr <subdomain>`: highest `NNN` across active and planned FRs plus one, never
   a reused number; `problem-space-fr` and init call it instead of describing the rule.
4. The ground (what a skill reads before it writes: glossaries, domain map, ADRs, drafts, planned FRs)
   is defined once, in `requirement`, step 1; init reads the same for its subdomain, plus code.
5. Domain map instead of two maps (option 2 of the existing refactoring): the Glossary column of
   `assets/domain-map.md` is the index, the methodology glossary gets a row there. Removed:
   `assets/glossary-map.md`, config key `glossary-map`, its use in `domain-modeling`, `requirement`,
   init and `assets/output-format.md`, the fixtures, and `GLOSSARY-MAP.md` in projects. Whoever
   creates a glossary adds the subdomain's row in the same change.

**Then init** (`problem-space-initialization`):

6. Only the delta: sources from code, business-object heuristic, code construct → FR type, scenarios
   from tests, the five question cases, report. The vocabulary is "take over" (as in the tag history
   line "taken over from code"), not "initialise a subdomain".
7. No markers in tests and no `test-collect` check: the plugin has no test space yet. The tests stay a
   *source*. The report drops "Tests with reference" and keeps "Without test" (scenarios from code
   only). Linking tests to scenarios becomes a step of the test space later. Config keys
   `scenario-marker`, `backend-tests` and `test-collect` are no longer needed by init.
8. Questions are not open points: an active FR carries no `@open` (`problem-space-fr`), init marks
   `@unconfirmed` and reports the questions. Rendering uses `interview-round.py` (`source`
   `problem-space-initialization`, `ref`, `type`), which needs a way to group by subdomain instead
   of by story. A question whose answer changes behaviour belongs in a `requirement` session.
9. Where the delta lives (file `subdomain.md` or inside `SKILL.md`): open, see below.

**Evals** (`evals/problem-space-initialization/`):

10. Remove the marker graders (`one-subdomain-from-code` grader 04, `two-subdomains-reconciled`
    grader 04 and the moving of a marker in its expected outcome).
11. New: `numbering-continues` (a subdomain with an active FR 002 and a planned new FR 003 → init
    writes 004); `domain-map-row` (a new subdomain gets its row with the glossary link, no glossary
    map).
12. Run each case several times, then the whole suite.

## Before starting

- Order: 1–4 and 5 (independent of each other), then 6–8, then evals.
- The pilot project: delete `GLOSSARY-MAP.md` and the key `glossary-map` in `.claude/pts.md` when it adopts
  the plugin version with this change; its `_methodology.md` names the glossary map in its terms.
- `requirements.py history` prints "existing: taken over from code (problem-space-initialization)";
  keep that line.

## Open

- **Name and form of `subdomain.md`.** After the cut it holds no knowledge of its own, only the brief
  of the subagent. Options: (a) keep a file under a better name (`take-over.md`); (b) put the brief
  inline into `SKILL.md`, as `requirement` does with the briefs of its subagents; (c) a skill of its
  own that the subagents call, like the writers of `requirement`; (d) spread the delta over the core
  assets. Recommendation: (b), see the discussion of 2026-11-16: (d) puts init-only knowledge into
  files every other skill reads, (c) adds a skill nobody calls alone.
