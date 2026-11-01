# FR-fristen-001: Überfälligkeit einer Frist

Subdomain: fristen · Business object: – · Type: Domain Service · Status: planned

## Changes

- US-0049 · Kind: edit · Rule: unchanged

## Scenarios

```gherkin
# language: de
Funktionalität: Überfälligkeit einer Frist

  @US-0049 @planned @base-existing
  Szenario: S1 – Am Fälligkeitstag ist eine Frist noch nicht überfällig
    Angenommen eine offene Frist ist fällig am 16.10.2026
    Wenn heute der 16.10.2026 ist
    Dann ist die Frist nicht überfällig
```
