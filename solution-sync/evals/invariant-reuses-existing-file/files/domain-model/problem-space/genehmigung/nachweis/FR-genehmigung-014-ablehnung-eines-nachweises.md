# FR-genehmigung-014: Ablehnung eines Nachweises

Subdomain: genehmigung · Business object: Nachweis · Type: Invariant · Status: valid

## Rule

Ein Nachweis kann nur aus dem Status In Prüfung abgelehnt werden. Danach ist sein Status Abgelehnt.

## Scenarios

```gherkin
# language: de
Funktionalität: Ablehnung eines Nachweises

  @US-0042 @planned
  Szenario: S1 – Ein Nachweis in Prüfung kann abgelehnt werden
    Angenommen ein Nachweis ist im Status In Prüfung
    Wenn er abgelehnt wird
    Dann ist sein Status Abgelehnt

  @US-0042 @planned
  Szenario: S2 – Ein gelieferter Nachweis kann nicht abgelehnt werden
    Angenommen ein Nachweis ist im Status Geliefert
    Wenn er abgelehnt wird
    Dann wird die Ablehnung zurückgewiesen
```

## History

- US-0042: created (AC1 → S1, AC2 → S2)
