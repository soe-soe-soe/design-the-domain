# US-0044: Abgelehnte Nachweise als Problemsignal

Status: ready · Topic: Abgelehnte Nachweise als Problemsignal · createdAt: 2026-10-26

Als Projektleiter möchte ich abgelehnte Nachweise in den Problemsignalen eines Projekts sehen.

## Why

Ein abgelehnter Nachweis gefährdet den Zeitplan; er soll so auffallen wie ein Nachweis mit Problem.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Problemsignale

  Szenario: AC1 – Ein abgelehnter Nachweis zählt als Problemsignal
    Angenommen ein Projekt hat einen abgelehnten Nachweis und sonst keine Probleme
    Wenn die Problemsignale des Projekts abgefragt werden
    Dann zeigen sie 1 Problem
```

## Functional requirements

- FR-fristen-013 (new): AC1 → S1
