# FR-fristen-014: Erinnerungen abbestellen

Subdomain: fristen · Business object: manuelle-frist · Type: Command · Status: planned

## Changes

- US-0051 · Kind: new · Rule: changed

## Rule

Ein Nutzer kann Fristerinnerungen für sich abbestellen; danach bekommt er keine Erinnerungen mehr.

## Scenarios

```gherkin
# language: de
Funktionalität: Erinnerungen abbestellen

  @US-0051 @planned
  Szenario: S1 – Abbestellte Erinnerungen werden nicht verschickt
    Angenommen Petra hat Fristerinnerungen abbestellt
    Und eine offene Frist von Petra ist fällig in 7 Tagen
    Wenn die Erinnerungen verschickt werden
    Dann erhält Petra keine Erinnerung
```
