#!/usr/bin/env bash
# Static watcher probe for a yolo direct-PR task's recorded GitHub head.
# Emits "checks-green <check-set-sha256>" only for an open PR at that head,
# with a successful rollup AND a nonempty, entirely passing required-check
# list. If requirements cannot be listed, every reported check must pass.
# The watcher deduplicates by head and check set, not head alone: a required
# check can first report after GitHub has already called the rollup SUCCESS.
# Errors and partial reads stay silent. This grants no merge authority;
# fm-pr-merge.sh still verifies all merge conditions live.
# Separate from fm-pr-poll.sh so armed merge polls remain byte-identical.
# Usage: fm-pr-green-poll.sh <github-pull-request-url> <head-sha>
set -u
LC_ALL=C
export LC_ALL

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" || exit 0
# shellcheck source=bin/fm-pr-lib.sh
. "$SCRIPT_DIR/fm-pr-lib.sh" || exit 0

[ "$#" -eq 2 ] || exit 0
fm_pr_url_parse "$1" && [ "$FM_PR_PROVIDER" = github ] || exit 0
fm_pr_head_valid "$2" || exit 0
HEAD_SHA=$2

read_head() {
  # Owner and repository are raw strings, including all-digit names.
  # shellcheck disable=SC2016  # GraphQL variables are literal query syntax.
  gh api graphql \
    -f query='query($owner:String!,$repo:String!,$number:Int!){repository(owner:$owner,name:$repo){pullRequest(number:$number){state headRefOid commits(last:1){nodes{commit{oid statusCheckRollup{state}}}}}}}' \
    -f "owner=$FM_PR_OWNER" -f "repo=$FM_PR_REPO" -F "number=$FM_PR_NUMBER" \
    --jq '.data.repository.pullRequest | [.state, .headRefOid, .commits.nodes[0].commit.oid, .commits.nodes[0].commit.statusCheckRollup.state] | map(. // "" | tostring) | join(" ")' \
    2>/dev/null
}
reading=$(read_head) || exit 0
[ "$reading" = "OPEN $HEAD_SHA $HEAD_SHA SUCCESS" ] || exit 0

if ! checks=$(gh pr checks "$FM_PR_URL" --required --json name,workflow,bucket 2>/dev/null); then
  # gh also exits nonzero for pending/failed checks WITH a JSON list. Judge
  # that list below; never bypass known nonpassing requirements via fallback.
  if [ -z "$checks" ]; then
    checks=$(gh pr checks "$FM_PR_URL" --json name,workflow,bucket 2>/dev/null) || exit 0
  fi
fi
check_set=$(printf '%s\n' "$checks" | jq -ce '
  select(type == "array" and length > 0)
  | select(all(.[]; .bucket == "pass" and (.name | type == "string" and length > 0)))
  | map([(.workflow // ""), .name]) | unique
' 2>/dev/null) || exit 0
check_key=$(printf '%s\n' "$check_set" | fm_pr_sha256 -) || exit 0
[[ "$check_key" =~ ^[0-9a-f]{64}$ ]] || exit 0
# pr checks addresses a PR, not a SHA. Confirm it did not move or close while
# reading the checks before attaching their identity to the recorded head.
reading=$(read_head) || exit 0
[ "$reading" = "OPEN $HEAD_SHA $HEAD_SHA SUCCESS" ] || exit 0
printf 'checks-green %s\n' "$check_key"
