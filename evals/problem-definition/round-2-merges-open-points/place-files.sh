#!/usr/bin/env bash
# The project context the skill reads (CLAUDE.md, glossaries, domain model, ADRs, pts config)
# comes from a checkout of a project that uses pts, named by PTS_EVAL_PROJECT; the case's own
# files are laid over it.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
project="${PTS_EVAL_PROJECT:?set PTS_EVAL_PROJECT to a project checkout that has .claude/pts.md}"
cp "$project/CLAUDE.md" "$project/GLOSSARY-MAP.md" .
mkdir -p .claude && cp "$project/.claude/pts.md" .claude/
cp -R "$project/domain-model" .
mkdir -p docs && cp -R "$project/docs/adr" docs/
if [ -d "$here/files" ]; then cp -R "$here/files/." .; fi
