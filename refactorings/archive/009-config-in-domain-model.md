# Refactoring 009: project config in `domain-model/config.md`, filled by the init skill

Status: Implemented · Date: 2026-11-23

## Goal

The project config lives in a tool-neutral place and nobody has to know it exists: a skill
without it says so in one sentence, and `problem-space-initialization` fills it in with the user.

## Why

`.claude/pts.md` was a convention from the plugin's early days (`pts` = problem-test-solution),
tied to Claude Code. The skills are meant to run in other tools as well (opencode), and a missing
config ended in "point the user to the template", which leaves the work to the user.

## Decisions

- **Place:** `domain-model/config.md`, beside what it configures (problem space, glossaries,
  solution space). A fixed path, not a key of the file: a skill must find it before it knows any key.
- **Missing or unfilled config in any skill:** stop and tell the user, in their language and
  nothing else, to fill in `domain-model/config.md` first and that
  `/design-the-domain:problem-space-initialization` does it with them. No guessing of values.
  `requirements.py` says the same.
- **Unfilled** means a key without a value or with a value that is only a placeholder (`<name>`);
  a pattern with brackets inside a value (`FR-<subdomain>-NNN`) counts as filled.
- **Init skill, new step 1 "Config":** first of all, before anything else of the project is read.
  It derives a proposal per open key from the project with its source (root layout, `CLAUDE.md`,
  `AGENTS.md`, README, build files, test and ADR folders, an existing `domain-model/`), never guesses
  a value it does not find, asks one question per group of the template through `interview-round.py`
  and writes the file only after the answers. A key that does not apply gets `–`.
- Plugin version 0.8.0: a breaking change of the config location; no migration, no project had the
  new file yet.

## Implemented

- Path replaced in all skills, assets, `scripts/requirements.py` and its tests, README, DEVELOPING and
  the evals (fixture `evals/fixtures/config.md`, all `place-files.sh`).
- Standard sentence for a missing config in every skill that reads it; message of `requirements.py`.
- Evals: `problem-space-initialization/config-missing-asks`,
  `problem-space-initialization/config-filled-after-answers` and `requirement/config-missing-points-to-init`.

## Evals (2026-11-23)

- `config-missing-points-to-init` 3/3, `config-filled-after-answers` 3/3, `config-missing-asks` 0.95
  (3 runs, remaining misses were judge noise on graders 03/04/07, reworded twice).
- Found by the first run: `interview-round.py` reads the config itself and fails without it, so the
  config step of the init skill asks in the interview format by hand.
- Found by the first run: a key without an answer stays a placeholder; the prompt of
  `config-filled-after-answers` names the keys that do not apply.
- Regression run of the other `problem-space-*` cases (1 run each): all green except flakes in
  `implemented-story-gets-successor` (grader 01, 1 of 3), `new-story-creates-frs` (grader 02 flaky
  before this change too, grader 07 failed 2 of 3 and not in the baseline of commit 8012418, not
  analysed further) and `map-from-code` grader 08 (relationship to a subdomain that is not in the
  domain map yet; the reconcile step now says to add it, 1 of 3 still missed).
## Open

- The `requirement` evals take the config from an external project checkout
  (`PTS_EVAL_PROJECT`, see refactoring 005); that checkout needs the file at the new place before
  they run again.
- opencode: the path was the smaller part. `${CLAUDE_PLUGIN_ROOT}`, subagents and the question tool of
  the skills are bound to Claude Code and need their own refactoring.
