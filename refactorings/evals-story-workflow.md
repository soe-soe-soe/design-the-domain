# Evals for story-workflow

## Goal

`story-workflow` has eval cases for its own rules – the gates, the order and the closing –
without re-testing what `solution-definition` and `test-definition` evals already cover.

## Why

It is one of the two user-facing workflows and has no eval. A full run (placement, red tests,
tdd, review, commit) is long and depends on external skills (`‹skill-tdd›`,
`‹skill-code-review›`), so the cheap, decisive parts are worth testing first.

## Current state

- `skills/story-workflow/SKILL.md` with two decision records, no `evals/story-workflow/`.
- Gates in the skill: step 1 stops on a story that is not `ready`; step 4 waits for the user
  after test-definition's report; step 8 reports lessons.

## Target state

Cases, at least:

- **draft-story-stops:** a `draft` story with entries under `## Open` → the run stops in
  step 1, names the open points, writes nothing.
- **review-gate-waits:** a `ready` story with a small fixture backend → the run places, writes
  red tests and stops at step 4 with test-definition's report; no implementation yet.
- Optional, once the above are stable: **close-sets-done** – a story whose tests are already
  green → `Status: done`, `@planned` removed, one commit, `Lessons: none`.

## Before starting

- Decide how the evals provide the external skills (installed in the eval environment or
  stubbed); without them steps 5 and 6 cannot run.
- Check that `max_turns`/`timeout_seconds` suffice for the review-gate case – it runs two
  skills before stopping.
