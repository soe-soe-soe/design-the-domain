# FR-fristen-001: Überfälligkeit einer Frist

Subdomain: fristen · Business object: – · Type: Domain Service · Status: planned

## Changes

- US-0039 · Kind: edit · Rule: unchanged

## Scenarios

```gherkin
# language: de
Funktionalität: Überfälligkeit einer Frist

  @US-0039 @planned @base-US-0007
  Szenario: S1 – Heute fällige Frist ist ab 18 Uhr überfällig
    Angenommen eine Frist ist fällig am 16.10.2026
    Wenn es der 16.10.2026, 18:00 Uhr ist
    Dann gilt die Frist als überfällig
```
