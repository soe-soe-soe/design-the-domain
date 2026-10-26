# US-0007: Überfällige Fristen markieren

Status: umgesetzt · Thema: Fristen · Datum: 2026-09-02

Als Projektleitung möchte ich überfällige Fristen erkennen.

## Warum

Fristen sollen nicht unbemerkt verstreichen.

## Inhalt

Fristen, deren Fälligkeitsdatum heute oder früher liegt, gelten als überfällig.

## Akzeptanzkriterien

```gherkin
# language: de
Funktionalität: Überfällige Fristen markieren

  Szenario: AK1 – Heute fällige Frist ist überfällig
    Angenommen eine Frist ist fällig am 16.10.2026
    Wenn heute der 16.10.2026 ist
    Dann gilt die Frist als überfällig

  Szenario: AK2 – Frist ohne Datum ist nie überfällig
    Angenommen eine Frist hat kein Fälligkeitsdatum
    Wenn heute der 16.10.2026 ist
    Dann gilt die Frist nicht als überfällig
```
