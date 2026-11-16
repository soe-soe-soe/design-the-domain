# Evals for solution-init

## Goal

`solution-init` has eval cases under `evals/solution-init/`.

## Why

No evals exist. Commit 2fc62d4 adjusted `context.md` to the new test layout
(tests mirror `backend/` under `‹backend-tests›`, markers stay), but nothing checks that the
migration plan actually moves tests that way.

## Current state

- `skills/solution-init/SKILL.md` and `context.md`, no `evals/solution-init/`.
- The fixtures of `evals/solution-definition/` already hold a migrated (`permits`) and a
  not-migrated context (`deadlines`) with glossaries and `structure.md` – reusable.

## Target state

Cases, at least:

- **plan-not-migrated-context:** `deadlines` (models/service/router) → plan
  `‹refactorings›/solution-structure-deadlines.md` with Goal, Why, Current state, Target state,
  Before starting; every module assigned to exactly one building block; tests get the mirrored
  path; no code changed.
- **boundary-violation-reported:** a module importing another context past its facade →
  counted under Boundary violations and asked as a question with Case `boundary`.
- **aggregate-cut-asks:** a command spanning two aggregates → question with Case `aggregate-cut`.
- **seed-consumed:** an existing `solution-init-seed.md` is handed to the subagent and deleted
  once its contexts are planned.

## Before starting

- Name the contexts in the prompt (`/pts:solution-init deadlines`) to skip AskUserQuestion.
- `‹context-map-command›` must exist in the eval project or be stubbed in `place-files.sh`.
