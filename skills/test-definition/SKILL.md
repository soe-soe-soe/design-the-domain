---
name: test-definition
description: Writes the tests of a placed story before its implementation – one scenario test per planned FR scenario, interface tests for facade methods, migration tests, the journey step for a UI change – red against the shell of solution-definition. Use as the step after solution-definition in /pts:story-workflow, or when the user wants the tests of a story written first.
---

# Test-Definition

You turn the scenarios of a story into tests before the code exists. The scenario is the
specification; the test makes it executable (Specification by Example). Where each test goes,
at which level and with which marker follows from `‹structure›`,
section Tests; why, from `‹test-strategy-adr›`. What a good test is comes from the skill `pts:tdd`.

Your input is the story and the placement report of `pts:solution-definition` from the same
session, with its shell built (`Shell` section, `Questions: none`). Without it, stop and say so.

You write tests and test code only: files under `‹backend-tests›`, `‹e2e-journeys›` and `‹e2e-pages›`. You never
touch production code, the problem space or the glossaries. Code and comments are in `‹solution-space-language›`.
You ask nothing; what you cannot test you report.

**Project config.** Read `.claude/pts.md` in the project root before anything else; a name in
angle quotes (`‹requirements›`) is one of its keys. Without the file, stop and point the user to the
template `${CLAUDE_PLUGIN_ROOT}/templates/config.md`.

## Steps

1. **Read the situation.** The story, every scenario tagged with it in the planned FR files
   (`planned/` below the FR folders; changed, new and `@obsolete` ones, and for a change line
   `Kind: deletion` every scenario of the active FR), the active FRs they change, the placement report, `‹structure›`, `‹test-strategy-adr›`, the shell files, the shared
   fixtures in `‹test-fixtures›` and the `conftest.py` files on the way to each test
   path (use their fixtures, add missing ones there), and existing tests that already carry a marker of these scenarios. For a story with
   a UI change also the journey of its business object and the page objects in
   `‹e2e-pages›`.

2. **Load the craft.** Call the Skill tool with `pts:tdd`. Follow what it says a good test is,
   its anti-patterns, its mocking rules and its seams (agreed in `‹structure›`). You **do not run
   the loop**: no production code, no green phase – writing the scenario tests first is the
   exception `tdd` names.

3. **Write a scenario test per planned scenario.**
   Worked examples for unit, command, policy and journey:
   [references/scenario-to-test.md](references/scenario-to-test.md); read it before the first test.
   - Level, seam and path by the table in `‹structure›`; the test imports the building block
     from the path of the placement.
   - Name and marker by `‹structure›`; one main test per scenario. A Scenario Outline becomes
     one test parametrised over its Beispiele.
   - Given → arrange, When → act (exactly one call at the seam), Then → assert. Expected
     values are the literals of the Then steps, never computed the way the code would.
   - Test data by the rule in `‹structure›`: what the scenario names stands in the test body,
     wiring comes from fixtures, a builder fixture `make_<aggregate>` fills the rest.
   - The marker names the scenario as `FR-…/Sn` with the number of the active FR – the planned
     file keeps it – never the path of the planned file.
   - A scenario that already has a test with its marker: change that test where it is – even
     at a path that does not mirror the code yet, moving it belongs to the context's
     migration – and rename it after the new statement; do not add a second test.
   - An `@obsolete` scenario: delete its test, and the file if nothing else is left in it.
   - **Data Migration:** downgrade to the revision before the shell's migration, seed the old
     state, upgrade, and check the new state. The seam is the stored data itself, so reading
     it directly is right here.

4. **Write an interface test per facade method** under `Interfaces` of the placement: through
   the facade, with the database, marker `story`, at the path `‹structure›` gives.
   Endpoints, repositories and schemas get none (`‹structure›`).

5. **Extend the journey** if an AC changes what a user does or sees in the UI. Add or change one
   step in `‹e2e-journeys›/<subdomain>/<business-object>`, tagged with the story;
   create the journey only if the business object has none yet. Drive the page through page
   objects and locate by role and label or text from the AC or glossary. Setup the step
   does not cover goes through the API. A selector may still change with the UI; the assertion
   may not.

6. **Check red for the right reason.** `‹test-collect›` collects without
   errors; run the new and changed tests: each fails at the shell's `‹not-implemented›`
   or with its assertion – never with an import, fixture or syntax error. For a journey,
   `‹e2e-list›` lists the step.

You are done when every planned scenario has its red main test or is reported as untestable,
every facade method of the placement has its interface test, the journey has the story's step
if the story changes the UI, and no production code is changed.

## Untestable

A scenario is untestable when the test would have to guess. Write no test for it and report it
with the reason and where it goes back:
- **problem space** – the Then step has no observable value (no number, status or text to assert),
  or the Angenommen lacks a value the test needs; the grilling missed it.
- **solution-definition** – the placement gives it no seam, or a value the test must store or
  read (e.g. the stored value of a status or kind) is named neither in the glossary's
  `Identifier` column nor in the code.

Test infrastructure is yours: fixtures and `conftest.py` under the test folders; a new module
in `‹test-fixtures›` is registered in the `conftest.py` of `‹backend-tests›`. What lies
outside them (migration or test runner configuration, production code) you do not create; a scenario
that needs it is untestable with the source solution-definition.

Even without a single test written, your last message is the report.

## Report

Your last message, exactly in this form; `/pts:story-workflow` shows it to the user for review:

Example (from a Python backend with a TypeScript UI):

```
Tests US-0042: Validity of expert reports
| Ref | Kind | Level | Test | Red because |
|---|---|---|---|---|
| FR-permits-020/S1 | scenario | Unit | tests/domain/permits/aggregates/evidence/model/services/test_validity_end.py::test_report_is_valid_for_five_years | not-implemented |
| FR-permits-022/S1 | scenario (Data Migration) | Integration | tests/ops/migrations/versions/test_<rev>_evidence_valid_until.py::test_existing_reports_stay_unlimited | assertion |
| PermitsFacade.get_expiring_evidences | interface | Integration | tests/domain/permits/facade/test_facade.py::test_get_expiring_evidences_returns_reports_due_within_period | not-implemented |
| US-0042 | journey step | E2E | frontend/e2e/journeys/permits/evidence.spec.ts › "expert report shows its validity end" | not run |
Removed: tests/domain/…::test_… (FR-permits-007/S3 obsolete)
Untestable:
- FR-permits-021/S2 (problem space): Then "is clearly highlighted" has no checkable value
```

Omit `Removed` when empty; `Untestable: none` when everything has a test.
