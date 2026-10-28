# FR-fristen-001: Überfälligkeit einer Frist

Subdomain: fristen · Business object: – · Type: Domain Service · Status: valid

## Rule

Eine offene Frist ist überfällig, wenn ihr Zieltermin vor heute liegt.

## Scenarios

```gherkin
# language: de
Funktionalität: Überfälligkeit einer Frist

  @US-0049 @planned
  Szenario: S1 – Am Fälligkeitstag ist eine Frist noch nicht überfällig
    Angenommen eine offene Frist ist fällig am 16.10.2026
    Wenn heute der 16.10.2026 ist
    Dann ist die Frist nicht überfällig

  @existing
  Szenario: S2 – Nach dem Fälligkeitstag ist eine Frist überfällig
    Angenommen eine offene Frist ist fällig am 15.10.2026
    Wenn heute der 16.10.2026 ist
    Dann ist die Frist überfällig

  @existing
  Szenario: S3 – Vor dem Fälligkeitstag ist eine Frist nicht überfällig
    Angenommen eine offene Frist ist fällig am 17.10.2026
    Wenn heute der 16.10.2026 ist
    Dann ist die Frist nicht überfällig

  @existing
  Szenario: S4 – Eine Frist ohne Zieltermin ist nie überfällig
    Angenommen eine offene Frist hat keinen Zieltermin
    Wenn heute der 16.10.2026 ist
    Dann ist die Frist nicht überfällig
```

## History

- existing: created (problem-init, 2026-10-26)
- US-0049: S1 changed (AC1 → S1)
