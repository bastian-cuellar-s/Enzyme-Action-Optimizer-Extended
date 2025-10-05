#!/usr/bin/env bash
set -euo pipefail

# Build sdist and wheel and bundle them into a single zip for release.
# Usage: ./scripts/build_release.sh

python -m pip install --upgrade build
python -m build --sdist --wheel

if [ -d dist ]; then
  # -j to junk the paths inside the zip
  if command -v zip >/dev/null 2>&1; then
    zip -j dist/release_artifacts.zip dist/*
    echo "Created dist/release_artifacts.zip"
  else
    echo "zip not found; leaving artifacts in dist/"
    ls -la dist
  fi
else
  echo "No dist folder created." >&2
  exit 1
fi
