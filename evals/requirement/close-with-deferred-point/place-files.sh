#!/usr/bin/env bash
# The project context the skill reads (CLAUDE.md, glossaries, domain model, ADRs, design-the-domain config)
# comes from a checkout of a project that uses design-the-domain, named by PTS_EVAL_PROJECT; the case's own
# files are laid over it.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
# PTS_EVAL_PROJECT, or the path in evals/.pts-eval-project (local, not committed): the eval runner
# does not pass the shell environment to scaffold scripts.
project="${PTS_EVAL_PROJECT:-$(cat "$here/../../.pts-eval-project" 2>/dev/null || true)}"
: "${project:?set PTS_EVAL_PROJECT or write a project checkout with .claude/pts.md into evals/.pts-eval-project}"
cp "$project/CLAUDE.md" .
mkdir -p .claude && cp "$project/.claude/pts.md" .claude/
cp -R "$project/domain-model" .
mkdir -p docs && cp -R "$project/docs/adr" docs/
if [ -d "$here/files" ]; then cp -R "$here/files/." .; fi
# Never sync to a real ticket system from an eval.
sed 's/^| `ticket-system` |\(.*\)| [^|]* |$/| `ticket-system` |\1| `none` |/' .claude/pts.md > .claude/pts.md.tmp && mv .claude/pts.md.tmp .claude/pts.md
sed 's/^| `ticket-team` |\(.*\)| [^|]* |$/| `ticket-team` |\1| `EVAL` |/' .claude/pts.md > .claude/pts.md.tmp && mv .claude/pts.md.tmp .claude/pts.md
