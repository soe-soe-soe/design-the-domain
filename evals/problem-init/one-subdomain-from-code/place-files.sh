#!/usr/bin/env bash
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
mkdir -p .claude && cp "$here/../../fixtures/pts.md" .claude/pts.md
cp -R "$here/files/." .
sed 's/^| `model-init` |\(.*\)| [^|]* |$/| `model-init` |\1| `sonnet` |/' .claude/pts.md > .claude/pts.md.tmp && mv .claude/pts.md.tmp .claude/pts.md
mkdir -p domain-model/glossaries && cp "$here/../../fixtures/methodology.md" domain-model/glossaries/_methodology.md
