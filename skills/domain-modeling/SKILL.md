---
name: domain-modeling
description: Build and sharpen the project's domain model while designing – challenge terms, invent edge-case scenarios, write glossary rows into the subdomain glossaries and record ADRs. Use from /pts:problem-definition, or when the user discusses the project's terminology, edits a glossary or records an ADR.
---

> Based on [mattpocock/skills](https://github.com/mattpocock/skills) `skills/engineering/domain-modeling` (MIT, © 2026 Matt Pocock),
> commit `4ae2317`, adapted for pts: one glossary per subdomain as a table, the domain map, paths from
> the project config. See `THIRD_PARTY_LICENSES.md` and `docs/upstream.md`.

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active*
discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and
decisions down the moment they crystallise. (Merely *reading* a glossary for vocabulary is not
this skill: that's a one-line habit any skill can do. This skill is for when you're changing the
model, not just consuming it.)

**Project config.** Read `.claude/pts.md` in the project root before anything else; a name in
angle quotes (`‹glossaries›`) is one of its keys. Without the file, stop and point the user to the
template `${CLAUDE_PLUGIN_ROOT}/templates/config.md`.

## File structure

```
‹glossary-map›              index: the glossaries, the domain map, the context map
‹domain-map›                subdomains, their types and business relationships
‹glossaries›/
  <subdomain>.md            one glossary per subdomain, a table (GLOSSARY-FORMAT.md)
  _methodology.md           methodology terms (‹methodology-glossary›), block format
‹adr›/                      architecture decisions, numbered as the folder already numbers them
```

Infer which subdomain the current topic belongs to from the domain map. If it is unclear, ask.
A term that fits no subdomain, or several, is an ownership question for the user, not yours to
settle silently.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in the subdomain's glossary,
call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y.
Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying
'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent
scenarios that probe edge cases and force the user to be precise about the boundaries between
concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a
contradiction, surface it: "Your code cancels entire Orders, but you just said partial
cancellation is possible. Which is right?"

### Update the glossary inline

When a term is resolved, add or change its row in `‹glossaries›/<subdomain>.md` right there.
Don't batch these up: capture them as they happen. Use the format in
[GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md); where `‹project-rules›` says more about the glossary,
it wins. Leave the solution-space columns empty when the code name is not decided yet:
`pts:solution-definition` fills them.

The glossary is totally devoid of implementation details beyond the code name in its
`Identifier` column. Do not treat it as a spec, a scratch pad, or a repository for
implementation decisions. It is a glossary and nothing else.

A new subdomain or a new relationship between subdomains goes into `‹domain-map›`.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for
   specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md);
the folder is `‹adr›`, and what `‹project-rules›` says about ADRs (e.g. updating one in place
instead of superseding it) wins over the format.
