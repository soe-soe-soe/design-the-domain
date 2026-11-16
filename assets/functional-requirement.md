<!--
Active FR – the implemented target state. Lies in ‹problem-space›/<subdomain>/[<business-object>/]<type-folder>/ (folder per FR type, see
functional-requirement-types.md). A Policy adds `· Process: [<Name>](process-<slug>.md) · Trigger: <event |
schedule: <when>>` to the header line.
Only `requirements.py complete` writes it (and problem-init for code taken over); problem-space-fr
writes the planned file next to it (planned-functional-requirement.md). Each scenario
carries the tag of the story that last changed it, or @existing. The history of an FR is not
kept here: `requirements.py history FR-<subdomain>-NNN` derives it from the done stories.
This comment is not copied into an FR file.
-->
# FR-<subdomain>-NNN: <rule or capability>

Subdomain: <subdomain> · Business object: <business object or –> · Type: <FR type> · Status: valid

## Rule

<The rule in glossary terms, without modules and classes.>

## Scenarios

```gherkin
# language: en
Feature: <rule or capability>

  @US-NNNN
  Scenario: S1 – <expected behaviour>
    Given <starting situation>
    When <exactly one trigger>
    Then <observable result>
```
