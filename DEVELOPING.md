# Developing design-the-domain

This file, `evals/`, `refactorings/`, `tools/` and the script tests are for development only.
They are not part of the published plugin (see Publishing).

## Working copy

Load the working copy instead of the installed plugin with `claude --plugin-dir <this repo>` and
`/reload-plugins` after an edit. Decision records stay with their skill under `decision-records/`.
The script's tests run with `python3 -m unittest discover scripts`.

## Evals

Evals live under `evals/<skill>/<case>/` and run with
`claude plugin eval . --scaffold --allow-tools Bash Write Edit` (`--tag problem-space` for the
problem space). Shell tools run sandboxed, so Linux needs `bubblewrap` and `socat`. They simulate a
project with a German problem space and an English solution space (`evals/fixtures/config.md`):
case descriptions and graders are English, fixtures and user prompts German. The
`requirement` cases need a project checkout with `domain-model/config.md`: its path in
`evals/.pts-eval-project` (not committed; the runner does not pass the environment to scaffold
scripts) or in `PTS_EVAL_PROJECT`. They switch the ticket sync off, so no eval creates real
tickets. The others bring their files.

`claude plugin eval` only finds evals below the plugin directory, and an install copies the whole
plugin directory with no way to exclude files. That is why the published plugin is built
separately.

## Publishing

`tools/build-dist.sh [<ref>]` builds the local branch `dist` from a ref (default `HEAD`). It holds
only what the plugin needs to run: `.claude-plugin/plugin.json`, `skills/` without their
`decision-records/`, `assets/`, `scripts/requirements.py`, `scripts/interview-round.py`, `LICENSE` and
`THIRD_PARTY_LICENSES.md`. No evals, refactorings, docs or development tooling. Each run adds one
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
