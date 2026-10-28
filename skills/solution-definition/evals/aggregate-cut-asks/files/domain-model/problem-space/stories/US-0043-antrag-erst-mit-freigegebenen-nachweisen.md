# US-0043: Antrag erst mit freigegebenen Nachweisen einreichen

Status: ready · Topic: Antrag erst mit freigegebenen Nachweisen einreichen · Date: 2026-10-26

Als Projektleiter möchte ich, dass ein Antrag erst eingereicht werden kann, wenn alle seine Nachweise freigegeben sind.

## Why

Ein unvollständiger Antrag kostet Wochen in der Vollständigkeitsprüfung der Behörde.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Antrag einreichen

  Szenario: AC1 – Ein Antrag mit nicht freigegebenem Nachweis wird nicht eingereicht
    Angenommen ein Antrag hat einen Nachweis im Status In Prüfung
    Wenn der Antrag eingereicht wird
    Dann wird das Einreichen zurückgewiesen
```
