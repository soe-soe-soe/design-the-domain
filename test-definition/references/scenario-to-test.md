# From scenario to test

Worked examples of the rules in `SKILL.md` and `domain-model/solution-space/structure.md`
(section Tests). The scenarios are German, the code is English. Paths are relative to
`backend/`; the context `deadlines` is shown as if migrated.

## Unit: a Szenariogrundriss of a domain service

```gherkin
  @US-0061 @planned
  Szenariogrundriss: S2 – Problemsignale zählen überfällige Fristen und Nachweise mit Problem
    Angenommen ein Projekt hat <überfällig> überfällige Fristen und <probleme> Nachweise mit Problem
    Wenn seine Problemsignale gezählt werden
    Dann zeigen sie <signale> Problemsignale

    Beispiele:
      | überfällig | probleme | signale |
      | 0          | 0        | 0       |
      | 2          | 1        | 3       |
```

`tests/domain/deadlines/model/services/test_problem_signals.py`:

```python
import pytest

from domain.deadlines.model.services.problem_signals import count_problem_signals


@pytest.mark.fr("FR-fristen-002/S2")
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

- One scenario, one test: the Beispiele become the parameters, row by row, as literals.
- Angenommen → the arguments, Wenn → the one call, Dann → one assertion.
- No fixture: a unit test constructs what it needs.

## Integration: a command through its endpoint

```gherkin
  @US-0062 @planned
  Szenario: S1 – Eine abgehakte Frist ist erledigt
    Angenommen eine offene manuelle Frist „Bauantrag nachreichen“ ist fällig am 20.11.2026
    Wenn sie am 18.11.2026 abgehakt wird
    Dann ist sie erledigt
    Und ihr Erledigungsdatum ist der 18.11.2026
```

`tests/domain/deadlines/aggregates/manual_deadline/application/commands/test_complete_deadline.py`:

```python
from datetime import date

import pytest


@pytest.mark.fr("FR-fristen-009/S3")
async def test_completed_deadline_is_done(api_client, make_manual_deadline, deadlines_facade):
    deadline = await make_manual_deadline(title="Bauantrag nachreichen", due_on=date(2026, 11, 20))

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
- Two Dann lines check one behaviour: one test, two assertions on the same result.
- The result is read through the facade, not through the repository or SQL.

## Integration: a policy across a context boundary

```gherkin
  @US-0063 @planned
  Szenario: S1 – Eine erledigte Frist eines Nachweises steht in seiner Historie
    Angenommen der Nachweis „Artenschutzgutachten“ hat eine offene Frist
    Wenn die Frist abgehakt wird
    Dann nennt die Historie des Nachweises die erledigte Frist
```

`tests/domain/permits/aggregates/evidence/application/policies/test_on_deadline_done.py`:

```python
import pytest

from domain.deadlines.facade.facade import DeadlinesFacade


@pytest.mark.fr("FR-genehmigung-012/S1")
async def test_done_deadline_appears_in_evidence_history(
    deadlines_facade: DeadlinesFacade, make_evidence, make_manual_deadline, permits_facade
):
    evidence = await make_evidence(title="Artenschutzgutachten")
    deadline = await make_manual_deadline(evidence_id=evidence.id, title="Gutachten anfordern")

    await deadlines_facade.complete_deadline(deadline.id)

    history = (await permits_facade.get_evidence(evidence.id)).history
    assert any("Gutachten anfordern" in entry for entry in history)
```

- The test lives at the path of the policy (in the aggregate it changes), but acts through the
  command that raises the event – a test calling the policy directly would not prove that the
  event triggers it.
- Across a context boundary, the command is reached through the triggering context's facade,
  and the effect is read through the changed context's facade.

## Journey step

A story that changes what a user does or sees adds one step to the journey of its business
object; it does not get a spec file of its own.

`frontend/e2e/journeys/fristen/manuelle-frist.spec.ts`, inside the existing
`test.describe.serial`:

```ts
test("Frist wird abgehakt", { tag: "@US-0062" }, async () => {
  await deadlinesPage.completeDeadline("Bauantrag nachreichen");

  await expect(deadlinesPage.deadlineRow("Bauantrag nachreichen")).toContainText("Erledigt");
});
```

- Only the happy path; the edge cases stay in the backend tests.
- New page-object methods (`completeDeadline`) go into the page object of the module, locating
  by role and German label or text.
- The step continues where the previous step left the business object; data it needs beyond
  that is set up through the API in `beforeAll`, not by clicking.
