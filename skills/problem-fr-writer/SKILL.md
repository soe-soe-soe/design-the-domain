---
name: problem-fr-writer
description: Writes the planned changes of functional requirements (FRs) under ‹problem-space›/**/planned/ from new or changed user stories and marks contradictions with the existing state as open points. Use from the writing subagent of /problem-definition after problem-story-writer, or when the user wants stories "taken into FRs" or the FR set reconciled.
---

# Problem-FR-Writer

An **FR** is the implemented target state of one rule or capability, assigned to exactly one
subdomain. Stories describe changes, FRs the result of all changes. You carry the acceptance
criteria (AC) of the stories over into **planned FRs** – the change next to the active FR,
merged into it only when the story is done – and look for **contradictions with the existing
state** the conversation cannot see.

You write what is decided and mark what is still open, in the FR itself. You ask nothing:
`/pts:problem-definition` reads the open points and decides when to ask them.

**Project config.** Read `.claude/pts.md` in the project root before anything else; a name in
angle quotes (`‹requirements›`) is one of its keys. Without the file, stop and point the user to the
template `${CLAUDE_PLUGIN_ROOT}/templates/config.md`.

You write only planned FRs (`planned/` below an FR folder), the domain map, and in a story the
section `## Functional requirements`. Active FRs, the rest of a story, glossaries and ADRs you
only read: an active FR changes only through `requirements.py complete` when its story is done. FRs contain no code locations; the link to the code is the
test that references a scenario.

Language: methodology terms, headings, tags, IDs and field labels are English; FR content
(title, rule, scenarios, open questions) is in `‹content-language›`.

## Layout

```
‹problem-space›/
  domain-map.md                    subdomains, types, business relationships
  <subdomain>/                     e.g. genehmigung, fristen (umlauts spelled out)
    <business-object>/             only business objects with an aggregate root, e.g. nachweis
      <type-folder>/               one per FR type, created with its first FR: invariants,
                                   domain-services, policies, commands, queries, acl, data-migrations
        FR-<subdomain>-NNN-<slug>.md   active FR, implemented
        planned/
          FR-<subdomain>-NNN-<slug>.md planned changes of that FR, same file name
          FR-<subdomain>-MMM-<slug>.md a new FR (Kind new), not active yet
      policies/
        process-<slug>.md          the process its policies belong to (assets/process.md)
    <type-folder>/                 FRs without own business object, e.g. rules of a value
```

The type folder follows the FR type ([references/fr-types.md](references/fr-types.md)); a
changed type moves the FR. Which business objects a subdomain has stands in the sections of its glossary
(`‹glossaries›/<subdomain>.md`). The number `NNN` counts per subdomain, across active and planned
FRs. One planned file per FR holds the changes of every story touching it; its format, the
change kinds (new, edit, deletion) and the `@base-` tag stand in the comment of
[assets/planned-functional-requirement.md](assets/planned-functional-requirement.md) – read it.

## Steps

1. **Read the situation.** The stories from the input (new or continued),
   `‹domain-map›`, the glossaries and all FRs of the subdomains they touch – active and planned
   – and the ADRs on the topic.

2. **Assign.** For each AC determine the subdomain from the domain map, the business object
   from the glossary and the FR type by [references/fr-types.md](references/fr-types.md). A
   query belongs to the subdomain that supplies the data, a policy to the one that triggers it.
   Each policy belongs to one process: an existing one whose chain it continues, or a new
   process file by [assets/process.md](assets/process.md) in the `policies/` folder where the
   chain starts. Add the policy as a step to its process; a policy in another subdomain links
   the process file there.
   Does an AC need a subdomain or a relationship between subdomains the domain map lacks, add
   it there by the template [assets/domain-map.md](assets/domain-map.md): a new subdomain with
   type `open`, a relationship in business terms.

3. **Check.** An AC leads to an open point in six cases only:
   - **ripple:** the change touches another FR the story says nothing about, e.g. a new
     overdue threshold and the FR "Problemsignale" that builds on overdue. The story leaves
     open whether the other FR follows.
   - **overwrite-implemented:** an AC contradicts a scenario of an active FR (without
     `@unconfirmed`), and the story does not supersede it via `Supersedes in part`.
   - **glossary:** a scenario you must write contradicts the description of a glossary term,
     or hangs on a term whose meaning the glossary leaves open, and its outcome depends on it;
     wording and style are no case. You do not change the glossary; the grilling maintains it.
   - **ownership:** a new term or rule fits more than one subdomain, or none in the domain map,
     and the input does not say which one owns it.
   - **consistency:** a rule links two business objects (e.g. Nachweis and Antrag) and the input
     does not say whether it must hold at once or may follow shortly after; the answer decides
     whether it is an invariant of one business object or a policy between two.
   - **existing-data:** an AC adds or changes what a business object holds or how it is
     derived (a new Wert, a changed status set), instances of it already exist, and no AC says
     what becomes of them. The answer is a scenario of an FR of type Data Migration.

   A difference to the code is no open point: it is the delta to be implemented. Contradictions
   with ADRs the grilling asks itself. A planned file that already holds a change of **another
   story** to the same scenario is no open point of yours either: report it under `Parallel`,
   and `/pts:problem-definition` takes it into the interview.

