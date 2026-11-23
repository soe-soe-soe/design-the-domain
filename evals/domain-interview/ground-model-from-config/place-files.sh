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
sed 's/^| `model-ground` |\(.*\)| [^|]* |$/| `model-ground` |\1| `haiku` |/' domain-model/config.md > domain-model/config.md.tmp && mv domain-model/config.md.tmp domain-model/config.md
