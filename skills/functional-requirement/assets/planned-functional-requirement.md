<!--
Planned FR – the changes not yet implemented. Lies in planned/ below the folder of the active FR,
with the same file name; a new FR gets its own name there. One planned file per FR holds the
changes of every story touching it; `requirements.py complete` merges one story's changes into the
active FR and removes them here, the file goes once no change is left.

## Changes   one line per story: Kind new (FR does not exist yet), edit, or deletion (the whole
            FR becomes obsolete; no scenarios needed). Rule: changed when ## Rule below is the
            story's new rule text.
## Rule      only when a change line says Rule: changed (for Kind new always).
## Scenarios only the scenarios a story changes, adds or drops, numbered as in the active FR:
            - changed: same Sn, full new text, tags @US-NNNN @planned @base-<tag>
            - dropped: same Sn, `Scenario: Sn – dropped: <title>`, tags @US-NNNN @planned @obsolete @base-<tag>
            - new:     next free Sn across the active FR and this file, tags @US-NNNN @planned
            @base-<tag> is the story tag the active scenario carried when the change was written
            (@base-US-0050, @base-existing); a differing tag at close is a parallel change.
## Open      as in the active FR's open points; omitted when empty.
This comment is not copied into an FR file.
-->
# FR-<subdomain>-NNN: <rule or capability>

Subdomain: <subdomain> · Business object: <business object or –> · Type: <FR type> · Status: planned

## Changes

- US-NNNN · Kind: <new | edit | deletion> · Rule: <changed | unchanged>

## Rule

<The rule after the change, in glossary terms.>

## Scenarios

```gherkin
# language: en
Feature: <rule or capability>

  @US-NNNN @planned @base-US-NNNN
  Scenario: S1 – <changed behaviour>
    Given <starting situation>
    When <exactly one trigger>
    Then <observable result>

  @US-NNNN @planned
  Scenario: S4 – <new behaviour>
    Given <starting situation>
    When <exactly one trigger>
    Then <observable result>
```

## Open

- **Sn** (functional-requirement): <question, accepted by "yes"> – Recommendation: <answer> – Story: US-NNNN · Case: <ripple | overwrite-implemented | glossary | ownership | consistency | existing-data> · Type: <FR type>
