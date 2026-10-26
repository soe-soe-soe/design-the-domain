---
name: test-definition
description: Writes the tests of a placed story before its implementation – one scenario test per planned FR scenario, interface tests for facade methods, migration tests, the journey step for a UI change – red against the shell of solution-definition. Use as the step after solution-definition in /story-workflow, or when the user wants the tests of a story written first.
---

# Test-Definition

You turn the scenarios of a story into tests before the code exists. The scenario is the
specification; the test makes it executable (Specification by Example). Where each test goes,
at which level and with which marker follows from `domain-model/solution-space/structure.md`,
section Tests; why, from ADR 012. What a good test is comes from Pocock's skill `tdd`.

Your input is the story and the placement report of `solution-definition` from the same
session, with its shell built (`Shell` section, `Questions: none`). Without it, stop and say so.

You write tests and test code only: files under `backend/tests/` and `frontend/e2e/`. You never
touch production code, the problem space or the glossaries. Code and comments are English.
You ask nothing; what you cannot test you report.

## Steps

1. **Read the situation.** The story, every FR scenario tagged with it (`@planned` and
   `@obsolete`), the placement report, `structure.md`, ADR 012, the shell files, the
   `conftest.py` files on the way to each test path (use their fixtures, add missing ones
   there), and existing tests that already carry a marker of these scenarios. For a story with
   a UI change also the journey of its business object and the page objects in
   `frontend/e2e/pages/`.

2. **Load the craft.** Call the Skill tool with `mattpocock-skills:tdd`. Follow what it says a
   good test is, its anti-patterns and its mocking rules. Two project rules stand above it:
   - The **seams are agreed** by the table in `structure.md`; you do not ask for them.
   - You **do not run the loop**: no production code, no green phase. Writing all tests of a
     story first is no horizontal slicing here – the scenarios are settled in the problem
     space, and the implementation arms them one at a time.

3. **Write a scenario test per planned scenario.**
   - Level, seam and path by the table in `structure.md`; the test imports the building block
     from the path of the placement.
   - Name and marker by `structure.md`; one main test per scenario. A Szenariogrundriss becomes
     one test parametrised over its Beispiele.
   - Angenommen → arrange, Wenn → act (exactly one call at the seam), Dann → assert. Expected
     values are the literals of the Dann, never computed the way the code would.
   - A scenario that already has a test with its marker: change that test, do not add one.
   - An `@obsolete` scenario: delete its test.
   - **Data Migration:** downgrade to the revision before the shell's migration, seed the old
     state, upgrade, and check the new state. The seam is the stored data itself, so reading
     it directly is right here.

4. **Write an interface test per facade method** under `Interfaces` of the placement: through
   the facade, with the database, marker `story`, in the mirrored `facade/test_facade.py`.
   Endpoints, repositories and schemas get none (`structure.md`).

5. **Extend the journey** if an AC changes what a user does or sees in the UI. Add or change one
   step in `frontend/e2e/journeys/<subdomain>/<business-object>.spec.ts`, tagged with the story;
   create the journey only if the business object has none yet. Drive the page through page
   objects and locate by role and German label or text from the AC or glossary. Setup the step
   does not cover goes through the API. A selector may still change with the UI; the assertion
   may not.

6. **Check red for the right reason.** `cd backend && pytest --collect-only -q` collects without
   errors; run the new and changed tests: each fails with `NotImplementedError` from the shell
   or with its assertion – never with an import, fixture or syntax error. For a journey,
   `cd frontend && npx playwright test --list` lists the step.

You are done when every planned scenario has its red main test or is reported as untestable,
every facade method of the placement has its interface test, the journey has the story's step
if the story changes the UI, and no production code is changed.

## Untestable

A scenario is untestable when the test would have to guess. Write no test for it and report it
with the reason and where it goes back:
- **problem space** – the Dann has no observable value (no number, status or text to assert),
  or the Angenommen lacks a value the test needs; the grilling missed it.
- **solution-definition** – the placement gives it no seam, or a value the test must store or
  read (e.g. the stored value of a status or kind) is named neither in the glossary's
  `Identifier` column nor in the code.

Test infrastructure is yours: fixtures and `conftest.py` under the test folders. What lies
outside them (Alembic or pytest configuration, production code) you do not create; a scenario
that needs it is untestable with the source solution-definition.

Even without a single test written, your last message is the report.

## Report

Your last message, exactly in this form; `/story-workflow` shows it to the user for review:

```
Tests US-0042: Gültigkeit von Gutachten
| Ref | Kind | Level | Test | Red because |
|---|---|---|---|---|
| FR-genehmigung-020/S1 | scenario | Unit | tests/unit/domain/permits/aggregates/evidence/model/services/test_validity_end.py::test_report_is_valid_for_five_years | NotImplementedError |
| FR-genehmigung-022/S1 | scenario (Data Migration) | Integration | tests/integration/ops/migrations/versions/test_<rev>_evidence_valid_until.py::test_existing_reports_stay_unlimited | assertion |
| PermitsFacade.get_expiring_evidences | interface | Integration | tests/integration/domain/permits/facade/test_facade.py::test_get_expiring_evidences_returns_reports_due_within_period | NotImplementedError |
| US-0042 | journey step | E2E | frontend/e2e/journeys/genehmigung/nachweis.spec.ts › "Gutachten zeigt sein Gültigkeitsende" | not run |
Removed: tests/unit/…::test_… (FR-genehmigung-007/S3 obsolete)
Untestable:
- FR-genehmigung-021/S2 (problem space): Dann „wird deutlich hervorgehoben“ hat keinen prüfbaren Wert
```

Omit `Removed` when empty; `Untestable: none` when everything has a test.
