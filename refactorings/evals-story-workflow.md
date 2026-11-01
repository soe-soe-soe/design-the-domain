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
- Gates in the skill: step 1 stops on a story that is not `ready` or fails `requirements.py check`; step 4 waits for the user
  after test-definition's report; step 8 reports lessons.

## Target state

Cases, at least:

- **draft-story-stops:** a `draft` story with entries under `## Open` → the run stops in
  step 1, names the open points, writes nothing.
- **review-gate-waits:** a `ready` story with a small fixture backend → the run places, writes
  red tests and stops at step 4 with test-definition's report; no implementation yet.
- **stale-base-stops:** a `ready` story whose planned scenario carries `@base-US-0050` while
  the active scenario now carries `@US-0058` → `requirements.py check` fails in step 1, the story
  goes back to `draft`, nothing else is written.
- Optional, once the above are stable: **close-sets-done** – a story whose tests are already
  green → `requirements.py complete` merges into the active FR, the story is `done` with `doneAt`
  and moved out of `planned/`, one commit, `Lessons: none`.

## Before starting

- Decide how the evals provide the external skills (installed in the eval environment or
  stubbed); without them steps 5 and 6 cannot run.
- Check that `max_turns`/`timeout_seconds` suffice for the review-gate case – it runs two
  skills before stopping.
