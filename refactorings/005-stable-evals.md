# Refactoring 005: stable evals for requirement and the problem-space skills

Status: Proposed · Date: 2026-11-16 · Narrowed and decided 2026-11-23

Narrowed because the solution-space skills leave for `implement-the-domain` (refactoring 011): their
evals (`solution-definition`, `test-definition`) move with them and are no part of this refactoring.
This one comes **before** refactoring 010: the suite is the safety net of the build work.

## Goal

The suite gives the same verdict on the same plugin: a failing case means a defect of a skill, not a
changed project checkout or a strict grader.

## Why

Full run of 2026-11-16 (31 cases, one run each): 26 green. Four of the six failures passed two out of
two on a rerun: `gap-becomes-open-point` and `close-validates-and-syncs` stay here,
`invariant-reuses-existing-file` and `journey-step-extends-journey` went to implement-the-domain (011).
Two stayed red:

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
- More flaky cases showed up: `functional-requirement/new-story-creates-frs` (grader 02 flaky before the
  changes, grader 07 failed two of three runs afterwards), `user-story/implemented-story-gets-successor`
  (grader 01, one of three), `domain-init/map-from-code` (grader 08: relationship to a
  subdomain that is not in the domain map, one of three).

## Current state

- `evals/requirement/*/place-files.sh` copy `CLAUDE.md`, glossaries, domain model, ADRs and the config
  from the project named in `evals/.pts-eval-project` or `PTS_EVAL_PROJECT`.
- `claude plugin eval` runs each case three times unless `--runs` says otherwise (`case.runs ?? 3`,
  no case sets `runs`); the full run of 2026-11-16 used one run per case.
- Judge model is the runner's default, `haiku`. Part of the variance of graders that need
  interpretation (02, 05, 07) is the judge, not the grader text [Wahrscheinlich].

## Target state

- A small checked-in project under `evals/fixtures/` replaces the external checkout
  (`.pts-eval-project` is no longer needed). It builds on the invented sample the init evals already
  use (subdomains Fristen and Genehmigung, German problem space): two glossaries, a domain map with a
  subdomain map, a handful of FRs, one ADR under `docs/adr`, a `CLAUDE.md` as `project-rules`, the
  config `evals/fixtures/config.md`. Invented, not a frozen copy of the pilot project: more stable and no German
  domain knowledge needed.
- What the fixture holds follows from the graders and prompts of the eight `requirement` cases: every
  term, FR or ADR a grader names exists in it (e.g. grader 05 of `round-1-grilling-only`: Frist,
  abgeleitete Frist, manuelle Frist, Projekttermin, Persönlicher Termin, Zieltermin, Verantwortlicher,
  an Avoid entry "Termin").
- `evals/fixtures/` and `implement-the-domain/evals/fixtures/` are kept apart, not synchronised
  (decision 2026-11-23); this refactoring extends only the first. When 011 splits the config, each
  plugin's fixture config is adjusted on its own.
- Grader 02 of `round-1-grilling-only`: the provenance line carries `🗣️` and `🧩` with `grilling`, or
  `domain-modeling` for a glossary question (names as renamed in 011). Grader 07: the glossaries and the
  domain map are first read by a subagent. Grader 05: check the compound terms and that "Termin" is not
  used alone as a business term. Graders use today's skill names; 011 carries the renames into
  `evals/` when it renames a skill.
- Graders of the flaky cases above made objective (what exactly is expected, no reading of the judge into
  the tags), as done for `map-missing-*` and `config-*`.
- The suite runs with `--judge-model sonnet` (decision 2026-11-23); `DEVELOPING.md` names the command
  with it.
- The full suite runs with the default of three runs per case; no per-case `runs`.
- `DEVELOPING.md` gets a short section "Rules for graders", so later sessions keep the evals clean:
  one checkable claim per grader; it names the exact text, tag or file it expects, no "appropriate" or
  "sensible"; it demands nothing the skill does not prescribe (the fault of graders 02 and 07); fixtures
  are invented, an eval never reads files of a real project.

## Done when

An LLM never answers twice alike, so "no case ever fails" cannot be reached; a threshold per case
instead:

1. One full run of design-the-domain, three runs per case, judge `sonnet`.
2. A case with 3/3 is stable. A case with 2/3 or worse runs three more times; with at least 5/6 it is
   stable.
3. A case below 5/6 has a defect in its skill or its grader; that defect is fixed and the case runs
   again.

Done when every case is stable this way and the `requirement` cases run without any external
checkout. Cost: about 70 agent runs plus the reruns.
