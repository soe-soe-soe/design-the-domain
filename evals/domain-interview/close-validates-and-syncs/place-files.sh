#!/usr/bin/env bash
# The invented fixture project (evals/fixtures/project, see evals/fixtures/README.md), the fixture
# config and the methodology glossary; the case's own files are laid over them.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
fixtures="$here/../../fixtures"
cp -R "$fixtures/project/." .
mkdir -p domain-model/glossaries
cp "$fixtures/config.md" domain-model/config.md
cp "$fixtures/methodology.md" domain-model/glossaries/_methodology.md
if [ -d "$here/files" ]; then cp -R "$here/files/." .; fi
# Linear without a connector in the eval: the run must say it cannot sync and invent no ID.
sed 's/^| `ticket-system` |\(.*\)| [^|]* |$/| `ticket-system` |\1| `linear` |/' domain-model/config.md > domain-model/config.md.tmp && mv domain-model/config.md.tmp domain-model/config.md
sed 's/^| `ticket-team` |\(.*\)| [^|]* |$/| `ticket-team` |\1| `EVAL` |/' domain-model/config.md > domain-model/config.md.tmp && mv domain-model/config.md.tmp domain-model/config.md
