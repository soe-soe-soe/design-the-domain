# DR 003: Closing a story is a script, not a skill or a subagent

**Status:** Accepted · **Date:** 2026-11-01

## Context

When a story is done its planned FR changes go into the active FRs, the story gets `done` and
`doneAt` and moves out of `planned/`. A background subagent on a small model was considered.

## Decision

`scripts/requirements.py complete` does it deterministically, all or nothing, before the commit of
story-workflow step 7, so placement, tests, code and problem space land in one commit. It checks
each `@base-` tag first and writes nothing on a conflict. `check`, `cancel` and `history` use the
same parsing.

## Considered alternatives

- **Subagent on a small model:** a merge mistake corrupts the source of truth unnoticed, for a
  saving of cents. Rejected.
- **In the background:** a second commit, or none if the session ends first. Rejected.
- **A skill wrapping the script:** adds nothing; the script can be called directly for repair.
  Rejected.
