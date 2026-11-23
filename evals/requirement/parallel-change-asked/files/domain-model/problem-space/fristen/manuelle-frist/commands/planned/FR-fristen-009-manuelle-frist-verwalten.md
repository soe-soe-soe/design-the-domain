# FR-fristen-009: Manuelle Frist verwalten

Subdomain: fristen · Business object: manuelle-frist · Type: Command · Status: planned

## Changes

- US-0039 · Kind: edit · Rule: unchanged
- US-0050 · Kind: edit · Rule: unchanged

## Scenarios

```gherkin
# language: de
Funktionalität: Manuelle Frist verwalten

  @US-0039 @planned @base-US-0042
  Szenario: S6 – Ändern setzt Angaben und Bezug neu und vermerkt die Änderung
    Angenommen eine manuelle Frist „Nachreichung“ am Nachweis Schallgutachten fällig am 15.11.2026
    Wenn sie geändert wird auf „Nachreichung Schall“, fällig am 01.12.2026
    Dann heißt sie „Nachreichung Schall“ und ist fällig am 01.12.2026
    Und ihre Historie nennt die Änderung

  @US-0050 @planned @base-US-0042
  Szenario: S6 – Ändern der Fälligkeit setzt die Erinnerung zurück
    Angenommen Petra wurde zu einer manuellen Frist fällig am 23.10.2026 erinnert
    Wenn die Fälligkeit auf den 06.11.2026 geändert wird
    Dann gilt Petra für diese Frist als nicht erinnert
```
