# US-0039: Eine Frist ist erst am Abend ihres Fälligkeitstags überfällig

Status: ready · Topic: Überfälligkeit · createdAt: 2026-10-20

Als Projektleitung möchte ich eine heute fällige Frist erst ab 18 Uhr als überfällig sehen.

## Why

Morgens ist eine heute fällige Frist noch gut zu schaffen; das Signal kam zu früh.

## Content

Eine heute fällige Frist ist erst ab 18 Uhr überfällig.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Überfälligkeit am Abend

  Szenario: AC1 – Heute fällige Frist ist ab 18 Uhr überfällig
    Angenommen eine Frist ist fällig am 16.10.2026
    Wenn es der 16.10.2026, 18:00 Uhr ist
    Dann gilt die Frist als überfällig
```

## Functional requirements

- FR-fristen-001 (edit): AC1 → S1
