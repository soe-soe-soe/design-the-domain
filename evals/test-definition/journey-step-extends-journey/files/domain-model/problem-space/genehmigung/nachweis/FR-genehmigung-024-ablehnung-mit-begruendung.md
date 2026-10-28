# FR-genehmigung-024: Ablehnung mit Begründung

Subdomain: genehmigung · Business object: Nachweis · Type: Command · Status: valid

## Rule

Ein Nachweis in Prüfung wird mit einer Begründung abgelehnt; die Begründung bleibt am Nachweis.

## Scenarios

```gherkin
# language: de
Funktionalität: Ablehnung mit Begründung

  @US-0047 @planned
  Szenario: S1 – Ein abgelehnter Nachweis nennt seine Begründung
    Angenommen der Nachweis „Schallgutachten“ ist in Prüfung
    Wenn er mit der Begründung „Messpunkte fehlen“ abgelehnt wird
    Dann ist er abgelehnt
    Und seine Begründung lautet „Messpunkte fehlen“
```

## History

- US-0047: created (AC1 → S1)
