# Refactoring 005: stable evals for requirement and solution-definition

Status: Proposed · Date: 2026-11-16

## Goal

The suite gives the same verdict on the same plugin: a failing case means a defect of a skill, not a
changed project checkout or a strict grader.

## Why

Full run of 2026-11-16 (31 cases, one run each): 26 green. Four of the six failures passed two out of
two on a rerun (`gap-becomes-open-point`, `close-validates-and-syncs`, `invariant-reuses-existing-file`,
`journey-step-extends-journey`). Two stay red:

- `requirement/round-1-grilling-only` (0.63–0.88 in five runs). Three causes, none of them a broken
  skill: the case reads glossaries and FRs from a checkout of the pilot project, so its verdict moves with the
  state of that repository; grader 02 demands `🧩 grilling` on every question although the skill lets
  a glossary question carry `domain-modeling`; grader 07 forbids the main run to read a file the
  ground subagent read, although the skill allows it when a question needs more than the report;
  grader 05 judges "Termin" against an Avoid entry that is meant for code, not for the compound
  terms Zieltermin and Projekttermin. One real defect was found and fixed: `assets/output-format.md`
  said "(English here)" for the heading, so the main run sometimes wrote **Context** instead of
  **Kontext**.
- `solution-definition/not-migrated-context-with-facade` (0.80 in three runs): grader 04 allows only
  the new facade method as shell, the run also adds the query file the placement names. Both are
  behaviour-free shells; the grader is narrower than the skill.

## Current state

- `evals/requirement/*/place-files.sh` copy `CLAUDE.md`, glossaries, domain model and ADRs from the
  project named in `evals/.pts-eval-project` or `PTS_EVAL_PROJECT`.
- Single runs; judge model default.

## Target state

- A small checked-in project under `evals/fixtures/` (two glossaries, a domain map, a handful of FRs,
  one ADR) replaces the external checkout; `.pts-eval-project` is no longer needed.
- Grader 02: the provenance line carries `🗣️` and `🧩` with `grilling`, or `domain-modeling` for a
  glossary question. Grader 07: the glossaries and the domain map are first read by a subagent.
  Grader 05: check the compound terms and that "Termin" is not used alone as a business term.
  `not-migrated-context-with-facade` grader 04: allows the shell files the placement names.
- Cases that vary between runs (the four above) run with `--runs 3` in the full suite.

## Before starting

- Decide whether the fixture is the pilot project's state frozen at a commit or an invented sample project
  (invented is more stable and needs no German domain knowledge).
