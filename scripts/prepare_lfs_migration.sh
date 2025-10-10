#!/usr/bin/env bash
set -euo pipefail

# This script prepares for Git LFS migration. It creates a fresh clone, ensures git-lfs
# is installed, creates .gitattributes if missing, and can run 'git lfs migrate import' if asked.

SOURCE_REPO_PATH="${1:-$(pwd)}"
WORK_DIR="${2:-/tmp/eao-lfs-migrate}"
REF="${3:-main}"
RUN_MIGRATE=${4:-false}

echo "Source repo: $SOURCE_REPO_PATH"
echo "Work dir: $WORK_DIR"
echo "Ref: $REF"

# verify dependencies
if ! command -v git >/dev/null 2>&1; then
  echo "git not found in PATH. Install git before running this script." >&2
  exit 1
fi
if ! command -v git-lfs >/dev/null 2>&1; then
  echo "git-lfs not found in PATH. Install Git LFS before running this script." >&2
  exit 1
fi

rm -rf "$WORK_DIR"
git clone "$SOURCE_REPO_PATH" "$WORK_DIR"
cd "$WORK_DIR"

git lfs install || true

if [ ! -f .gitattributes ]; then
  cat > .gitattributes <<'EOF'
# Git LFS attributes for large problem datasets
problems/** filter=lfs diff=lfs merge=lfs -text
*.mexw64 filter=lfs diff=lfs merge=lfs -text
*.mat filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
EOF
  git add .gitattributes
  git commit -m "chore: add .gitattributes for Git LFS (problems/**)"
else
  echo ".gitattributes exists — review before migrating"
fi

# Preview: list top 50 large files in the repository working tree
echo "Top 50 largest files in working tree (preview):"
bash -lc "du -ah . | sort -hr | head -n 50"

if [ "$RUN_MIGRATE" = "true" ]; then
  read -p "THIS WILL REWRITE HISTORY LOCALLY. Type YES to continue: " confirm
  if [ "$confirm" != "YES" ]; then
    echo "Aborting"
    exit 1
  fi
  git lfs migrate import --include="problems/**" --include-ref=refs/heads/$REF
  git count-objects -vH
  git lfs ls-files | head -n 20 || true
  echo "Migration complete locally in $WORK_DIR. Push with: git push origin $REF --force-with-lease"
else
  echo "Dry-run complete. To run migration pass 'true' as 4th arg."
fi
