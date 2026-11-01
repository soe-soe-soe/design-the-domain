# US-0050: Erinnerung vor Fristablauf per E-Mail

Status: draft · Topic: Fristerinnerung · createdAt: 2026-10-27

Als Verantwortliche möchte ich vor Ablauf einer Frist per E-Mail erinnert werden.

## Why

Fristen der Behörde dürfen nicht verstreichen; Verlängerungen müssen rechtzeitig beantragt werden.

## Content

Verantwortliche bekommen 7 Kalendertage vor der Fälligkeit eine E-Mail zu jeder offenen Frist.

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
```

## Functional requirements

- FR-fristen-013 (new): AC1 → S1, AC2 → S2
