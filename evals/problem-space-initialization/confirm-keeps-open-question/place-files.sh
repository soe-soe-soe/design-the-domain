#!/usr/bin/env bash
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
# Same project as one-subdomain-from-code: a TODO in reminder_days gives the run an open question.
mkdir -p .claude && cp "$here/../../fixtures/pts.md" .claude/pts.md
cp -R "$here/../one-subdomain-from-code/files/." .
sed 's/^| `model-init` |\(.*\)| [^|]* |$/| `model-init` |\1| `sonnet` |/' .claude/pts.md > .claude/pts.md.tmp && mv .claude/pts.md.tmp .claude/pts.md
mkdir -p domain-model/glossaries && cp "$here/../../fixtures/methodology.md" domain-model/glossaries/_methodology.md
