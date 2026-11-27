---
name: glossary
description: Keeps the ubiquitous language of the project – challenges terms against the subdomain glossaries, sharpens fuzzy ones, stress-tests them with concrete scenarios and against the code, writes glossary rows and a new subdomain's row and relationships into the domain map. Use from /domain-interview, when the user discusses the project's terminology or edits a glossary, or from another plugin that sets the solution-space columns of a term (interface, see below).
---

> Based on [mattpocock/skills](https://github.com/mattpocock/skills) `skills/engineering/domain-modeling` (MIT, © 2026 Matt Pocock),
> commit `4ae2317`, adapted for design-the-domain: one glossary per subdomain as a table, the domain map, paths from
> the project config, an interface for the solution-space columns; ADRs went to implement-the-domain. See `THIRD_PARTY_LICENSES.md` and `docs/upstream.md` in the source repository.

# Glossary

Paths `assets/…` and `scripts/…` are relative to this skill's base directory (named when the skill loads; `<base directory>` below). Scripts run from the project root.

Keep the project's language precise while the problem space is designed: challenge terms, sharpen
fuzzy ones and write the glossary down the moment a term crystallises. (Merely *reading* a glossary
for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when
you're changing the language, not just consuming it.)

**Project config.** Read `domain-model/config.md` in the project root before anything else; a name in
angle quotes (`‹glossaries›`) is one of its keys. Without the file, or when a key you need holds no value or only a placeholder (`<name>`), stop and tell the
user, in their language and nothing else: fill in `domain-model/config.md` first, `/domain-init` does it with them. Guess no value.

## File structure

```
‹domain-map›                index: subdomains with their types and glossaries, business relationships
‹glossaries›/
  <subdomain>.md            one glossary per subdomain, a table (assets/glossary.md)
  _methodology.md           methodology terms (‹methodology-glossary›), block format
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
concepts; they become ACs and FR scenarios.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a
contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation
is possible. Which is right?" The code tells what is, not what should be: a difference the user
confirms is the delta to implement.

### Update the glossary inline

When a term is resolved, add or change its row in `‹glossaries›/<subdomain>.md` right there.
Don't batch these up: capture them as they happen. Use the format in
`assets/glossary.md`. A new glossary gets its subdomain's row in `‹domain-map›` (column Glossary, `–` in the column
Subdomain map) by `assets/domain-map.md`. Leave the solution-space columns
(`Solution space`, `Identifier`) empty: they are set through the interface below, by whoever decides
the code name.

The glossary is totally devoid of implementation details beyond the code name in its
`Identifier` column. Do not treat it as a spec, a scratch pad, or a repository for
implementation decisions. It is a glossary and nothing else.

A new subdomain or a new relationship between subdomains goes into `‹domain-map›`.

## Interface

Another plugin (`implement-the-domain` when it decides code names) calls this skill through the
Skill tool to set the solution-space columns of existing terms; the problem-space columns stay
untouched.

- **Call:** `glossary set-solution <subdomain>` with one line per term:
  `<term> | <Solution space> | <Identifier>`, e.g.
  `Nachweisart | Value Object | EvidenceKind (sound_report, …)`. `<Solution space>` is a kind of the
  template's mapping (Bounded Context, Aggregate Root, Entity, Value Object, Domain Event, Command,
  Query, Domain Service); `<Identifier>` in `‹solution-space-language›` as in the code.
- **What you do:** find each term's row in `‹glossaries›/<subdomain>.md` and write the two columns.
  An empty column you fill; a filled one you change only to the given value and name the old one in
  the result. A term with no row you do not add: the term belongs to the problem space and is
  decided there.
- **Result:** your last message, exactly in this form:

  ```
  Glossary: <subdomain>
  - <term>: set
  - <term>: changed (was <old identifier>)
  - <term>: missing – no row in the glossary
  ```
- **Guarantees:** writes only the columns `Solution space` and `Identifier` of existing rows of
  that one glossary file. Asks nothing; a missing term is reported, not created.
