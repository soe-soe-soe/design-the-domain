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

- **Why the glossary map exists:** Pocock's `domain-modeling` (`‹skill-domain-modeling›`), which
  problem-definition loads for the interview, looks for `GLOSSARY-MAP.md` in the project root and
  only there. The map is the entry point for that skill, not a pts invention; it cannot simply be
  deleted while pts relies on `domain-modeling`.
- `skills/problem-fr-writer/assets/domain-map.md`: per subdomain Type, Glossary link,
  Description; plus the relationships.
- `templates/glossary-map.md`: per glossary file the Subdomain and what it covers; plus the
  methodology glossary.
- Readers: problem-definition reads `‹glossary-map›` first to find the glossaries; problem-init
  and problem-fr-writer read `‹domain-map›`. `templates/output-format.md` lists both as problem
  artifacts.

## Target state

Pick one of these (recommendation first):

1. **Drop the Glossary column from the domain map.** The domain map stays purely about
   subdomains and relationships; the glossary map, which `domain-modeling` needs anyway, is the
   only index of glossaries.
2. **Drop the glossary map.** Only possible if `domain-modeling` no longer needs it (check its
   current version) or pts stops using `domain-modeling`; then `‹domain-map›` is the index.
3. **Keep both, generate one.** A script builds the glossary map from the domain map; more
   machinery for little gain.

## Before starting

- Check what the current `domain-modeling` reads from `GLOSSARY-MAP.md` (path, format), so
  the template `templates/glossary-map.md` stays compatible with it.
- Option 1 or 2 changes `templates/config.md`, `evals/fixtures/pts.md`,
  `templates/output-format.md`, problem-definition step 1 and 2, problem-init and the
  domain-map fixtures of the evals.
