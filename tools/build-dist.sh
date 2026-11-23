#!/usr/bin/env bash
# Build the distribution branch of the plugin: only what users need, without evals, refactorings
# and dev tooling. Commits onto the local branch `dist` (created on first run); push it yourself.
#
#   tools/build-dist.sh [<ref>]     default ref: HEAD
#
# The allowlist below is the published plugin. Everything else stays in the development branches.
set -euo pipefail

ref="${1:-HEAD}"
branch="dist"
include=(
  .claude-plugin/plugin.json
  skills
  assets
  scripts/requirements.py
  scripts/interview-round.py
  scripts/confluence_publish.py
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
git ls-tree -r "$source_commit" -- "${existing[@]}" | awk -F'\t' '$2 !~ /\/decision-records\//' | GIT_INDEX_FILE="$index" git update-index --index-info
tree="$(GIT_INDEX_FILE="$index" git write-tree)"

# Warn about published files that point into implement-the-domain (refactoring 011): design must
# work without it.
git ls-tree -r --name-only "$tree" | while read -r f; do
  git show "$tree:$f" | grep -n "implement-the-domain:" | sed "s#^#warning: $f: #" || true
done

# Warn about implement-the-domain calling a design skill that is not an interface (README, section
# Interfaces): a call is `design-the-domain:<skill>` without a leading slash; `/design-the-domain:…`
# only tells the user what to run.
git ls-tree -r --name-only "$source_commit" -- implement-the-domain/skills | while read -r f; do
  { git show "$source_commit:$f" | grep -noE '(^|[^/])design-the-domain:[a-z-]+' || true; } | while IFS=: read -r line ref; do
    skill="${ref##*design-the-domain:}"
    if ! git show "$source_commit:skills/$skill/SKILL.md" 2>/dev/null | grep -q '^## Interface'; then
      echo "warning: $f:$line: calls design-the-domain:$skill, which has no ## Interface"
    fi
  done
done

parent="$(git rev-parse -q --verify "refs/heads/$branch" || true)"
if [ -n "$parent" ] && [ "$(git rev-parse "$parent^{tree}")" = "$tree" ]; then
  echo "$branch already matches $(git rev-parse --short "$source_commit"), nothing to commit"
  exit 0
fi
commit="$(git commit-tree "$tree" ${parent:+-p "$parent"} -m "build: plugin from $(git rev-parse --short "$source_commit")")"
git update-ref "refs/heads/$branch" "$commit"
echo "$branch → $(git rev-parse --short "$commit") (from $(git rev-parse --short "$source_commit"))"
git ls-tree -r --name-only "$commit" | sed 's#/.*##' | sort | uniq -c
