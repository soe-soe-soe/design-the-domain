# Gherkin for acceptance criteria

Acceptance criteria are business text in German. Each scenario later becomes exactly one test,
so each must be testable on its own.

## Keywords (German)

`# language: de` is the first line of the block.

| German | English |
|---|---|
| Funktionalität | Feature |
| Grundlage | Background |
| Szenario | Scenario |
| Szenariogrundriss | Scenario Outline |
| Beispiele | Examples |
| Angenommen | Given |
| Wenn | When |
| Dann | Then |
| Und / Aber | And / But |

## Rules

- **Business, not clicks.** Write what happens, not what is clicked: "Wenn die Frist erledigt
  wird" instead of "Wenn ich auf den Haken klicke". UI details only when the UI itself is the
  requirement.
- **One behaviour per scenario.** Exactly one `Wenn`; the `Dann` check its consequences. Two
  triggers make two scenarios.
- **Concrete example values.** Real dates, amounts and statuses instead of "ein Datum" or
  "X". The expected value in the `Dann` comes from the decision, not from a calculation the
  code would make as well.
- **Value tables as Szenariogrundriss.** If the same rule is checked with several values
  (boundaries, calculations), write a `Szenariogrundriss` with `Beispiele` instead of several
  near-identical scenarios.
- **Glossary terms.** Use the terms of the subdomain glossaries, not the words after
  "Avoid: …".
- **Boundaries and counter-cases.** If a rule applies from a threshold, the case just below it
  belongs in. If it applies to a tenant, status or role, the excluded case belongs in.
- **Name = number + statement.** `Szenario: AC2 – Frist ohne Datum ist nie überfällig`. The
  statement is the expected behaviour, not a topic ("Fristen ohne Datum").

## Example: Szenariogrundriss

```gherkin
# language: de
Funktionalität: Überfällige Fristen

  Szenariogrundriss: AC1 – Überfällig ab dem Fälligkeitstag
    Angenommen eine Frist ist fällig am <fällig>
    Wenn heute der 16.10.2026 ist
    Dann ist die Frist <ergebnis>

    Beispiele:
      | fällig     | ergebnis         |
      | 15.10.2026 | überfällig       |
      | 16.10.2026 | überfällig       |
      | 17.10.2026 | nicht überfällig |
```
