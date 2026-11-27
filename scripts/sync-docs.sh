#!/bin/sh
# Copy the hub's markdown into docs/ for the MkDocs build.
# docs/ is generated (gitignored) — the repo root stays the single
# source of truth, so lessons, guides and research are never duplicated.
# Layout: docs/en/ = English (repo root), docs/ur/ = Roman Urdu
# (i18n/ur/). Files missing in ur/ (CHANGELOG, ROADMAP) fall back to
# English via mkdocs-static-i18n. Stylesheets go in both so the theme
# (logo, favicon, CSS) resolves in each language build.
set -eu
cd "$(dirname "$0")/.."
rm -rf docs
mkdir -p docs/en docs/ur
cp -r learn guides research stylesheets docs/en/
cp README.md CHANGELOG.md ROADMAP.md CONTRIBUTING.md docs/en/
cp -r i18n/ur/* docs/ur/
cp -r stylesheets docs/ur/
# Also at docs/ root, so the social plugin finds the logo at
# docs/stylesheets/logo.svg (it resolves theme.logo from docs_dir).
cp -r stylesheets docs/
echo "docs/ synced: $(find docs/en -name '*.md' | wc -l) English + $(find docs/ur -name '*.md' | wc -l) Roman Urdu markdown files"
