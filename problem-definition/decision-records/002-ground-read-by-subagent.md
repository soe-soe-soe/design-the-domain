# DR 002: The ground is read by a subagent

**Status:** Accepted · **Date:** 2026-10-27

## Context

Step 1 read glossaries, domain map, draft stories and whatever the idea pointed to (refactoring
plans, frontend code) into the interview's context. That is the largest single block of a
session, while the interview needs only the state, the terms and the drafts' open points.

## Decision

One subagent reads the ground and reports `Kontext`, `Stand` (at most 15 lines), `Begriffe` and
`Drafts`. The interview runs on the report and reads a file itself only when a question needs
more.

## Considered alternatives

- **Reading in the main context as before:** every detail at hand, but files stay in the
  context for the whole session. Rejected.
- **A subagent that formats the answers:** it would need the whole content and its result lands
  in the main context anyway. Rejected; subagents pay off when they read much and return little.
