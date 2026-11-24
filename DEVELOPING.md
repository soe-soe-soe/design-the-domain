# Developing design-the-domain

This file, `evals/`, `refactorings/`, `tools/` and the script tests are for development only.
They are not part of the published plugin (see Publishing).

## Working copy

The skills are self-contained only in the build output: their texts name `assets/…` and `scripts/…`
relative to the skill's base directory, and `tools/build.py` copies what each skill needs into its
folder (derived from the paths its files name, no list; see the docstring). So load the build, not the
source: `python3 tools/build.py --with-evals`, then `claude --plugin-dir build/design-the-domain`, and
rebuild plus `/reload-plugins` after an edit. `python3 tools/build.py --with-evals --check` fails when
`build/` is stale. `python3 tools/build.py --target opencode` builds the OpenCode variant
(`build/opencode/`: namespace-free skills, `commands/` wrappers; install in a test project with
`apm install <path> --target opencode`). `python3 -m unittest tools/test_build.py` tests the build. The build also checks the skill names (folder = `name:`, no collision with
`tools/denied-skill-names.txt` or `implement-the-domain/`). Decision records stay with their skill under `decision-records/`.
The script's tests run with `python3 -m unittest discover scripts`.

## Evals

Evals live under `evals/<skill>/<case>/` and run **from the build output** (`cd build/design-the-domain`,
built with `--with-evals`) with `claude plugin eval . --ablation none --scaffold --allow-tools Bash Write Edit`
(`--tag problem-space` for the problem space). Without `--ablation none` the runner adds a
no-plugin baseline arm and doubles the runs. It also finds the evals of `implement-the-domain/`
(`--eval-dir evals` does not keep them out): run single cases with `--case <name>`. The judge is the runner's default, Haiku: a Sonnet judge costs about
$7 per run instead of $0.50, reruns too (Sonnet was not steadier). Each case runs three times (the runner's default;
no case sets `runs`). Shell tools run sandboxed, so Linux needs `bubblewrap` and `socat`. They
simulate a project with a German problem space and an English solution space
(`evals/fixtures/config.md`): case descriptions and graders are English, fixtures and user prompts
German. The `domain-interview` cases copy the invented sample project `evals/fixtures/project/` (see
`evals/fixtures/README.md`) and lay their own files over it; the other cases bring their files.
No eval reads a real project, and none syncs to a real ticket system (`ticket-system` is `none`,
or `linear` without a connector).

A case is stable when it passes 3 of 3 runs, or at least 5 of 6 after three more runs. A case
below that has a defect in its skill or its grader: fix it, don't rerun until it is green.

### Rules for graders

- One checkable claim per grader. Where the claim is a fixed text, use a `type: regex` grader
  (`target: trace | last_message | {source: file, path: …}`, `pattern`, `match: contains |
  not_contains | count:N`): it needs no judge, costs nothing and does not vary. The judge sees at
  most 100,000 characters of a trace, so a long run's Write calls may be cut off; regex sees all.
- Name the exact text, tag, file or tool call expected; no "appropriate", "sensible" or "tries to".
- Demand nothing the skill does not prescribe; where the skill allows two ways, the grader allows
  both.
- `focus: {source: file, path: …}` when the claim is about one file's content; `focus: files` shows
  the judge only the list of file paths, so use it only for which files exist; `focus: trace` for
  what the run did (tool calls and their contents, subagents, the final message).
- "Unchanged" means no Write or Edit call on the file, not a comparison the judge cannot make.
- Fixtures are invented; terms, FRs and stories a grader names exist in the case's files or in
  `evals/fixtures/project/`.

`claude plugin eval` only finds evals below the plugin directory, and an install copies the whole
plugin directory with no way to exclude files. That is why the published plugin is built
separately.

## Publishing

`tools/build-dist.sh [<ref>]` builds the local branch `dist` from a ref (default `HEAD`), as the output
of `tools/build.py` run on that ref's committed files. It holds only what the plugin needs to run:
`.claude-plugin/plugin.json`, the OpenCode build in `opencode/`, `skills/` without their `decision-records/` and with the `assets/` and
`scripts/` each skill needs inside its folder, `LICENSE` and `THIRD_PARTY_LICENSES.md`. No evals, refactorings, docs or development tooling. Each run adds one
commit, so `dist` keeps a history of the releases.

The marketplace (`.claude-plugin/marketplace.json` on `main`) points the plugin entry at the branch
`dist` of this repository, so projects get exactly that build:

```json
{ "name": "design-the-domain", "source": { "source": "github", "repo": "soe-soe-soe/design-the-domain", "ref": "dist" } }
```

Release:

1. Bump `version` in `.claude-plugin/plugin.json` on `main` (an unchanged version can keep an old
   copy in the plugin cache).
2. `tools/build-dist.sh main`, then `git push origin main dist`.
3. In a project: update the marketplace and the plugin (`/plugin`), then `/reload-plugins`.

## implement-the-domain (refactoring 011)

The solution-space skills and their evals live in `implement-the-domain/`, a plugin of its own
(scaffold, not published). Load it with `claude --plugin-dir implement-the-domain`; its evals run
from that folder.
