# US-0007: Überfällige Fristen markieren

Status: done · Topic: Fristen · createdAt: 2026-09-02 · doneAt: 2026-09-02

Als Projektleitung möchte ich überfällige Fristen erkennen.

## Why

Fristen sollen nicht unbemerkt verstreichen.

## Content

Fristen, deren Fälligkeitsdatum heute oder früher liegt, gelten als überfällig.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Überfällige Fristen markieren

  Szenario: AC1 – Heute fällige Frist ist überfällig
    Angenommen eine Frist ist fällig am 16.10.2026
    Wenn heute der 16.10.2026 ist
    Dann gilt die Frist als überfällig

  Szenario: AC2 – Frist ohne Datum ist nie überfällig
    Angenommen eine Frist hat kein Fälligkeitsdatum
    Wenn heute der 16.10.2026 ist
    Dann gilt die Frist nicht als überfällig
```
