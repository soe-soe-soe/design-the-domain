# DR 003: Stored values of a scenario's values go into the glossary

**Status:** Accepted · **Date:** 2026-10-26

## Context

In the eval `data-migration-test` of `test-definition`, a scenario named "Schallgutachten", but
the test had to write it into the column `evidence.kind`. The stored form (`sound_report`?)
stood neither in the glossary nor in the code, so the test could only guess, and `test-definition`
rightly refused (its DR 005).

## Decision

When placing a scenario that names a value of a set (a kind, a status) whose stored form a test
must write or read, `solution-definition` enters that form into the `Identifier` column of the
value's glossary row – from the code if it exists, otherwise decided as part of the placement.

## Considered alternatives

- **`test-definition` decides the stored form:** a test would fix a solution-space decision
  nobody reviewed as such. Rejected.
- **Problem space names the stored form:** stored values are solution space. Rejected.
