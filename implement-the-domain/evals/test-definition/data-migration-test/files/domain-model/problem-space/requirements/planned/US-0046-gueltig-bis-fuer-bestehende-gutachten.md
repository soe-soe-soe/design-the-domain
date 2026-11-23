# US-0046: Gültig bis für bestehende Gutachten

Status: ready · Topic: Gültigkeit von Gutachten · createdAt: 2026-10-26

Als Projektleiter möchte ich auch bei bereits gelieferten Gutachten sehen, bis wann sie gültig sind.

## Why

Mit der Einführung von „Gültig bis“ hätten alle vorhandenen Gutachten sonst kein Datum.

## Acceptance criteria

```gherkin
# language: de
Funktionalität: Gültig bis für bestehende Gutachten

  Szenariogrundriss: AC1 – Bestehende Nachweise erhalten ihr Gültig bis bei der Umstellung
    Angenommen ein <art> wurde vor der Umstellung am <geliefert> geliefert
    Wenn die Umstellung auf „Gültig bis“ läuft
    Dann ist er gültig bis <gültig_bis>

    Beispiele:
      | art                       | geliefert  | gültig_bis |
      | Schallgutachten           | 15.03.2026 | 14.03.2031 |
      | Lageplan                  | 15.03.2026 | leer       |
```

## Functional requirements

- FR-genehmigung-022 (new): AC1 → S1
