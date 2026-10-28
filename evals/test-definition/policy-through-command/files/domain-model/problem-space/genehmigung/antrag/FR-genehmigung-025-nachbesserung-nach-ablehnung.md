# FR-genehmigung-025: Nachbesserung nach Ablehnung

Subdomain: genehmigung · Business object: Antrag · Type: Policy · Status: valid

## Rule

Wird ein Nachweis abgelehnt, geht sein eingereichter Antrag in die Nachbesserung.

## Scenarios

```gherkin
# language: de
Funktionalität: Nachbesserung nach Ablehnung

  @US-0048 @planned
  Szenario: S1 – Ein abgelehnter Nachweis schickt seinen Antrag in die Nachbesserung
    Angenommen ein eingereichter Antrag hat einen Nachweis in Prüfung
    Wenn der Nachweis abgelehnt wird
    Dann ist der Antrag in Nachbesserung
```

## History

- US-0048: created (AC1 → S1)
