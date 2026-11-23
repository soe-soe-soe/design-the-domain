# DR 004: Pocock's `tdd` is called, not copied

**Status:** Accepted · **Date:** 2026-10-26

## Context

What a good test is (behaviour through public interfaces, no tautological expectations, mocks only
at system boundaries) is already written down in Pocock's `tdd`. A copy would drift from his
updates.

## Decision

`test-definition` loads `mattpocock-skills:tdd` for its test-quality rules and puts two project
rules on top: the seams are fixed by the target structure, and the red → green loop is not run.
`implement-story` loads the same skill for the loop. What the workflow relies on and overrides is
listed in `.claude/pocock-skills.md`; a weekly scheduled task compares Pocock's changes against
that list.

## Considered alternatives

- **Own test rules in the skill:** independent of Pocock, but rebuilt and unmaintained. Rejected.
