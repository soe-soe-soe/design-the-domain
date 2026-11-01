# US-0039: Änderungen einer Frist stehen in ihrer Historie

Status: ready · Topic: Fristhistorie · createdAt: 2026-10-20

Als Projektleitung möchte ich sehen, wann eine Frist geändert wurde.

## Why

Verschobene Fristen fallen sonst nicht auf.

## Content

Jede Änderung einer manuellen Frist wird in ihrer Historie vermerkt.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Änderung in der Historie

  Szenario: AC1 – Ändern vermerkt die Änderung
    Angenommen eine manuelle Frist „Nachreichung“ fällig am 15.11.2026
    Wenn sie auf den 01.12.2026 geändert wird
    Dann nennt ihre Historie die Änderung
```

## Functional requirements

- FR-fristen-009 (edit): AC1 → S6
