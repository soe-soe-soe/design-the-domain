# Glossary map and domain map overlap

## Goal

Each fact about subdomains and glossaries stands in exactly one file: either `‹glossary-map›`
or `‹domain-map›` lists which glossary belongs to which subdomain, not both.

## Why

Both files list every subdomain with a link to its glossary. A new subdomain means two rows in
two files written by different skills (problem-fr-writer the domain map, problem-init and the
grilling the glossary map); sooner or later they disagree, and nobody notices because no skill
compares them.

## Current state

- `skills/problem-fr-writer/assets/domain-map.md`: per subdomain Type, Glossary link,
  Description; plus the relationships.
- `templates/glossary-map.md`: per glossary file the Subdomain and what it covers; plus the
  methodology glossary.
- Readers: problem-definition reads `‹glossary-map›` first to find the glossaries; problem-init
  and problem-fr-writer read `‹domain-map›`. `templates/output-format.md` lists both as problem
  artifacts.

## Target state

Pick one of these (recommendation first):

1. **Drop the glossary map.** `‹domain-map›` is the index; its Glossary column already links
   every glossary, the methodology glossary gets a line below the subdomain table.
   problem-definition reads `‹domain-map›` instead. Removes a config key and a template.
2. **Drop the Glossary column from the domain map.** The domain map stays purely about
   subdomains and relationships; the glossary map is the only index of glossaries.
3. **Keep both, generate one.** A script builds the glossary map from the domain map; more
   machinery for little gain.

## Before starting

- Check whether a project outside pts relies on `‹glossary-map›` (the pilot project has
  `GLOSSARY-MAP.md` in its root, see its refactoring for the pts migration).
- Option 1 or 2 changes `templates/config.md`, `evals/fixtures/pts.md`,
  `templates/output-format.md`, problem-definition step 1 and 2, problem-init and the
  domain-map fixtures of the evals.
