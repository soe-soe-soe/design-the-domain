# DR 001: One orchestrator from placement to commit, with a review gate

**Status:** Accepted · **Date:** 2026-10-26

## Context

The feature workflow has five steps: problem definition, solution definition, test definition,
implementation (`tdd`), review (`code-review`). The first is an interview of its own; the others
depend on each other's output in the same session.

## Decision

`/requirement` runs on its own. `/implement-story` runs the rest in order:
`solution-definition` → `test-definition` → the user reviews the tests → `tdd` → `code-review` →
close and one commit. Questions it has to ask are reported as lessons for the problem definition.

## Considered alternatives

- **Each step as its own command:** more control, but the placement report and the test report
  would have to be handed over by hand or in files. Rejected.
