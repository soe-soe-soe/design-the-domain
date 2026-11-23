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

  @US-0050 @planned
  Szenario: S4 – Nach dem Verschieben wird zum neuen Datum erinnert
    Angenommen Petra wurde zu einer Frist mit Fälligkeit 23.10.2026 erinnert
    Und die Fälligkeit wurde auf den 06.11.2026 verschoben
    Wenn heute der 30.10.2026 ist
    Dann erhält Petra erneut eine E-Mail-Erinnerung zu dieser Frist
```
