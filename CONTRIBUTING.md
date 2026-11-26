# Contributing

Welcome! This hub is public so anyone can learn Frappe and ERPNext
from it — and anyone can help make it better. Small fixes are as
welcome as big new lessons. You do not need to ask permission first:
open an issue or a pull request, and the owner reviews it before
anything is merged.

> **The one rule that matters most:** changes come only through
> fork → branch → pull request, reviewed by the owner. Nobody pushes
> directly to `main`, and nobody edits a published release.

## Ways to contribute

- **Fix a typo or a broken link** — the smallest, most useful PR.
- **Suggest a new lesson** — open an issue first with the
  lesson-request template, so we agree on the topic before you write it.
- **Add a troubleshooting entry** — one real error, in the format of
  `guides/troubleshooting.md`: exact error → when it happens → why →
  the fix, in order → prevention.
- **Add a case study** — a real project you worked on, anonymised:
  no client names, no company names, no quotes, no measured numbers.
  Approximate numbers only, and say so.
- **Add a new app to the catalog** — one entry in the right category
  file under `research/apps-catalog/`: GitHub link, install command,
  and one line on how we can use it.
- **Improve a lesson** — a clearer example, a missing common mistake,
  a command that changed in a new version.

## How to contribute (the PR flow)

1. **Fork** the repo, then create a branch: `fix/typo-lesson-05`
   or `add/lesson-frappe-mail`.
2. **Make the change in BOTH languages** — English and Roman Urdu,
   same structure, same headings. A content PR with only one language
   cannot be merged. (See the Roman Urdu rules below.)
3. **Build the docs site locally** and check your page renders:
   `sh scripts/sync-docs.sh && .venv-docs/bin/mkdocs build --clean`
   (or `mkdocs serve` to preview it in the browser).
4. **Open a pull request** with a short description of what changed
   and why. The PR template has a checklist — tick it honestly.
5. The owner reviews, asks for changes if needed, and merges.

## Content rules

- **Lesson format** — every lesson follows the same shape: what it
  is, a minimal working example with real code or commands, when to
  use it — and when not to — common mistakes, and a Next link.
- **Every claim needs a source** — official docs, Frappe Blog/Forum,
  GitHub release, or a tested example. Link the source.
- **Never promise a version you have not tested.**
- **Verify facts before writing** — check the DocType or field in the
  Frappe source or docs, not from memory. (Example: the Contact
  DocType has `user` and a `links` Dynamic Link child table — there
  is no `customer` field on Contact.)
- **No invented names, quotes, or numbers.** If a number is
  approximate, say so.
- **Keep entries short** — what, when, how to use it, source link.
- **One topic per file, beginner first.**

### Roman Urdu rules

- **0 Devanagari / Arabic-script characters** anywhere in the Urdu
  version. Roman Urdu only — Urdu written in Latin letters.
- Code, commands, DocType and field names, URLs and app names stay
  in **English**.
- The "How we can use it" line is always
  **"Hum isay kaise istemal kar sakte hain"**.
- Same headings and structure as the English file, in the same order.

## What NOT to change

- Do not delete files, rewrite published releases, or edit
  CHANGELOG history entries for released versions.
- Do not change repo settings, topics, `mkdocs.yml`, or anything
  under `.github/workflows/` — open an issue first if you think
  something there needs changing.
- Do not add a new top-level section or a new guide without
  discussing it in an issue first.

## Questions?

Open an issue — the templates (lesson request, bug report, new app)
are there to guide you. If you are not sure which one fits, pick
the closest and say so in the text.
