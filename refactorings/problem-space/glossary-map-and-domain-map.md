# Glossary map and domain map overlap

## Goal

Each fact about subdomains and glossaries stands in exactly one file: either `‹glossary-map›`
or `‹domain-map›` lists which glossary belongs to which subdomain, not both.

## Why

Both files list every subdomain with a link to its glossary. A new subdomain means two rows in
two files written by different skills (problem-space-fr the domain map, problem-space-initialization and the
grilling the glossary map); sooner or later they disagree, and nobody notices because no skill
compares them.

## Current state

- **Why the glossary map exists:** Pocock's `domain-modeling` looked for `GLOSSARY-MAP.md` in the
  project root and only there. Since November 2026 pts has its own `pts:domain-modeling`
  (`docs/upstream.md`), which reads `‹glossary-map›` from the config – the root constraint is
  gone, and option 2 below no longer depends on upstream.
- `assets/domain-map.md`: per subdomain Type, Glossary link,
  Description; plus the relationships.
- `assets/glossary-map.md`: per glossary file the Subdomain and what it covers; plus the
  methodology glossary.
- Readers: requirement reads `‹glossary-map›` first to find the glossaries; problem-space-initialization
  and problem-space-fr read `‹domain-map›`. `assets/output-format.md` lists both as problem
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

- `pts:domain-modeling` is part of the plugin: change it together with the chosen option.
- Option 1 or 2 changes `assets/config.md`, `evals/fixtures/pts.md`,
  `assets/output-format.md`, requirement step 1 and 2, problem-space-initialization and the
  domain-map fixtures of the evals.
