# US-0048: Nachbesserung nach Ablehnung

Status: ready · Topic: Nachbesserung · Date: 2026-10-26

Als Projektleiter möchte ich sehen, dass ein Antrag nachgebessert werden muss, sobald einer seiner Nachweise abgelehnt wurde.

## Why

Ein abgelehnter Nachweis hält den ganzen Antrag auf; das soll am Antrag selbst sichtbar sein.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Nachbesserung nach Ablehnung

  Szenario: AC1 – Ein abgelehnter Nachweis schickt seinen Antrag in die Nachbesserung
    Angenommen ein eingereichter Antrag hat einen Nachweis in Prüfung
    Wenn der Nachweis abgelehnt wird
    Dann ist der Antrag in Nachbesserung
```
