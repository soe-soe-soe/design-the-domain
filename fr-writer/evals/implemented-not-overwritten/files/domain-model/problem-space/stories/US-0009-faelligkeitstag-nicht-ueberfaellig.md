# US-0009: Fristen am Fälligkeitstag nicht als überfällig zeigen

Status: ready · Topic: Fristenansicht · Date: 2026-10-25

Als Projektleitung möchte ich eine Frist an ihrem Fälligkeitstag noch nicht als überfällig sehen.

## Why

Am Fälligkeitstag lässt sich die Frist noch fristgerecht erledigen.

## Content

Die Fristenansicht markiert eine Frist erst nach ihrem Fälligkeitstag als überfällig.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Fristen am Fälligkeitstag nicht als überfällig zeigen

  Szenario: AC1 – Am Fälligkeitstag ist die Frist nicht überfällig
    Angenommen eine Frist ist fällig am 16.10.2026
    Wenn heute der 16.10.2026 ist
    Dann gilt die Frist nicht als überfällig
```
