# DR 003: Scenario tests and interface tests, nothing per building block by default

**Status:** Accepted · **Date:** 2026-10-26

## Context

Asked to write "all kinds of tests", a skill would test every repository, endpoint and migration
file on its own, duplicating what the scenario tests already prove.

## Decision

The skill writes exactly one test per source line: a **scenario test** per planned FR scenario
(marker `fr`) and an **interface test** per facade method in the placement's `Interfaces`
(marker `story`), because a facade is the contract another context depends on and no scenario
names it. Repositories, endpoints and schemas get no test of their own; levels and paths come
from `domain-model/solution-space/structure.md`.

## Considered alternatives

- **A test per building block:** slower suite, costlier refactorings, same coverage. Rejected.
- **No interface tests:** a facade change would be tested only through the consumer's scenario,
  if at all. Rejected at the user's request.
