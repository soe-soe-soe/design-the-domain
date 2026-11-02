#!/usr/bin/env bash
# Build the distribution branch of the plugin: only what users need, without evals, refactorings
# and dev tooling. Commits onto the local branch `dist` (created on first run); push it yourself.
#
#   tools/build-dist.sh [<ref>]     default ref: HEAD
#
# The allowlist below is the published plugin, without the decision records of the skills.
# Everything else stays in the development branches.
set -euo pipefail

ref="${1:-HEAD}"
branch="dist"
include=(
  .claude-plugin
  skills
  templates
  scripts/requirements.py
  scripts/round.py
  README.md
  LICENSE
  THIRD_PARTY_LICENSES.md
)

cd "$(git rev-parse --show-toplevel)"
source_commit="$(git rev-parse --verify "$ref^{commit}")"

index="$(mktemp)"
trap 'rm -f "$index"' EXIT
rm -f "$index"

existing=()
for path in "${include[@]}"; do
  if git cat-file -e "$source_commit:$path" 2>/dev/null; then existing+=("$path"); fi
done
git ls-tree -r "$source_commit" -- "${existing[@]}" | grep -v "/decision-records/" | GIT_INDEX_FILE="$index" git update-index --index-info
tree="$(GIT_INDEX_FILE="$index" git write-tree)"

parent="$(git rev-parse -q --verify "refs/heads/$branch" || true)"
if [ -n "$parent" ] && [ "$(git rev-parse "$parent^{tree}")" = "$tree" ]; then
  echo "$branch already matches $(git rev-parse --short "$source_commit"), nothing to commit"
  exit 0
fi
commit="$(git commit-tree "$tree" ${parent:+-p "$parent"} -m "build: plugin from $(git rev-parse --short "$source_commit")")"
git update-ref "refs/heads/$branch" "$commit"
echo "$branch → $(git rev-parse --short "$commit") (from $(git rev-parse --short "$source_commit"))"
git ls-tree -r --name-only "$commit" | sed 's#/.*##' | sort | uniq -c
