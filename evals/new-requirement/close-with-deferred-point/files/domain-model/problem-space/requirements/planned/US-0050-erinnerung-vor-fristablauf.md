# US-0050: Erinnerung vor Fristablauf per E-Mail

Status: draft · Topic: Fristerinnerung · createdAt: 2026-10-27

Als Verantwortliche möchte ich vor Ablauf einer Frist per E-Mail erinnert werden.

## Why

Fristen der Behörde dürfen nicht verstreichen; Verlängerungen müssen rechtzeitig beantragt werden.

## Content

Verantwortliche bekommen 7 Kalendertage vor der Fälligkeit eine E-Mail zu jeder offenen Frist, ob manuell oder abgeleitet. Wird die Fälligkeit verschoben, wird zum neuen Datum erneut erinnert. Absender ist noreply@example.org, der Versandtag wird in der Zeitzone Europe/Berlin bestimmt.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Erinnerung vor Fristablauf per E-Mail

  Szenario: AC1 – Erinnerung sieben Tage vor Fälligkeit
    Angenommen eine offene manuelle Frist ist fällig am 23.10.2026
    Und Petra ist verantwortlich
    Wenn heute der 16.10.2026 ist
    Dann erhält Petra eine E-Mail-Erinnerung zu dieser Frist

  Szenario: AC2 – Erledigte Frist wird nicht erinnert
    Angenommen eine manuelle Frist ist fällig am 23.10.2026 und erledigt
    Wenn heute der 16.10.2026 ist
    Dann wird keine Erinnerung verschickt

  Szenario: AC3 – Abgeleitete Fristen werden ebenso erinnert
    Angenommen die Lieferung eines Nachweises ist fällig am 23.10.2026
    Und Petra ist verantwortlich
    Wenn heute der 16.10.2026 ist
    Dann erhält Petra eine E-Mail-Erinnerung zu dieser Frist

  Szenario: AC4 – Nach dem Verschieben wird zum neuen Datum erinnert
    Angenommen Petra wurde zu einer Frist mit Fälligkeit 23.10.2026 erinnert
    Und die Fälligkeit wurde auf den 06.11.2026 verschoben
    Wenn heute der 30.10.2026 ist
    Dann erhält Petra erneut eine E-Mail-Erinnerung zu dieser Frist
```

## Functional requirements

- FR-fristen-013 (new): AC1 → S1, AC2 → S2, AC3 → S3, AC4 → S4
