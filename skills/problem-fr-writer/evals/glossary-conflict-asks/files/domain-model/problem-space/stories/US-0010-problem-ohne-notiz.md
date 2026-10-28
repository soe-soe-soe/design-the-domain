# US-0010: Problem an einer Frist ohne Notiz kennzeichnen

Status: ready · Topic: Probleme an Fristen · Date: 2026-10-25

Als Projektleitung möchte ich eine Frist mit einem Klick als Problem kennzeichnen.

## Why

Im Termin mit der Behörde bleibt keine Zeit, eine Notiz zu tippen; die Kennzeichnung soll sofort gehen.

## Content

Eine Frist lässt sich ohne Notiz als Problem kennzeichnen.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Problem an einer Frist ohne Notiz kennzeichnen

  Szenario: AC1 – Problem ohne Notiz setzen
    Angenommen eine offene manuelle Frist ohne Notiz
    Wenn die Projektleitung sie als Problem kennzeichnet
    Dann ist die Frist als Problem gekennzeichnet
    Und die Frist hat weiterhin keine Notiz
```
