# FR-fristen-013: Fristerinnerung per E-Mail

Subdomain: fristen · Business object: manuelle-frist · Type: Policy · Status: planned

## Changes

- US-0050 · Kind: new · Rule: changed

## Rule

Sieben Kalendertage vor der Fälligkeit einer offenen Frist, manuell oder abgeleitet, bekommt ihr
Verantwortlicher eine E-Mail-Erinnerung; erledigte Fristen werden nicht erinnert.

## Scenarios

```gherkin
# language: de
Funktionalität: Fristerinnerung per E-Mail

  @US-0050 @planned
  Szenario: S1 – Erinnerung sieben Tage vor Fälligkeit
    Angenommen eine offene manuelle Frist ist fällig am 23.10.2026
    Und Petra ist verantwortlich
    Wenn heute der 16.10.2026 ist
    Dann erhält Petra eine E-Mail-Erinnerung zu dieser Frist

  @US-0050 @planned
  Szenario: S2 – Erledigte Frist wird nicht erinnert
    Angenommen eine manuelle Frist ist fällig am 23.10.2026 und erledigt
    Wenn heute der 16.10.2026 ist
    Dann wird keine Erinnerung verschickt

  @US-0050 @planned
  Szenario: S3 – Abgeleitete Fristen werden ebenso erinnert
    Angenommen die Lieferung eines Nachweises ist fällig am 23.10.2026
    Und Petra ist verantwortlich
    Wenn heute der 16.10.2026 ist
    Dann erhält Petra eine E-Mail-Erinnerung zu dieser Frist
```
