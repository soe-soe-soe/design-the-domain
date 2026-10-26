# FR-genehmigung-015: Einreichen nur mit freigegebenen Nachweisen

Subdomain: genehmigung · Business object: Antrag · Type: Invariant · Status: valid

## Rule

Ein Antrag darf nur eingereicht werden, wenn jeder seiner nicht archivierten Nachweise freigegeben ist.

## Scenarios

```gherkin
# language: de
Funktionalität: Einreichen nur mit freigegebenen Nachweisen

  @US-0043 @planned
  Szenario: S1 – Ein Antrag mit nicht freigegebenem Nachweis wird nicht eingereicht
    Angenommen ein Antrag hat einen Nachweis im Status In Prüfung
    Wenn der Antrag eingereicht wird
    Dann wird das Einreichen zurückgewiesen
```

## History

- US-0043: created (AC1 → S1)
