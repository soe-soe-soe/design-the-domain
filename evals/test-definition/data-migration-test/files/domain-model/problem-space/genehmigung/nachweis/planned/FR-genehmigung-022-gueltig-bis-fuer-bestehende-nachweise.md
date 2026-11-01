# FR-genehmigung-022: Gültig bis für bestehende Nachweise

Subdomain: genehmigung · Business object: Nachweis · Type: Data Migration · Status: planned

## Changes

- US-0046 · Kind: new · Rule: changed

## Rule

Nachweise, die vor der Einführung von „Gültig bis“ geliefert wurden, erhalten bei der Umstellung ein Gültig bis: Schallgutachten fünf Jahre ab Lieferung bis zum Vortag, alle anderen Nachweise keines (unbefristet).

## Scenarios

```gherkin
# language: de
Funktionalität: Gültig bis für bestehende Nachweise

  @US-0046 @planned
  Szenariogrundriss: S1 – Bestehende Nachweise erhalten ihr Gültig bis bei der Umstellung
    Angenommen ein <art> wurde vor der Umstellung am <geliefert> geliefert
    Wenn die Umstellung auf „Gültig bis“ läuft
    Dann ist er gültig bis <gültig_bis>

    Beispiele:
      | art                       | geliefert  | gültig_bis |
      | Schallgutachten           | 15.03.2026 | 14.03.2031 |
      | Lageplan                  | 15.03.2026 | leer       |
```
