#!/bin/sh
# Copy the hub's markdown into docs/ for the MkDocs build.
# docs/ is generated (gitignored) — the repo root stays the single
# source of truth, so lessons, guides and research are never duplicated.
set -eu
cd "$(dirname "$0")/.."
rm -rf docs
mkdir -p docs
cp -r learn guides research stylesheets docs/
cp README.md CHANGELOG.md ROADMAP.md CONTRIBUTING.md docs/
echo "docs/ synced: $(find docs -name '*.md' | wc -l) markdown files"
