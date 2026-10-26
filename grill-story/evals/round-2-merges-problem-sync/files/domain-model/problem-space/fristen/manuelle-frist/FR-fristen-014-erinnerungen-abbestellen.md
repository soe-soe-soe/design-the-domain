# FR-fristen-014: Erinnerungen abbestellen

Subdomain: fristen · Business object: manuelle-frist · Type: Command · Status: valid

## Rule

Ein Nutzer kann Fristerinnerungen abbestellen; danach bekommt er keine Erinnerungen mehr.

## Scenarios

```gherkin
# language: de
Funktionalität: Erinnerungen abbestellen

  @US-0051 @planned @open
  Szenario: S1 – Abbestellte Erinnerungen werden nicht verschickt
    Angenommen Petra hat Fristerinnerungen abbestellt
    Und eine offene Frist von Petra ist fällig in 7 Tagen
    Wenn die Erinnerungen verschickt werden
    Dann erhält Petra keine Erinnerung
```

## Open

- **S1** (fr-writer): Gehört das Abbestellen als Einstellung des Nutzers zur Subdomäne Zugang statt zu Fristen? – Recommendation: Ja, es ist eine Einstellung des Nutzers, keine Eigenschaft der Frist. – Story: US-0051 · Case: ownership · Type: Command · Test level: Integration

## History

- US-0051: created (AC1 → S1)
