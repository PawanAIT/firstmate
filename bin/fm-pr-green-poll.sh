#!/usr/bin/env bash
# Static watcher program that reports when a yolo direct-PR task's GitHub pull
# request turns green at the head its merge poll recorded.
# It prints exactly one checks-green line when the pull request is open, its
# live head and newest commit are both exactly <head-sha>, and GitHub reports
# that commit's combined check state as SUCCESS. It prints nothing otherwise,
# including when no check has reported yet and on every error, so a failed or
# partial read is never taken for green.
# bin/fm-watch.sh runs it only after a validated merge poll for the task read no
# merge, passing that poll's canonical URL and the task's recorded pr_head=, and
# owns the once-per-head wake. It merges nothing: bin/fm-pr-merge.sh verifies
# every merge condition live when firstmate acts on the wake.
# It is a separate program rather than a branch of bin/fm-pr-poll.sh because
# every armed merge poll must stay byte-identical to that template.
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

# The combined state is GitHub's own verdict over every check reported on that
# commit, and it is null while nothing has reported. Owner and repository go as
# raw strings so an all-digit name is never retyped as a number.
# shellcheck disable=SC2016  # GraphQL variables are literal query syntax.
reading=$(gh api graphql \
  -f query='query($owner:String!,$repo:String!,$number:Int!){repository(owner:$owner,name:$repo){pullRequest(number:$number){state headRefOid commits(last:1){nodes{commit{oid statusCheckRollup{state}}}}}}}' \
  -f "owner=$FM_PR_OWNER" -f "repo=$FM_PR_REPO" -F "number=$FM_PR_NUMBER" \
  --jq '.data.repository.pullRequest | [.state, .headRefOid, .commits.nodes[0].commit.oid, .commits.nodes[0].commit.statusCheckRollup.state] | map(. // "" | tostring) | join(" ")' \
  2>/dev/null) || exit 0
[ "$reading" = "OPEN $HEAD_SHA $HEAD_SHA SUCCESS" ] && printf '%s\n' checks-green
exit 0
