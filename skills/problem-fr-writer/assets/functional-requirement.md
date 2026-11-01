<!--
Active FR – the implemented target state. Lies in ‹problem-space›/<subdomain>/[<business-object>/].
Only `requirements.py complete` writes it (and problem-init for code taken over); problem-fr-writer
writes the planned file next to it (assets/planned-functional-requirement.md). Each scenario
carries the tag of the story that last changed it, or @existing. The history of an FR is not
kept here: `requirements.py history FR-<subdomain>-NNN` derives it from the done stories.
This comment is not copied into an FR file.
-->
# FR-<subdomain>-NNN: <Regel oder Fähigkeit>

Subdomain: <subdomain> · Business object: <business object or –> · Type: <FR type> · Status: valid

## Rule

<Die Regel in Glossarbegriffen, ohne Module und Klassen.>

## Scenarios

```gherkin
# language: de
Funktionalität: <Regel oder Fähigkeit>

  @US-NNNN
  Szenario: S1 – <erwartetes Verhalten>
    Angenommen <Ausgangslage>
    Wenn <genau ein Auslöser>
    Dann <beobachtbares Ergebnis>
```
