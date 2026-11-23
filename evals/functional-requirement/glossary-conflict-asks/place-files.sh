#!/usr/bin/env bash
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
mkdir -p domain-model && cp "$here/../../fixtures/config.md" domain-model/config.md
cp -R "$here/files/." .
mkdir -p domain-model/glossaries && cp "$here/../../fixtures/methodology.md" domain-model/glossaries/_methodology.md