4. **Write.** For each AC, into the planned file of its FR by the template
   [assets/planned-functional-requirement.md](assets/planned-functional-requirement.md),
   creating the file (and the `planned/` folder) if needed:
   - **Phrase it on the FR's rule.** A scenario checks exactly the rule of its FR. Do not take
     an AC verbatim if it checks another rule as well: "Die Projektübersicht zeigt 1
     Problemsignal" becomes "Dann gilt die Frist als überfällig" in the FR "Überfälligkeit";
     the count belongs to the FR of the problem signals.
   - **Kind.** The story's line under `## Changes`: `edit` if an active FR of the same rule
     exists, `new` if not – with the next free FR number of the subdomain; for **ownership**
     in the subdomain you recommend –, `deletion` if the story drops the rule altogether.
     `Rule: changed` and the new rule text under `## Rule` if the story changes the rule.
   - **Numbers stay those of the active FR.** A changed scenario keeps its `Sn` and gets
     `@base-<tag>` with the story tag the active scenario carries now; a new scenario takes the
     next free `Sn` across the active FR and the planned file. Tests reference these numbers.
   - Each scenario carries the tag of its story and `@planned`.
   - An AC marked as dropped (`entfallen`) makes its scenario `@obsolete`
     (`Szenario: Sn – entfällt: <Titel>`); the number stays taken.
   - **Story reference.** Write the section `## Functional requirements` of the story: one line
     per FR with its kind and which AC became which scenario
     (`- FR-fristen-003 (edit): AC1 → S1, AC2 → S3 obsolete`). It replaces the history an FR
     used to keep: `requirements.py history` reads it.

5. **Mark what is open** – in planned files only, never in an active FR. The scenario an open
   point concerns carries the tag `@open` (meaning as in the term "Open point"): for **ripple**
   and **overwrite-implemented** a copy of the active scenario in the planned file of its FR,
   with its Dann, `@base-<tag>` and a change line `Kind: edit` for the story – you write no
   scenario for a contradicting AC until the answer is in; otherwise the new scenario, without
   Dann while its outcome hangs on the answer. Each open point gets one entry under `## Open` of that planned file, in
   the format of the term "Open point" in `‹methodology-glossary›`, with source
   `problem-fr-writer` and the fields `Story`, `Case`, `Type`, and for **glossary**
   `Glossary` (glossary and term, e.g. `fristen.md: Problem`).

6. **Resolve what is answered.** If a story now answers an open point (a later round decided
   it), carry the answer into the scenario, remove `@open` and the entry under `## Open`; for
   **ownership** move the planned FR if the answer names another subdomain. An answer that
   leaves the other FR as it is removes the copied scenario, and the story's change line when
   nothing of the story is left; a planned file without change lines is deleted.

You are done when every AC of the input stories stands in a scenario of a planned file, every
story names its FRs under `## Functional requirements`, every open point is marked, and every
subdomain and relationship you used stands in the domain map.

## Tags per scenario

| Tag | Meaning |
|---|---|
| `@US-0042` | Active FR: story that last changed the scenario. Planned file: story the change belongs to |
| `@existing` | Taken from existing code (problem-init), without story |
| `@planned` | Planned file only: the change is not implemented yet |
| `@base-US-0042` | Planned file only: story tag of the active scenario the change was written against (`@base-existing`) |
| `@unconfirmed` | Derived from code, not yet confirmed by the user |
| `@open` | An open point in `## Open` concerns this scenario |
| `@obsolete` | No longer applies; the number is never reused |

The FR header knows `Status: valid` or `Status: obsolete` for an active FR and
`Status: planned` for a planned file. `## Open` is omitted when there is nothing to enter.

## Report

Your last message is the report, exactly in this form. It names what changed; `Sn open` marks a
scenario that got a new open point, so `/pts:problem-definition` knows which FRs to read – the point itself
stands only in the FR:

```
FRs:
- FR-fristen-001: Überfälligkeit einer Frist (edit, S1 changed)
- FR-fristen-002: Zählung der Problemsignale (edit, S1 open)
- FR-fristen-004: Fristerinnerung per E-Mail (new)
Parallel:
- FR-fristen-001/S1: also changed by US-0039 (ready)
Domain map: unchanged
```

`Domain map` lists what you added, otherwise `unchanged`. `Parallel` is omitted when no planned
file holds a change of another story to a scenario this story changes.
