# FR-genehmigung-020: Gültigkeitsende eines Gutachtens

Subdomain: genehmigung · Business object: Nachweis · Type: Domain Service · Status: planned

## Changes

- US-0045 · Kind: new · Rule: changed

## Rule

Ein Gutachten gilt ab dem Tag seiner Lieferung für seine Gültigkeitsdauer in Jahren; es ist gültig bis zum Vortag desselben Kalendertags nach Ablauf der Jahre.

## Scenarios

```gherkin
# language: de
Funktionalität: Gültigkeitsende eines Gutachtens

  @US-0045 @planned
  Szenariogrundriss: S1 – Ein Gutachten gilt ab Lieferung für seine Gültigkeitsdauer
    Angenommen ein Gutachten wurde am <geliefert> geliefert und gilt <jahre> Jahre
    Wenn sein Gültigkeitsende bestimmt wird
    Dann ist es gültig bis <gültig_bis>

    Beispiele:
      | geliefert  | jahre | gültig_bis |
      | 15.03.2026 | 5     | 14.03.2031 |
      | 29.02.2024 | 1     | 28.02.2025 |

  @US-0045 @planned
  Szenario: S2 – Ein bald ablaufendes Gutachten fällt auf
    Angenommen ein Gutachten läuft bald ab
    Wenn der Projektleiter den Antrag ansieht
    Dann wird das Gutachten deutlich hervorgehoben
```
