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
  LICENSE
  THIRD_PARTY_LICENSES.md
)

# Skills of the solution space stay in the repository but are not published until it is finished.
unreleased=(code-review codebase-design solution-definition solution-init tdd test-definition story-workflow)
unreleased_re="^skills/($(IFS='|'; echo "${unreleased[*]}"))/"

cd "$(git rev-parse --show-toplevel)"
source_commit="$(git rev-parse --verify "$ref^{commit}")"

index="$(mktemp)"
trap 'rm -f "$index"' EXIT
rm -f "$index"

existing=()
for path in "${include[@]}"; do
  if git cat-file -e "$source_commit:$path" 2>/dev/null; then existing+=("$path"); fi
done
git ls-tree -r "$source_commit" -- "${existing[@]}" | awk -F'\t' -v re="$unreleased_re" '$2 !~ /\/decision-records\// && $2 !~ re' | GIT_INDEX_FILE="$index" git update-index --index-info
tree="$(GIT_INDEX_FILE="$index" git write-tree)"

# Warn about published files that still point to an unreleased skill.
names="$(IFS='|'; echo "${unreleased[*]}")"
git ls-tree -r --name-only "$tree" | while read -r f; do
  git show "$tree:$f" | grep -nE "define-the-domain:($names)\b" | sed "s#^#warning: $f: #" || true
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
