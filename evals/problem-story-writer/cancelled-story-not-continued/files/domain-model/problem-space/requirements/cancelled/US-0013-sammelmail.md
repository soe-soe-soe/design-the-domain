# US-0013: Wöchentliche Sammelmail

Status: cancelled · Topic: Sammelmail · createdAt: 2026-10-12

Als Verantwortliche möchte ich eine wöchentliche Sammelmail statt einzelner Erinnerungen.

## Why

Zu viele einzelne Mails.

## Content

Freitags eine Mail mit allen Fristen der kommenden Woche.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Sammelmail

  Szenario: AC1 – Sammelmail am Freitag
    Angenommen Petra hat zwei offene Fristen in der kommenden Woche
    Wenn Freitag ist
    Dann erhält Petra eine Sammelmail mit beiden Fristen
```
