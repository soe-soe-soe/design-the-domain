# FR-fristen-001: Überfällige Frist

Subdomain: fristen · Business object: – · Type: Domain Service · Status: valid

## Rule

Eine Frist ist überfällig, sobald ihr Fälligkeitsdatum verstrichen ist, außer sie ist erledigt.

## Scenarios

```gherkin
# language: de
Funktionalität: Überfällige Frist

  @US-0010
  Szenario: S1 – Verstrichenes Fälligkeitsdatum
    Angenommen eine offene Frist ist fällig am 15.10.2026
    Wenn heute der 16.10.2026 ist
    Dann gilt die Frist als überfällig
```
