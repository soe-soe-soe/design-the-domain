# US-0047: Nachweis mit Begründung ablehnen

Status: ready · Topic: Ablehnung von Nachweisen · createdAt: 2026-10-26

Als Projektleiter möchte ich einen Nachweis in Prüfung mit einer Begründung ablehnen.

## Why

Der Gutachter muss wissen, was er nachbessern soll; ohne Begründung beginnt das Nachfragen.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Nachweis mit Begründung ablehnen

  Szenario: AC1 – Ein abgelehnter Nachweis zeigt seine Begründung
    Angenommen der Nachweis „Schallgutachten“ ist in Prüfung
    Wenn der Projektleiter ihn mit der Begründung „Messpunkte fehlen“ ablehnt
    Dann zeigt die Nachweisliste ihn als „Abgelehnt“
    Und die Nachweisliste zeigt die Begründung „Messpunkte fehlen“
```

## Functional requirements

- FR-genehmigung-024 (new): AC1 → S1
