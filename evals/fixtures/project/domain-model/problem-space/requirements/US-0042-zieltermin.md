# US-0042: Zieltermin für manuelle Fristen

Status: done · Topic: Zieltermin · createdAt: 2026-10-01 · doneAt: 2026-10-15

Als Verantwortlicher möchte ich einer manuellen Frist einen Zieltermin geben, damit ich vor der Fälligkeit fertig bin.

## Why

Wer erst am Fälligkeitstag liefert, hat keinen Puffer für Rückfragen der Behörde.

## Content

Eine manuelle Frist kann einen Zieltermin vor ihrer Fälligkeit haben; wird die Fälligkeit
verschoben, bleibt der Zieltermin stehen.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Zieltermin für manuelle Fristen

  Szenario: AC1 – Zieltermin nach der Fälligkeit wird abgelehnt
    Angenommen eine manuelle Frist fällig am 15.11.2026
    Wenn Petra den Zieltermin 20.11.2026 setzt
    Dann bleibt die Frist ohne Zieltermin und Petra erfährt, dass der Zieltermin vor der Fälligkeit liegen muss

  Szenario: AC2 – Verschieben lässt den Zieltermin stehen
    Angenommen eine manuelle Frist fällig am 15.11.2026 mit Zieltermin 08.11.2026
    Wenn die Fälligkeit auf den 01.12.2026 geändert wird
    Dann ist sie fällig am 01.12.2026 und ihr Zieltermin bleibt der 08.11.2026
```

## Functional requirements

- FR-fristen-009 (edit): AC1 → S4, AC2 → S6
