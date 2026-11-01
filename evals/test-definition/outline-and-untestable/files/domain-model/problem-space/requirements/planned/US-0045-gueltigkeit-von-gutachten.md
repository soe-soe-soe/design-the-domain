# US-0045: Gültigkeit von Gutachten

Status: ready · Topic: Gültigkeit von Gutachten · createdAt: 2026-10-26

Als Projektleiter möchte ich sehen, bis wann ein Gutachten gültig ist.

## Why

Die Behörde akzeptiert Gutachten nur innerhalb ihrer Gültigkeit; ein abgelaufenes Gutachten verzögert den Antrag.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Gültigkeit von Gutachten

  Szenariogrundriss: AC1 – Ein Gutachten gilt ab Lieferung für seine Gültigkeitsdauer
    Angenommen ein Gutachten wurde am <geliefert> geliefert und gilt <jahre> Jahre
    Wenn sein Gültigkeitsende bestimmt wird
    Dann ist es gültig bis <gültig_bis>

    Beispiele:
      | geliefert  | jahre | gültig_bis |
      | 15.03.2026 | 5     | 14.03.2031 |
      | 29.02.2024 | 1     | 28.02.2025 |

  Szenario: AC2 – Ein bald ablaufendes Gutachten fällt auf
    Angenommen ein Gutachten läuft bald ab
    Wenn der Projektleiter den Antrag ansieht
    Dann wird das Gutachten deutlich hervorgehoben
```

## Functional requirements

- FR-genehmigung-020 (new): AC1 → S1, AC2 → S2
