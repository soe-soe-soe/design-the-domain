# FR-deadlines-002: Problemsignale je Projekt

Kontext: deadlines · Typ: Domain Service (Ableitung) · Status: gültig

## Regel

Ein Problemsignal ist eine überfällige Frist oder eine Frist mit Problem. Die Projektübersicht
zählt sie je Projekt.

## Szenarien

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

## Umsetzung

`domain/deadlines/regeln/signals.py` → `count_signals`

## Historie

- US-0005: angelegt (AK1 → S1, AK2 → S2)
