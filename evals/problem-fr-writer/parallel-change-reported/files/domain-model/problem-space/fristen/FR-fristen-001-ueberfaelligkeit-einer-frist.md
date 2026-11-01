# FR-fristen-001: Überfälligkeit einer Frist

Subdomain: fristen · Business object: – · Type: Domain Service · Status: valid

## Rule

Eine Frist ist überfällig, wenn ihr Fälligkeitsdatum heute oder früher liegt. Eine Frist ohne
Fälligkeitsdatum ist nie überfällig.

## Scenarios

```gherkin
# language: de
Funktionalität: Überfälligkeit einer Frist

  @US-0007
  Szenario: S1 – Heute fällige Frist ist überfällig
    Angenommen eine Frist ist fällig am 16.10.2026
    Wenn heute der 16.10.2026 ist
    Dann gilt die Frist als überfällig

  @US-0007
  Szenario: S2 – Frist ohne Datum ist nie überfällig
    Angenommen eine Frist hat kein Fälligkeitsdatum
    Wenn heute der 16.10.2026 ist
    Dann gilt die Frist nicht als überfällig
```
