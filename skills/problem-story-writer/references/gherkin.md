# Gherkin for acceptance criteria

Acceptance criteria are business text in `‹problem-space-language›`. Each scenario later becomes
exactly one test, so each must be testable on its own.

## Keywords

The keywords are Gherkin's dialect of `‹problem-space-language›`; `# language: <code>` (`en`, `de`,
…) is the first line of the block. The rules below name the English keywords; the examples are
written in German (`# language: de`):

| English | German |
|---|---|
| Feature | Funktionalität |
| Background | Grundlage |
| Scenario | Szenario |
| Scenario Outline | Szenariogrundriss |
| Examples | Beispiele |
| Given | Angenommen |
| When | Wenn |
| Then | Dann |
| And / But | Und / Aber |

## Rules

- **Business, not clicks.** Write what happens, not what is clicked: "Wenn die Frist erledigt
  wird" instead of "Wenn ich auf den Haken klicke". UI details only when the UI itself is the
  requirement.
- **One behaviour per scenario.** Exactly one `When`; the `Then` steps check its consequences. Two
  triggers make two scenarios.
- **Concrete example values.** Real dates, amounts and statuses instead of "ein Datum" or
  "X". The expected value in the `Then` comes from the decision, not from a calculation the
  code would make as well.
- **Value tables as Scenario Outline.** If the same rule is checked with several values
  (boundaries, calculations), write a `Scenario Outline` with `Examples` instead of several
  near-identical scenarios.
- **Glossary terms.** Use the terms of the subdomain glossaries, not the words after
  "Avoid: …".
- **Boundaries and counter-cases.** If a rule applies from a threshold, the case just below it
  belongs in. If it applies to a tenant, status or role, the excluded case belongs in.
- **Name = number + statement.** `Scenario: AC2 – Frist ohne Datum ist nie überfällig`. The
  statement is the expected behaviour, not a topic ("Fristen ohne Datum").

## Example: Scenario Outline

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
