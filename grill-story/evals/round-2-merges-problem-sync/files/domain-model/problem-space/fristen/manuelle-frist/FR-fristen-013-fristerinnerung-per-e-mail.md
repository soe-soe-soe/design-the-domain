# FR-fristen-013: Fristerinnerung per E-Mail

Subdomain: fristen · Business object: manuelle-frist · Type: Policy · Status: valid

## Rule

Sieben Kalendertage vor der Fälligkeit einer offenen Frist bekommt ihr Verantwortlicher eine E-Mail-Erinnerung; erledigte Fristen werden nicht erinnert.

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

  @US-0050 @planned @open
  Szenario: S2 – Abgeleitete Frist sieben Tage vor Fälligkeit
    Angenommen die Lieferung eines Nachweises ist fällig am 23.10.2026
    Und Petra ist verantwortlich
    Wenn heute der 16.10.2026 ist
```

## Open

- **S2** (fr-writer): Gilt die Erinnerung auch für abgeleitete Fristen, also Fristen aus Nachweis- und Antragsstatus? – Recommendation: Ja, das Glossar fasst unter „Frist“ beide Arten zusammen. – Story: US-0050 · Case: glossary · Type: Policy · Test level: Integration · Glossary: fristen.md: Frist

## History

- US-0050: created (AC1 → S1, AC2 → S2)
