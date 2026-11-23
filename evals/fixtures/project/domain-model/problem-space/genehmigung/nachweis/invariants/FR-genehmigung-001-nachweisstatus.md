# FR-genehmigung-001: Nachweisstatus nur über erlaubte Übergänge

Subdomain: genehmigung · Business object: nachweis · Type: Invariant · Status: valid

## Rule

Ein Nachweis wechselt nur von angefordert zu in Arbeit, von in Arbeit zu geliefert und von
geliefert zu nachgefordert; nachgefordert gilt wie angefordert.

## Scenarios

```gherkin
# language: de
Funktionalität: Nachweisstatus nur über erlaubte Übergänge

  @US-0030
  Szenario: S1 – Geliefert nur aus in Arbeit
    Angenommen das Schallgutachten ist angefordert
    Wenn es als geliefert erfasst werden soll
    Dann bleibt es angefordert und der Nutzer erfährt, dass es erst in Arbeit sein muss
```
