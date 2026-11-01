<!--
Process – the chain from one trigger through the policies it sets off. Lies in the policies/
folder where the chain starts: ‹problem-space›/<subdomain>/[<business-object>/]policies/process-<slug>.md.
Every Policy FR names its process in its header; a policy of another subdomain links this file.

- Trigger: the Command FR that starts the chain, or a schedule (cron) with its time.
- Steps: in order, one line per FR: the trigger, then each policy with what it reacts to and what
  it sets off. problem-fr-writer adds a step when it writes the policy (planned or active) and
  removes it when the policy is deleted; the FR files carry the status.
- No rules and no scenarios here: they stand in the FRs.
This comment is not copied into a process file.
-->
# Process: <name of the process>

Subdomain: <subdomain> · Business object: <business object or –> · Trigger: <FR-<subdomain>-NNN | schedule: <when>>

## Goal

<What the process achieves in business terms, one sentence.>

## Steps

1. [FR-<subdomain>-NNN](../commands/FR-<subdomain>-NNN-<slug>.md) (Command): <trigger> → <event>
2. [FR-<subdomain>-MMM](FR-<subdomain>-MMM-<slug>.md) (Policy): on <event> → <reaction>
