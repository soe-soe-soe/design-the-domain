#!/usr/bin/env bash
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
mkdir -p domain-model && cp "$here/../../fixtures/config.md" domain-model/config.md
cp -R "$here/files/." .
