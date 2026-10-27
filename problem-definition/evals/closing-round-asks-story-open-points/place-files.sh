#!/usr/bin/env bash
# The project context the skill reads (CLAUDE.md, glossaries, domain model) comes from the
# repository this case lives in; the case's own files are laid over it.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../../../../.." && pwd)"
cp "$repo/CLAUDE.md" "$repo/GLOSSARY-MAP.md" .
mkdir -p .claude/skills/templates && cp "$repo/.claude/skills/templates/output-format.md" .claude/skills/templates/
cp -R "$repo/domain-model" .
mkdir -p docs && cp -R "$repo/docs/adr" docs/
if [ -d "$here/files" ]; then cp -R "$here/files/." .; fi
