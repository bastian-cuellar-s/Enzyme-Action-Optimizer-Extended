#!/usr/bin/env bash
set -euo pipefail

# extract_problems_subtree.sh
# Non-destructive helper to split the `problems/` directory into its own branch
# Usage: ./scripts/extract_problems_subtree.sh
# This creates a local branch `problems-only` with the history for `problems/`.

command -v git >/dev/null 2>&1 || { echo "git is required but not found in PATH" >&2; exit 2; }

HERE=$(pwd)
REPO_ROOT="$HERE"

echo "Creating a branch with only the 'problems/' subtree (non-destructive)..."

# Create a temporary branch and perform subtree split
git fetch --all --prune

if git show-ref --quiet refs/heads/problems-only; then
  echo "Branch 'problems-only' already exists locally. Please delete or rename it and re-run." >&2
  exit 1
fi

# Create the split branch
git subtree split --prefix=problems -b problems-only

echo
echo "Created branch 'problems-only'. To push this to a new repository or remote, run something like:"
echo
echo "  # create a new repo on GitHub and set its URL as NEW_REMOTE"
echo "  git remote add NEW_REMOTE https://github.com/your-org/problems-repo.git"
echo "  git push NEW_REMOTE problems-only:main"

echo
echo "Notes:"
echo " - This operation is non-destructive for the current repository and only creates a new local branch containing the history for the 'problems/' folder."
echo " - If you want the split branch to use a different branch name, rename 'problems-only' after creation."

echo "Done."
