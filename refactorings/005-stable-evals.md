# Refactoring 005: stable evals for requirement and the problem-space skills

Status: Proposed · Date: 2026-11-16 · Narrowed 2026-11-23

Narrowed because the solution-space skills leave for `implement-the-domain` (refactoring 011): their
evals (`solution-definition`, `test-definition`) move with them and are no part of this refactoring.
This one comes **before** refactoring 010: the suite is the safety net of the build work.

## Goal

The suite gives the same verdict on the same plugin: a failing case means a defect of a skill, not a
changed project checkout or a strict grader.

## Why

Full run of 2026-11-16 (31 cases, one run each): 26 green. Four of the six failures passed two out of
two on a rerun (`gap-becomes-open-point`, `close-validates-and-syncs`, `invariant-reuses-existing-file`,
`journey-step-extends-journey`). Two stayed red:

- `requirement/round-1-grilling-only` (0.63–0.88 in five runs). Three causes, none of them a broken
  skill: the case reads glossaries and FRs from a checkout of the pilot project, so its verdict moves with the
  state of that repository; grader 02 demands `🧩 grilling` on every question although the skill lets
  a glossary question carry `domain-modeling`; grader 07 forbids the main run to read a file the
  ground subagent read, although the skill allows it when a question needs more than the report;
  grader 05 judges "Termin" against an Avoid entry that is meant for code, not for the compound
  terms Zieltermin and Projekttermin. One real defect was found and fixed: `assets/output-format.md`
  said "(English here)" for the heading, so the main run sometimes wrote **Context** instead of
  **Kontext**.
- `solution-definition/not-migrated-context-with-facade` – goes to implement-the-domain (011).

Since then (2026-11-23):

- The config moved to `domain-model/config.md` (refactoring 009); the `requirement` evals still copy
  it from the external checkout at the old place, so they **do not run at all** at the moment.
- More flaky cases showed up: `problem-space-fr/new-story-creates-frs` (grader 02 flaky before the
  changes, grader 07 failed two of three runs afterwards), `problem-space-story/implemented-story-gets-successor`
  (grader 01, one of three), `problem-space-initialization/map-from-code` (grader 08: relationship to a
  subdomain that is not in the domain map, one of three).

## Current state

- `evals/requirement/*/place-files.sh` copy `CLAUDE.md`, glossaries, domain model, ADRs and the config
  from the project named in `evals/.pts-eval-project` or `PTS_EVAL_PROJECT`.
- Single runs; judge model default.

## Target state

- A small checked-in project under `evals/fixtures/` replaces the external checkout
  (`.pts-eval-project` is no longer needed). It builds on the invented sample the init evals already
  use (subdomains Fristen and Genehmigung, German problem space): two glossaries, a domain map with a
  subdomain map, a handful of FRs, one ADR, the config `evals/fixtures/config.md`. Invented, not a
  frozen copy of the pilot project: more stable and no German domain knowledge needed.
- Grader 02 of `round-1-grilling-only`: the provenance line carries `🗣️` and `🧩` with `grilling`, or
  `domain-modeling` for a glossary question (names as renamed in 011). Grader 07: the glossaries and the
  domain map are first read by a subagent. Grader 05: check the compound terms and that "Termin" is not
  used alone as a business term.
- Graders of the flaky cases above made objective (what exactly is expected, no reading of the judge into
  the tags), as done for `map-missing-*` and `config-*`.
- Cases that vary between runs run with `--runs 3` in the full suite.

## Done when

The full suite of design-the-domain, run three times, shows no case that fails in some runs and
passes in others without a change of a skill in between; the `requirement` cases run without any
external checkout.
