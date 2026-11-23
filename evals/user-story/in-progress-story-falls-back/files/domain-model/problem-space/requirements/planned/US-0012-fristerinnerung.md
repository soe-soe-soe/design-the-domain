# US-0012: Verantwortliche werden vor Ablauf einer Frist erinnert

Status: in-progress · Topic: Fristerinnerung · createdAt: 2026-10-20

Als Verantwortliche möchte ich vor Ablauf einer Frist per E-Mail erinnert werden.

## Why

Fristen der Behörde verstreichen, weil niemand rechtzeitig daran denkt.

## Content

Eine E-Mail an die Verantwortliche einige Tage vor der Fälligkeit.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Fristerinnerung

  Szenario: AC1 – Erinnerung sieben Tage vor Fälligkeit
    Angenommen Petra ist verantwortlich für eine offene Frist fällig am 23.10.2026
    Wenn heute der 16.10.2026 ist
    Dann erhält Petra eine E-Mail-Erinnerung zu dieser Frist
```

## Functional requirements

- FR-fristen-013 (new): AC1 → S1
