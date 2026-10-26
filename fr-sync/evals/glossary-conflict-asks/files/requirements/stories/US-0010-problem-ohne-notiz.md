# US-0010: Problem an einer Frist ohne Notiz kennzeichnen

Status: bereit · Thema: Probleme an Fristen · Datum: 2026-10-25

Als Projektleitung möchte ich eine Frist mit einem Klick als Problem kennzeichnen.

## Warum

Im Termin mit der Behörde bleibt keine Zeit, eine Notiz zu tippen; die Kennzeichnung soll sofort gehen.

## Inhalt

Eine Frist lässt sich ohne Notiz als Problem kennzeichnen.

## Akzeptanzkriterien

```gherkin
# language: de
Funktionalität: Problem an einer Frist ohne Notiz kennzeichnen

  Szenario: AK1 – Problem ohne Notiz setzen
    Angenommen eine offene manuelle Frist ohne Notiz
    Wenn die Projektleitung sie als Problem kennzeichnet
    Dann ist die Frist als Problem gekennzeichnet
    Und die Frist hat weiterhin keine Notiz
```
