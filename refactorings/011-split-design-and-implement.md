# Refactoring 011: split into design-the-domain (problem space) and implement-the-domain (solution space)

Status: Proposed · Date: 2026-11-23

## Goal

`design-the-domain` holds the problem space only; the skills of the solution space move into a plugin
of their own, `implement-the-domain`. Each plugin has one job, a smaller surface for the OpenCode work
(refactoring 010) and a name rule that keeps its skill names unique.

## Decisions (user, 2026-11-23)

- The split follows the two spaces: problem space → `design-the-domain`, solution space →
  `implement-the-domain`.
- Skill names carry what they do in the domain; example: `grilling` becomes `domain-grilling`.

## Assignment of the skills

| Skill | Goes to | Remark |
|---|---|---|
| `requirement` | design | entry skill, user types it |
| `problem-space-story`, `problem-space-fr` | design | writers |
| `problem-space-initialization` | design | entry skill; fills config, domain map, glossary, subdomain map, FRs |
| `grilling` | design | renamed, collides with Matt Pocock's `grilling` |
| `domain-modeling` | design | **must be renamed**: collides with Matt Pocock's `domain-modeling` |
| `solution-definition`, `solution-init` | implement | |
| `story-workflow`, `test-definition` | implement | `story-workflow` calls `requirements.py` of design |
| `tdd`, `code-review`, `codebase-design` | implement | all three collide with Matt Pocock's skills; `code-review` also with Claude's built-in |

## Name rule (proposal)

1. A name says its area and its function: `problem-space-…`, `domain-…` in design; `implement-…` in
   implement.
2. A name is in no known collection: Matt Pocock, Anthropic, Superpowers, built-ins of Claude Code and
   OpenCode. The build checks every name against a deny list and against doubles in the own plugin
   (OpenCode overrides a duplicate `name` silently, see refactoring 010).
3. Entry skills the user types keep a short name as long as they pass the check (`requirement`).
4. Folder name and `name:` are the same; `npx skills` names the target folder after `name:`.

Candidates still to settle: new name of `domain-modeling` (it writes glossary rows and ADRs, so
something like `domain-glossary` or `domain-language`), names of the three skills that collide in
implement (`implement-tdd`, `implement-review`, `implement-design`).

## Questions to settle before starting

1. **One repository with two plugins or two repositories.** A marketplace file can list both plugins.
   One repository keeps the shared build and moves cheaply; two repositories separate the histories.
   [Vermutung: one repository for the split, a later move stays easy.]
2. **`scripts/requirements.py`** (status of stories, `complete`, `check`, `next-fr`) manages stories and
   FRs, so it belongs to design; `story-workflow` in implement calls it. Either implement's build
   vendors a copy (two states to keep in step, with a version check) or implement requires the design
   plugin. Claude Code plugins have no declared dependency [Vermutung, not checked].
3. **Config `domain-model/config.md`** is one file with the sections of both plugins. The init skill of
   design fills Project, Problem space, the code keys it reads (`backend`, `backend-shared`,
   `backend-tests`, `architecture-adrs`), Ticket system and the models it uses; the sections Solution
   space, Code (the rest) and Commands belong to implement, which fills them the same way
   (its own config step). The template is split in two parts of one file.
4. **The pilot project:** where the solution-space skills stand today stays as it is (they were never in
   `dist`); the new plugin gets its own marketplace entry and `dist` build.
5. **Version:** design becomes 0.9.0 or 1.0.0 (name changes of skills break callers).

## Plan

1. Settle the questions above and the names.
2. Move the solution-space skills, their evals (`solution-definition/*`, `test-definition/*`), the
   assets only they use and their config keys into the new plugin; no change of behaviour.
3. Rename `grilling`, `domain-modeling` (design) and the three colliding skills (implement), with all
   cross-references; the build check of the name rule.
4. Cut the config template and the config step of the init skill to the design part.
5. Marketplace entries and `dist` builds for both plugins.

## Effects on other refactorings

- 005 (stable evals) shrinks to the evals of design; the evals of implement move with their skills.
- 010 (OpenCode) works on design only; implement follows the same build and adapter later.
