# DR 005: Untestable scenarios go back instead of being guessed

**Status:** Accepted · **Date:** 2026-10-26

## Context

In the eval `data-migration-test` the scenario named "Schallgutachten", but the test had to store
it in the column `evidence.kind`, whose value (`sound_report`?) stood nowhere. A guessed value can
make a correct migration fail. In `outline-and-untestable` a Dann ("deutlich hervorgehoben") had
no value to assert.

## Decision

The skill writes no test that would have to guess and reports the scenario as untestable, with
where it goes back: the **problem space** when the scenario lacks an observable value, the
**solution-definition** when a seam or a stored value is missing from the placement, the glossary
`Identifier` column and the code. Test infrastructure (fixtures, `conftest.py`) the skill may
add; configuration outside the test folders it may not.

## Considered alternatives

- **Guess and mark the guess:** a wrong guess turns a correct implementation red. Rejected.
