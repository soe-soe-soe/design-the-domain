# FR-fristen-013: Abgelehnte Nachweise als Problemsignal

Subdomain: fristen · Business object: – · Type: Query · Status: valid

## Rule

Die Problemsignale eines Projekts zählen neben Nachweisen mit Problem auch abgelehnte Nachweise, die nicht archiviert sind.

## Scenarios

```gherkin
# language: de
Funktionalität: Abgelehnte Nachweise als Problemsignal

  @US-0044 @planned
  Szenario: S1 – Ein abgelehnter Nachweis zählt als Problemsignal
    Angenommen ein Projekt hat einen abgelehnten Nachweis und sonst keine Probleme
    Wenn die Problemsignale des Projekts abgefragt werden
    Dann zeigen sie 1 Problem
```

## History

- US-0044: created (AC1 → S1)
