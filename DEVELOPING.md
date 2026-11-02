# Developing pts

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
project with a German problem space and an English solution space (`evals/fixtures/pts.md`):
case descriptions and graders are English, fixtures and user prompts German. The
`problem-definition` cases need a project checkout with `.claude/pts.md`: its path in
`evals/.pts-eval-project` (not committed; the runner does not pass the environment to scaffold
scripts) or in `PTS_EVAL_PROJECT`. They switch the ticket sync off, so no eval creates real
tickets. The others bring their files.

`claude plugin eval` only finds evals below the plugin directory, and an install copies the whole
plugin directory with no way to exclude files. That is why the published plugin is built
separately.

## Publishing

`tools/build-dist.sh [<ref>]` builds the local branch `dist` from a ref (default `HEAD`). It holds
only the allowlist in the script: `.claude-plugin/`, `skills/`, `templates/`,
`scripts/requirements.py`, `scripts/round.py`, `README.md`, `LICENSE` and `THIRD_PARTY_LICENSES.md`. Each run adds one commit, so `dist` keeps a
history of the releases.

1. Bump `version` in `.claude-plugin/plugin.json` on `main`.
2. `tools/build-dist.sh main` and `git push origin dist`.
3. Once the plugin is public: point the plugin entry in `.claude-plugin/marketplace.json` at the
   distribution branch instead of the repository root:

   ```json
   { "name": "pts", "source": { "source": "github", "repo": "soe-soe-soe/problem-test-solution-skills", "ref": "dist" } }
   ```

   Until then the entry stays `"source": "./"`, so projects using the plugin get `main` directly
   without a build step.
