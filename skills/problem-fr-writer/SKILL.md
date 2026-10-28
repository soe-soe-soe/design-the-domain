---
name: problem-fr-writer
description: Writes the functional requirements (FRs) under ‹problem-space›/ from new or changed user stories and marks contradictions with the existing state as open points. Use from the writing subagent of /problem-definition after problem-story-writer, or when the user wants stories "taken into FRs" or the FR set reconciled.
---

# Problem-FR-Writer

An **FR** is the current target state of one rule or capability, assigned to exactly one
subdomain. Stories describe changes, FRs the result of all changes. You carry the acceptance
criteria (AC) of the stories over into FR scenarios and look for **contradictions with the
existing state** the conversation cannot see.

You write what is decided and mark what is still open, in the FR itself. You ask nothing:
`/pts:problem-definition` reads the open points and decides when to ask them.

**Project config.** Read `.claude/pts.md` in the project root before anything else; a name in
angle quotes (`‹stories›`) is one of its keys. Without the file, stop and point the user to the
template `${CLAUDE_PLUGIN_ROOT}/templates/config.md`.

You write only FRs under `‹problem-space›/<subdomain>/` and the domain map. Stories,
glossaries and ADRs you only read. FRs contain no code locations; the link to the code is the
test that references a scenario.

Language: methodology terms, headings, tags, IDs and field labels are English; FR content
(title, rule, scenarios, open questions) is in `‹content-language›`.

## Layout

```
‹problem-space›/
  domain-map.md                    subdomains, types, business relationships
  <subdomain>/                     e.g. genehmigung, fristen (umlauts spelled out)
    <business-object>/             only business objects with an aggregate root, e.g. nachweis
      FR-<subdomain>-NNN-<slug>.md
    FR-<subdomain>-NNN-<slug>.md   rules without own business object, e.g. of a value
    subdomain-<name>/              provisional subdomain (see its README), FR IDs of the host
```

Which business objects a subdomain has stands in the sections of its glossary
(`‹glossaries›/<subdomain>.md`). The number `NNN` counts per subdomain.

## Steps

1. **Read the situation.** The stories from the input (new or continued),
   `‹domain-map›`, the glossaries and all FRs of the subdomains
   they touch, and the ADRs on the topic.

2. **Assign.** For each AC determine the subdomain from the domain map, the business object
   from the glossary and the FR type by [references/fr-types.md](references/fr-types.md). A
   query belongs to the subdomain that supplies the data, a policy to the one that triggers it.
   Does an AC need a subdomain or a relationship between subdomains the domain map lacks, add
   it there by the template [assets/domain-map.md](assets/domain-map.md): a new subdomain with
   type `open`, a relationship in business terms.

3. **Check.** An AC leads to an open point in six cases only:
   - **ripple:** the change touches another FR the story says nothing about, e.g. a new
     overdue threshold and the FR "Problemsignale" that builds on overdue. The story leaves
     open whether the other FR follows.
   - **overwrite-implemented:** an AC contradicts an implemented scenario (without `@planned`
     and `@unconfirmed`), and the story does not supersede it via `Supersedes in part`.
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
   with ADRs the grilling asks itself.

4. **Write.** For each AC, by the template
   [assets/functional-requirement.md](assets/functional-requirement.md):
   - **Phrase it on the FR's rule.** A scenario checks exactly the rule of its FR. Do not take
     an AC verbatim if it checks another rule as well: "Die Projektübersicht zeigt 1
     Problemsignal" becomes "Dann gilt die Frist als überfällig" in the FR "Überfälligkeit";
     the count belongs to the FR of the problem signals.
   - If it belongs to an existing FR of the same rule, change the matching scenario (number
     stays) or append the next `Sn`; otherwise create an FR with the next free number of the
     subdomain. For **ownership**, create it in the subdomain you recommend.
   - Each scenario carries the tag of its story and, while that story is not done, `@planned`.
     Once a story is `done`, remove `@planned` from its scenarios.
   - An AC marked as dropped (`entfallen`) makes its scenario `@obsolete`; the number stays
     taken.
   - Record in the history which AC became which scenario.

5. **Mark what is open.** The scenario an open point concerns carries the tag `@open` (meaning
   as in the term "Open point"): for **ripple** the scenario of the other FR, for
   **overwrite-implemented** the implemented scenario, which keeps its Dann – you write no
   scenario for the contradicting AC until the answer is in; otherwise the new scenario, without
   Dann while its outcome hangs on the answer. Each open point gets one entry under `## Open` of that FR, in
   the format of the term "Open point" in `‹methodology-glossary›`, with source
   `problem-fr-writer` and the fields `Story`, `Case`, `Type`, and for **glossary**
   `Glossary` (glossary and term, e.g. `fristen.md: Problem`).

6. **Resolve what is answered.** If a story now answers an open point (a later round decided
   it), carry the answer into the scenario, remove `@open` and the entry under `## Open`; for
   **ownership** move the FR if the answer names another subdomain.

You are done when every AC of the input stories stands in a scenario, every open point is
marked, and every subdomain and relationship you used stands in the domain map.

## Tags per scenario

| Tag | Meaning |
|---|---|
| `@US-0042` | Story that last changed the scenario |
| `@existing` | Taken from existing code (problem-init), without story |
| `@planned` | The story is not implemented yet |
| `@unconfirmed` | Derived from code, not yet confirmed by the user |
| `@open` | An open point in `## Open` concerns this scenario |
| `@obsolete` | No longer applies; the number is never reused |

The FR header knows only `Status: valid` or `Status: obsolete`. `## Open` is omitted when there is nothing to enter.

## Report

Your last message is the report, exactly in this form. It names what changed; `Sn open` marks a
scenario that got a new open point, so `/pts:problem-definition` knows which FRs to read – the point itself
stands only in the FR:

```
FRs:
- FR-fristen-001: Überfälligkeit einer Frist (S1 changed)
- FR-fristen-002: Zählung der Problemsignale (S1 open)
- FR-fristen-004: Fristerinnerung per E-Mail (new)
Domain map: unchanged
```

`Domain map` lists what you added, otherwise `unchanged`.
