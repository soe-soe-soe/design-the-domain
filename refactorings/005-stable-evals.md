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
- The suite runs with the default judge Haiku and `--ablation none`, reruns too. Changed 2026-11-23 from Sonnet
  throughout: the first full run cost about $440, $404 of it the Sonnet judge (about $7 per run
  against $0.50 with Haiku), and it also ran a no-plugin baseline and the implement evals.
- The full suite runs with the default of three runs per case; no per-case `runs`.
- `DEVELOPING.md` gets a short section "Rules for graders", so later sessions keep the evals clean:
  one checkable claim per grader; it names the exact text, tag or file it expects, no "appropriate" or
  "sensible"; it demands nothing the skill does not prescribe (the fault of graders 02 and 07); fixtures
  are invented, an eval never reads files of a real project.

## Progress (2026-11-23)

- `evals/fixtures/project/` (invented, see `evals/fixtures/README.md`): CLAUDE.md with a feature
  workflow, domain map, subdomain maps, glossaries Fristen and Genehmigung, active FR-fristen-009
  (S6 last changed by US-0042, so a planned `@base-US-0030` fails `check`), FR-fristen-006,
  FR-genehmigung-001, done stories US-0030 and US-0042. No ADR: since 011 no design skill reads one.
- `evals/fixtures/config.md` cut to the design part (no Solution space, Commands, solution code keys).
- The seven `requirement` scaffolds copy the fixture project; case FR files moved into their type
  folders (`commands/`, `policies/`). `.pts-eval-project` is no longer read.
- Graders made objective: `round-1-grilling-only` 02, 05, 06, 07; `new-story-creates-frs` 02, 07;
  `implemented-story-gets-successor` 01; `map-from-code` 08; `close-validates-and-syncs` 04;
  `gap-becomes-open-point` 06.
- `DEVELOPING.md`: command (Haiku judge, `--ablation none`; `--eval-dir evals` does not keep the
  implement evals out, single cases run with `--case`), stability threshold, rules for graders
  (regex graders for fixed texts; `focus: files` shows only paths; the judge sees at most 100,000
  characters of a trace).
- Runs: full run with Haiku (`evals/results/005-full-2.json`): 21 of 29 design cases 3/3. Reruns in
  `evals/results/005-rerun/`. Found and fixed on the way:
  - Fixture: the closing cases lacked the planned FR-fristen-013/-014 their stories name, US-0051
    carried the role sentence of US-0050 (a run refused to set US-0050 ready because of it).
  - Skills: `user-story` once wrote an English summary before its report → the report rule of
    `user-story` and `functional-requirement` now fixes the first and last line; `domain-init` wrote
    a code name (`permits`) into the domain map's relationships → brief and reconcile step demand the
    business name.
  - Fixture config got the Confluence section the template gained in parallel work.
  - Graders: regex instead of judge for FR header, change line, FR type, no `## History`, no story
    headings in round 1, the open point of `glossary-conflict-asks`, the report of
    `gap-becomes-open-point`, the relationship row of `map-from-code`; judge graders that allowed
    only one of two allowed forms widened (🗣️ <user> 🧩 glossary from the round script, an FR open
    point merged into an own question, a plural subdomain name).
- Judge for reruns: Haiku too. Five reruns with Sonnet cost $69 (about $14 per case) and were not
  steadier.
- Cost of all runs on 2026-11-23: about $610, of it $440 for the first, aborted run (Sonnet judge,
  baseline arm, implement evals).

### State per case (latest run)

Stable (3/3): the 21 of the full run, `close-validates-and-syncs`, `close-with-deferred-point`,
`closing-round-asks-story-open-points`, `new-story-creates-frs`, `gap-becomes-open-point`,
`round-2-merges-open-points`, `glossary-conflict-asks`, `clear-decisions-no-questions`;
`map-from-code` 3/3 after the `domain-init` fix with grader 08 checked again on the saved maps.

Open:
- `round-1-grilling-only` 4/6: once the round differs from the output of `interview-round.py`
  (grader 09), once a question says "Termin" alone (grader 05). Both are model slips, not grader
  faults.
- The changes to `user-story` and `functional-requirement` came after the full run; their 12 cases
  did not run again with them.
- `domain-init/config-filled-after-answers` grader 01 lists the config sections without Confluence;
  it fails once the Confluence section of the template is committed.

## Done when

An LLM never answers twice alike, so "no case ever fails" cannot be reached; a threshold per case
instead:

1. One full run of design-the-domain, three runs per case, judge Haiku.
2. A case with 3/3 is stable. A case with 2/3 or worse runs three more times, judge Haiku; with at least 5/6 it is
   stable.
3. A case below 5/6 has a defect in its skill or its grader; that defect is fixed and the case runs
   again.

Done when every case is stable this way and the `requirement` cases run without any external
checkout. Cost: about 90 agent runs (about $70) plus the reruns.
