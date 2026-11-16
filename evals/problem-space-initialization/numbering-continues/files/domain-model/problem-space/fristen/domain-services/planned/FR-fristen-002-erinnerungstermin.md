# FR-fristen-002: Erinnerungstermin

Subdomain: fristen · Business object: – · Type: Domain Service · Status: planned

## Changes

- US-0050 · Kind: new · Rule: changed

## Rule

Der Erinnerungstermin einer offenen Frist liegt sieben Kalendertage vor ihrer Fälligkeit.

## Scenarios

```gherkin
# language: de
Funktionalität: Erinnerungstermin

  @US-0050 @planned
  Szenario: S1 – Erinnerungstermin sieben Tage vorher
    Angenommen eine offene Frist ist fällig am 23.10.2026
    Wenn der Erinnerungstermin berechnet wird
    Dann ist er der 16.10.2026
```
