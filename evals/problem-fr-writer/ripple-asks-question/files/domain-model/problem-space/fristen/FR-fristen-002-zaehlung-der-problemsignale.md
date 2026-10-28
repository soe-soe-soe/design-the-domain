# FR-fristen-002: Problemsignale je Projekt

Subdomain: fristen · Business object: – · Type: Domain Service · Status: valid

## Rule

Ein Problemsignal ist eine überfällige Frist oder eine Frist mit Problem. Die Projektübersicht
zählt sie je Projekt.

## Scenarios

```gherkin
# language: de
Funktionalität: Problemsignale je Projekt

  @US-0005
  Szenario: S1 – Heute fällige Frist zählt als Problemsignal
    Angenommen ein Projekt hat als einzige offene Frist eine Frist fällig am 16.10.2026
    Wenn heute der 16.10.2026 ist
    Dann zählt das Projekt 1 Problemsignal

  @US-0005
  Szenario: S2 – Überfällige Frist mit Problem zählt doppelt
    Angenommen ein Projekt hat eine offene Frist mit Problem, fällig am 10.10.2026
    Wenn heute der 16.10.2026 ist
    Dann zählt das Projekt 2 Problemsignale
```

## History

- US-0005: created (AC1 → S1, AC2 → S2)
