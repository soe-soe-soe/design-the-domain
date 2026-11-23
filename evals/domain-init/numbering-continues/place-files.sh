#!/usr/bin/env bash
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
mkdir -p domain-model && cp "$here/../../fixtures/config.md" domain-model/config.md
cp -R "$here/files/." .
sed 's/^| `model-init` |\(.*\)| [^|]* |$/| `model-init` |\1| `sonnet` |/' domain-model/config.md > domain-model/config.md.tmp && mv domain-model/config.md.tmp domain-model/config.md
mkdir -p domain-model/glossaries && cp "$here/../../fixtures/methodology.md" domain-model/glossaries/_methodology.md
