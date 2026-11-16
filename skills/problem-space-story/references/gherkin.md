# Gherkin for acceptance criteria

Acceptance criteria are business text in `‹problem-space-language›`. Each scenario later becomes
exactly one test, so each must be testable on its own.

## Keywords

The keywords are Gherkin's dialect of `‹problem-space-language›`; `# language: <code>` (`en`, `de`,
…) is the first line of the block. The rules and examples use the English keywords.

## Rules

- **Business, not clicks.** Write what happens, not what is clicked: "When the deadline is
  done" instead of "When I click the tick". UI details only when the UI itself is the
  requirement.
- **One behaviour per scenario.** Exactly one `When`; the `Then` steps check its consequences. Two
  triggers make two scenarios.
- **Concrete example values.** Real dates, amounts and statuses instead of "a date" or
  "X". The expected value in the `Then` comes from the decision, not from a calculation the
  code would make as well.
- **Value tables as Scenario Outline.** If the same rule is checked with several values
  (boundaries, calculations), write a `Scenario Outline` with `Examples` instead of several
  near-identical scenarios.
- **Glossary terms.** Use the terms of the subdomain glossaries, not the words after
  "Avoid: …".
- **Boundaries and counter-cases.** If a rule applies from a threshold, the case just below it
  belongs in. If it applies to a tenant, status or role, the excluded case belongs in.
- **Name = number + statement.** `Scenario: AC2 – A deadline without a date is never overdue`. The
  statement is the expected behaviour, not a topic ("Deadlines without a date").

## Example: Scenario Outline

```gherkin
# language: en
Feature: Overdue deadlines

  Scenario Outline: AC1 – Overdue from the due date
    Given a deadline is due on <due>
    When today is 2026-10-16
    Then the deadline is <result>

    Examples:
      | due        | result      |
      | 2026-10-15 | overdue     |
      | 2026-10-16 | overdue     |
      | 2026-10-17 | not overdue |
```
