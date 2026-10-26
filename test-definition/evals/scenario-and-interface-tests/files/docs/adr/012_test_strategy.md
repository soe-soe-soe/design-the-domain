# ADR 012: Test strategy – every scenario and every boundary gets exactly one test

**Status:** Accepted
**Date:** 2026-10-26
**Deciders:** Development team

## Context

Requirements live in the problem space as user stories and FR scenarios (Gherkin, German); the
code lives in the solution space under `backend/domain/<context>/` (ADR 008, 009). The test is
the bridge between both (Specification by Example, Living Documentation): its marker names the
scenario it proves, its path mirrors the code it tests.

So far it was open which tests a story needs, at which level, and when they are written. Tests
came about during implementation, at whatever seam seemed right; end-to-end tests appeared
without a rule; migrations were not tested at all, although they become critical once the
application runs in production. The feature workflow wanted the tests defined before the
implementation, but a test at a mirrored path presumes that the placement is known.

## Decision

1. **Order: placement, then tests, then implementation.** `solution-definition` places the
   story and creates only the shell (new files and symbols whose body raises
   `NotImplementedError`, behaviour-preserving moves, deletion of unused code).
   `test-definition` writes the tests against that shell; the user reviews them; Pocock's `tdd`
   then makes them green one at a time. A test imports the building block from its placed path,
   so it can only turn green where the placement put the code.
2. **Tests are red, not `xfail`.** They are committed together with the implementation, never
   on their own; the suite on `main` stays green.
3. **Two kinds of tests.** A **scenario test** proves one FR scenario and carries
   `@pytest.mark.fr("FR-…/Sn")`, exactly one main test per scenario. An **interface test**
   checks a boundary the story adds or changes – a facade method another context uses – and
   carries `@pytest.mark.story("US-NNNN")`. Repositories get no test of their own: every
   integration test runs through the real SQL repository.
4. **The test level follows the building block, not the FR.** Unit for building blocks under
   `model/`, integration with database for commands, queries, policies, facades and
   anti-corruption layers (with a fake of the foreign system). The table lives in
   `domain-model/solution-space/structure.md`; the problem space carries no test level.
5. **Existing data is a requirement.** A story that changes stored data states, as acceptance
   criteria, what happens to the data that already exists. Such a scenario is an FR of type
   *Data Migration*; its scenario test seeds the old state, runs the migration and checks the
   new state. Once, globally, a test runs the whole migration chain up and down and checks with
   `alembic check` that models and migrations agree.
6. **End-to-end tests are journeys per business object.** One journey per business object with
   a UI walks its life cycle on the happy path; a story with a UI part adds or changes one step
   of that journey instead of a file of its own. Setup goes through the API, not through
   clicks. `smoke` runs on every commit, the journeys before a deploy.
7. **Names and traceability.** A test function is named after the scenario's statement,
   translated to English (`test_deadline_is_overdue_from_due_date`); the ID stands in the
   marker. The link FR → test → code is generated from markers and paths, like the context map,
   and never written by hand.

## Considered alternatives

- **Tests at the outermost seam only (classic BDD):** every acceptance test through the API or
  UI, independent of the placement. Rejected: slow, and calculated rules (overdue, IRR) are
  proven far more precisely at the unit level.
- **Tests before the placement:** the test would have to guess where the code goes. Rejected;
  the placement comes first and is fixed by the shell.
- **Writing tests and implementation in one loop (Pocock's `tdd` alone):** tests would come
  about without a review against the scenarios. Rejected; `tdd` stays the implementation loop
  and the reference for what a good test is.
- **`xfail(strict=True)` for tests committed before the implementation:** keeps the suite
  green, but needs function-local imports (a missing module fails at collection, not inside
  the test). Rejected while tests and implementation land in one commit.
- **A test per repository, endpoint and migration file:** duplicates what the scenario tests
  already prove and makes refactorings more expensive. Rejected; only facades, as the contract
  between contexts, get interface tests.
- **One end-to-end test per story:** stories are changes, not state, so the number of tests
  would only grow, and so would the run time. Rejected in favour of journeys that follow the
  living state of a business object.

## Consequences

- The feature workflow in `CLAUDE.md` is `/problem-definition` → `/implement-story`, which runs
  `solution-definition`, `test-definition`, Pocock's `tdd` and `code-review`.
- `domain-model/solution-space/structure.md` holds the operative rules: levels, paths, markers,
  journeys.
- FR type *Data Migration* is added to `.claude/skills/fr-writer/references/fr-types.md`.
- Existing tests, scenarios without tests, the generator for traceability, the global migration
  test and the restructuring of `frontend/e2e/` into journeys per business object are tracked
  in `refactorings/test-strategy-rollout.md`.
