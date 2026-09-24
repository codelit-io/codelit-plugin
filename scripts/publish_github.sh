#!/usr/bin/env bash
# Publish only this reviewed skills package, never an existing Git worktree.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="codelit-io/codelit-plugin"
export GH_HOST="github.com"
unset GH_REPO || true
cd "$ROOT"

case "${1:-}" in
  ""|--dry-run) ;;
  *) printf 'Usage: bash scripts/publish_github.sh [--dry-run]\n' >&2; exit 2 ;;
esac
if [ "$#" -gt 1 ]; then
  printf 'Unexpected additional arguments.\n' >&2
  exit 2
fi

command -v python3 >/dev/null 2>&1 || { echo 'Python 3.9+ is required.' >&2; exit 1; }
python3 scripts/validate_bundle.py

if [ "${1:-}" = "--dry-run" ]; then
  printf '\nDRY RUN: no Git initialization, GitHub calls, or publication performed.\n'
  printf 'Target: %s (PUBLIC)\n' "$TARGET"
  printf 'Source: %s\n' "$ROOT"
  printf 'Actual publication requires gh authentication and a configured Git author.\n'
  printf 'Planned command: gh repo create %s --public --source=. --remote=origin --push --homepage=https://codelit.io/\n' "$TARGET"
  exit 0
fi

for tool in git gh; do
  command -v "$tool" >/dev/null 2>&1 || { printf 'Missing required command: %s\n' "$tool" >&2; exit 1; }
done
if git rev-parse --git-dir >/dev/null 2>&1; then
  echo 'Stopped: extract a fresh copy outside an existing Git worktree. No existing history will be published.' >&2
  exit 1
fi
if ! gh auth status --hostname github.com --active >/dev/null 2>&1; then
  echo 'Authenticate first: gh auth login --hostname github.com --git-protocol https --web' >&2
  exit 1
fi
for field in user.name user.email; do
  if [ -z "$(git config --get "$field" || true)" ]; then
    printf 'Configure your own Git %s before publishing. No author identity has been guessed.\n' "$field" >&2
    exit 1
  fi
done
# A failed lookup can mean denied access or a network failure, not absence.
# Require a successful organization inventory before concluding it is absent.
repo_inventory="$(gh api --paginate "orgs/codelit-io/repos?per_page=100" --jq '.[].full_name')" || {
  echo 'Stopped: organization inventory failed; repository existence is unknown.' >&2
  exit 1
}
if printf '%s\n' "$repo_inventory" | grep -Fxq "$TARGET"; then
  printf 'Stopped: %s already exists. It has not been changed.\n' "$TARGET" >&2
  exit 1
fi

printf 'Publishing reviewed source as PUBLIC: %s\n' "$TARGET"
git init -b main
git add --all
printf '\nFiles included in the initial public commit:\n'
git diff --cached --name-only
git commit -m "Initial Codelit plugin source release v1.1.1"

if ! gh repo create "$TARGET" \
  --public \
  --source=. \
  --remote=origin \
  --push \
  --description "Codelit plugin: product plans, system architecture, and supervised agent teams" \
  --homepage "https://codelit.io/"; then
  printf '\nCreation/push did not confirm completion. The repository may already have been created.\n' >&2
  printf 'Inspect https://github.com/%s and git remote -v before any retry. No retry was performed.\n' "$TARGET" >&2
  exit 1
fi

local_sha="$(git rev-parse HEAD)"
remote_sha="$(git ls-remote origin refs/heads/main | awk '{print $1}')"
if [ "$local_sha" != "$remote_sha" ]; then
  echo 'Remote commit does not match the local commit. Do not assume publication is complete.' >&2
  exit 1
fi
visibility="$(gh api "repos/$TARGET" --jq '.visibility')"
if [ "$visibility" != "public" ]; then
  echo 'Public visibility was not confirmed. Inspect repository settings; no visibility change was retried.' >&2
  exit 1
fi
printf '\nConfirmed PUBLIC repository and matching commit: https://github.com/%s\n' "$TARGET"
printf 'Commit: %s\n' "$remote_sha"
printf 'This does not submit or publish an OpenAI directory listing.\n'
