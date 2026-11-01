# US-0042: Nachweise können abgelehnt werden

Status: ready · Topic: Nachweise können abgelehnt werden · createdAt: 2026-10-26

Als Projektleiter möchte ich einen geprüften Nachweis ablehnen.

## Why

Mangelhafte Gutachten müssen nachgebessert werden; die Ablehnung macht das sichtbar.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Nachweise ablehnen

  Szenario: AC1 – Ein Nachweis in Prüfung kann abgelehnt werden
    Angenommen ein Nachweis ist im Status In Prüfung
    Wenn er abgelehnt wird
    Dann ist sein Status Abgelehnt

  Szenario: AC2 – Ein gelieferter Nachweis kann nicht abgelehnt werden
    Angenommen ein Nachweis ist im Status Geliefert
    Wenn er abgelehnt wird
    Dann wird die Ablehnung zurückgewiesen
```

## Functional requirements

- FR-genehmigung-014 (new): AC1 → S1, AC2 → S2
