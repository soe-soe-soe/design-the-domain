# From scenario to test

Worked examples of the rules in `SKILL.md` and `‹structure›`
(section Tests), taken from a Python backend (pytest, FastAPI) with a Playwright UI; another
stack follows the same pattern with its own `‹structure›`. Scenarios follow
`‹problem-space-language›`, code `‹solution-space-language›`; both are English here. Paths are relative to the backend root; the context `deadlines` is shown as if
migrated.

## Unit: a Scenario Outline of a domain service

```gherkin
  @US-0061 @planned
  Scenario Outline: S2 – Problem signals count overdue deadlines and evidences with a problem
    Given a project has <overdue> overdue deadlines and <problems> evidences with a problem
    When its problem signals are counted
    Then they show <signals> problem signals

    Examples:
      | overdue | problems | signals |
      | 0       | 0        | 0       |
      | 2       | 1        | 3       |
```

`tests/domain/deadlines/model/services/test_problem_signals.py`:

```python
import pytest

from domain.deadlines.model.services.problem_signals import count_problem_signals


@pytest.mark.fr("FR-deadlines-002/S2")
@pytest.mark.parametrize(
    ("overdue", "problems", "signals"),
    [
        (0, 0, 0),
        (2, 1, 3),
    ],
)
def test_problem_signals_count_overdue_deadlines_and_problem_evidences(overdue, problems, signals):
    assert count_problem_signals(overdue_deadlines=overdue, problem_evidences=problems) == signals
```

- One scenario, one test: the Examples become the parameters, row by row, as literals.
- Given → the arguments, When → the one call, Then → one assertion.
- No fixture: a unit test constructs what it needs.

## Integration: a command through its endpoint

```gherkin
  @US-0062 @planned
  Scenario: S1 – A ticked-off deadline is done
    Given an open manual deadline "Submit building application" is due on 2026-11-20
    When it is ticked off on 2026-11-18
    Then it is done
    And its completion date is 2026-11-18
```

`tests/domain/deadlines/aggregates/manual_deadline/application/commands/test_complete_deadline.py`:

```python
from datetime import date

import pytest


@pytest.mark.fr("FR-deadlines-009/S3")
async def test_completed_deadline_is_done(api_client, make_manual_deadline, deadlines_facade):
    deadline = await make_manual_deadline(title="Submit building application", due_on=date(2026, 11, 20))

    response = await api_client.post(
        f"/deadlines/{deadline.id}/complete", json={"completed_on": "2026-11-18"}
    )

    assert response.status_code == 200
    completed = await deadlines_facade.get_deadline(deadline.id)
    assert completed.done is True
    assert completed.completed_on == date(2026, 11, 18)
```

- The test lives at the path of the command, but acts through its endpoint (the seam).
- What the scenario names (title, due date, day of completion) stands in the test;
  `make_manual_deadline` fills the rest with defaults, `api_client` and `deadlines_facade` are
  wiring.
- Two Then lines check one behaviour: one test, two assertions on the same result.
- The result is read through the facade, not through the repository or SQL.

## Integration: a policy across a context boundary

```gherkin
  @US-0063 @planned
  Scenario: S1 – A done deadline of an evidence stands in its history
    Given the evidence "Species protection report" has an open deadline
    When the deadline is ticked off
    Then the history of the evidence names the done deadline
```

`tests/domain/permits/aggregates/evidence/application/policies/test_on_deadline_done.py`:

```python
import pytest

from domain.deadlines.facade.facade import DeadlinesFacade


@pytest.mark.fr("FR-permits-012/S1")
async def test_done_deadline_appears_in_evidence_history(
    deadlines_facade: DeadlinesFacade, make_evidence, make_manual_deadline, permits_facade
):
    evidence = await make_evidence(title="Species protection report")
    deadline = await make_manual_deadline(evidence_id=evidence.id, title="Request report")

    await deadlines_facade.complete_deadline(deadline.id)

    history = (await permits_facade.get_evidence(evidence.id)).history
    assert any("Request report" in entry for entry in history)
```

- The test lives at the path of the policy (in the aggregate it changes), but acts through the
  command that raises the event – a test calling the policy directly would not prove that the
  event triggers it.
- Across a context boundary, the command is reached through the triggering context's facade,
  and the effect is read through the changed context's facade.

## Journey step

A story that changes what a user does or sees adds one step to the journey of its business
object; it does not get a spec file of its own.

`frontend/e2e/journeys/deadlines/manual-deadline.spec.ts`, inside the existing
`test.describe.serial`:

```ts
test("deadline is ticked off", { tag: "@US-0062" }, async () => {
  await deadlinesPage.completeDeadline("Submit building application");

  await expect(deadlinesPage.deadlineRow("Submit building application")).toContainText("Done");
});
```

- Only the happy path; the edge cases stay in the backend tests.
- New page-object methods (`completeDeadline`) go into the page object of the module, locating
  by role and label or text as the UI shows them.
- The step continues where the previous step left the business object; data it needs beyond
  that is set up through the API in `beforeAll`, not by clicking.
