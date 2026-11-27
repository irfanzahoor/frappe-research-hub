# Changelog

All notable changes to the Frappe Research Hub. Dates are in Asia/Karachi.

## Unreleased

### Added

- **Docs website** — the hub now reads as a website at
  https://irfanzahoor.github.io/frappe-research-hub/ (MkDocs Material:
  search, sidebar navigation, dark/light mode, dark-blue brand).
  `mkdocs.yml` + `stylesheets/extra.css` + `scripts/sync-docs.sh`
  build it from the repo's own markdown — no content is duplicated.
  Deployed to the `gh-pages` branch (GitHub Pages, branch source) by
  `workspace/custom-connectors/custom.github-research-hub/bin/deploy_pages.py`;
  redeploy after every content push until the token gains the Workflows
  permission, when `.github/workflows/docs.yml` (already written, not
  yet pushed — GitHub blocks workflow files for tokens without that
  permission) can take over auto-deploy.
- **Docs UI polish** — Inter for text, JetBrains Mono for code; custom
  dark-blue logo + favicon; bolder headings with dark-blue titles;
  dark-blue table headers with zebra rows; rounded code blocks and
  admonitions; "Edit this page" / "View source" links on every page
  (GitHub edit).
- **Docs theme** — navy / gold / teal (the LinkedIn banner colours):
  navy gradient header with a gold rule, teal links, gold title bar
  under every page heading. Dark mode included.
- **Roman Urdu version** — the whole hub translated into Roman Urdu
  (62 files: all 21 Framework lessons, 14 ERPNext modules, 9 guides,
  research, root pages). Code, commands, DocType/field names and URLs
  stay in English; prose is Roman Urdu. Switch languages from the
  header: English at `/`, Roman Urdu at `/ur/`. The label
  "How we can use it" is standardised to
  "Hum isay kaise istemal kar sakte hain" across the Urdu version.
  CHANGELOG and ROADMAP stay in English (fallback) in the Urdu site.
- **Urdu site is LTR, like English** — the Roman Urdu version uses
  the same left-to-right layout as English (`dir="ltr"` forced in
  the theme config, overriding Material's automatic RTL for the `ur`
  locale). Roman Urdu is Latin script, so it reads like English.
  (It was briefly RTL; changed at the owner's request.)
  Blockquotes use logical CSS, so their accent bar stays correct
  in either direction.
- **SEO + social cards** — the docs site now generates one Open Graph
  card image per page (MkDocs Material `social` plugin, navy `#0b2a5b`
  background, white text, Inter, hub logo; needs Pillow + cairosvg in
  `.venv-docs`), so shared links show a proper preview on LinkedIn /
  X. Key pages (both homepages, guides index, research history +
  apps catalog, the four new guides) have a specific `description:`
  in front matter, in their own language (English / Roman Urdu),
  under 160 characters; other pages fall back to the site
  description. `site_url` is set, so cards and the sitemap use
  absolute URLs. Still manual: submit the sitemap in Google Search
  Console.
- **Troubleshooting / error library** — `guides/troubleshooting.md`
  (English + Roman Urdu): 22 real, common Frappe/ERPNext errors in
  three stages — Setup & Install (wrong versions, MariaDB access
  denied / not running, Redis refused, `bench build`, missing
  `frappe` module, port in use), Development (migrate patch failures,
  Unknown column, Not Permitted, Data too long, link validation,
  mandatory-but-hidden field, scripts not running, stale print
  format), and Production & Go-live (Something went wrong, scheduler
  not running, email queue stuck, `bench update` merge conflicts,
  restore version mismatch, 504 timeouts, blank Desk after update).
  Every entry has the same format — exact error, when it happens,
  why, the fix in order, and prevention — plus a "first 3 checks"
  section and a "still stuck?" section pointing at Lesson 16 and the
  Frappe Forum. Error text and fixes verified against Frappe docs,
  Frappe Cloud docs and the Forum; v16 requirements (Python 3.14,
  Node 24, MariaDB 11.8) from the `pyproject.toml` ranges.
- **Practice project / capstone guide** — `guides/practice-project.md`
  (English + Roman Urdu): build a spice factory end to end in 8 phases
  — bench/site/app and masters, Gate Pass register, BOM + Work Order +
  Stock Entry (Manufacture), Sales Order → Delivery Note → Sales
  Invoice, Quality Inspection gate before dispatch, Payment Entry +
  Gate Pass approval workflow, Order-to-Cash Script Report + invoice
  print format, then permissions, backup and go-live. Every phase names
  the lessons it uses, has concrete steps with real code and bench
  commands, a checkpoint, and common mistakes. DocType fields verified
  against ERPNext v16 source; the Gate Pass matches Lesson 03 exactly.
- **Case studies** — `guides/case-studies.md` (English + Roman Urdu):
  three anonymised production case studies in the same shape
  (background → problem → solution → what went wrong → results →
  what to take from it): a spice manufacturer (batch-wise stock,
  submit-blocking Quality Inspection gate, BOM costing), a
  trading/distribution business (order-to-cash flow, credit limits,
  delivery tracking, Gate Pass), and a services company (Projects +
  Timesheets + invoicing, approval workflows, client portal). No
  client names, company names, quotes or measured metrics — every
  number is framed as approximate, by design — plus a shared
  lessons section and an invitation to contribute your own case
  study. Each case links to the hub lessons it uses.
- **Cheat sheets** — `guides/cheat-sheets.md` (English + Roman
  Urdu): one-page quick reference in 5 scannable sections — bench
  commands (28, from `bench init` to `bench doctor`, with `<site>`
  placeholders), hooks (`hooks.py`: doc_events, scheduler_events,
  fixtures, permission hooks, jinja, page/app includes, route rules,
  one-line example each), Server Script / API essentials
  (`frappe.get_doc` / `get_list` / `get_all` / `new_doc`,
  `db.get_value` / `db.set_value` / parameterised `db.sql`,
  `msgprint` / `throw`, `@frappe.whitelist`, `frappe.call`,
  `frappe.ui.form.on` skeleton, `frm` vs `cur_frm`, filter
  operators), a DocType field-types table (18 types with "use when"),
  and a permissions & roles table (standard roles + the 3 most
  common permission mistakes from Lesson 09). Commands verified
  against the official Frappe bench cheatsheet; unconfirmed commands
  (`bench stop`, Postgres console) left out rather than guessed.
- **Language switch, visible** — both homepages now link to the other
  language at the top, and the header language selector has a gold
  outline so it is easy to spot on every page.
- **Fixed: Edit / View-source links** — with the en/ + ur/ folder
  layout, MkDocs built edit links as `.../edit/main/en/learn/...`
  and `.../edit/main/ur/learn/...`, neither of which exists on main.
  A build hook (`hooks/fix_edit_url.py`) now rewrites them per page:
  English pages point at `learn/...`, Roman Urdu pages at
  `i18n/ur/learn/...`. The View-source (raw) links are derived from
  the same URL, so they are fixed too. Verified: 0 broken GitHub
  links left across all 119 pages.
- **Community contributions setup** — `CONTRIBUTING.md` (English +
  Roman Urdu) expanded from 4 bullets into a full guide: ways to
  contribute (typo/link fix, new lesson, troubleshooting entry,
  anonymised case study, new app for the catalog), the PR flow
  (fork → branch → PR → owner review), content rules (lesson format,
  every claim needs a source, verify facts before writing, no
  invented names/quotes/numbers, every content PR needs BOTH
  English and Roman Urdu), and what not to change. New GitHub issue
  templates (`.github/ISSUE_TEMPLATE/`: lesson-request, bug-report,
  new-app) and a pull request template (`.github/pull_request_template.md`)
  with an EN+UR / links / facts checklist. The Contributing page is
  already in the docs nav (About → Contributing). GitHub Discussions
  was then enabled on the repo via the API (the token's Administration
  permission covers it) — verified `has_discussions: true`.
- **Interview prep guide** — `guides/interview-prep.md`
  (English + Roman Urdu): 36 interview questions with short model
  answers in 5 sections — Frappe Framework basics (10), ERPNext
  functional (8: order-to-cash, buying/stock, manufacturing, BOM,
  batch vs serial, HR, CRM), code & debugging (8: spot-the-bug with
  real snippets — f-string SQL injection, JS field-hiding is not
  security, `validate` vs `before_insert`, `None` from `get_value`,
  `frappe.enqueue`, `cur_frm`, `save` vs `submit`, N+1 queries),
  scenario questions (6: discount approval workflow, gate-pass
  register, custom report, Excel migration, slow report, production
  bug at 5pm), and HR / behavioural (4). Ends with a one-week
  revision plan mapping each day to the hub lessons to revise, and
  every section links to the lesson that teaches it. No invented
  salaries, companies or hiring claims — every answer verified
  against the hub's own lessons.
- **Page comments (giscus)** — every lesson and guide page now has a
  Comments section at the bottom, backed by GitHub Discussions
  (category "General", one discussion per page, `overrides/partials/comments.html`
  wired through the theme's `custom_dir`). Readers can ask questions
  right under the lesson they are reading. The giscus GitHub App
  still needs the owner to install it at https://github.com/apps/giscus
  on this repo — until then the widget shows a "giscus is not
  installed on this repository" message instead of a comment box.
- **Demo app code** — `demo-app/lal_mirch_foods/` (linked from the
  practice-project guide, English + Roman Urdu): the practice
  project's Gate Pass as a real, minimal, installable Frappe app —
  Gate Pass + Gate Pass Item DocType JSONs (fields exactly as Lesson
  03, structure modelled on the real Frappe v16 `ToDo`, `DocField`
  and `DocType Link` files), controller validation (no future dates,
  positive qty), the Phase 2 client script, a `doc_events` validate
  hook, a daily scheduler job that files ToDos for stale draft
  Delivery passes, two unit tests, and a `pyproject.toml` in the
  `bench new-app` form. Install is a manual copy into the bench's
  `apps/` folder (`bench get-app` cannot install a subfolder) —
  documented in `demo-app/README.md`. Left out on purpose: the print
  format (Jinja to paste into Desk, per the guide) and the rest of
  the project (BOMs, Work Orders, reports stay as guide steps).
- **Learning paths** — `guides/learning-paths.md` (English + Roman
  Urdu): two ordered tracks through the hub, top of the Guides
  section. The Developer Mastery Track runs Level 1 → 2 → 3 →
  ERPNext Operations → Level 4, with the ERPNext Core modules
  interleaved after Level 2, a hands-on checkpoint after each stage
  (done only when it can be completed without opening the hub), the
  practice project as capstone with the demo app as reference — not
  a shortcut — and interview prep as the final check; mastery is
  defined explicitly (build the Gate Pass app + the practice-project
  flow from a blank bench, without the hub). The Functional Guidance
  Track needs no code: what Frappe/ERPNext is, the business flows,
  choosing apps, case studies, working with developers, and what
  can go wrong — ending with how to use it in a real
  implementation. Time estimates are labelled rough. README intro
  reframed to the same purpose (a personal Noob-to-Pro mastery path:
  developers master Frappe by doing it, functional people use it
  for guidance); guides count is now 10.

## v1.0 — 2026-11-26

The full path is written: all 21 Framework topics, all 14 ERPNext
modules, all 4 guides. A learner can go from zero to a production
ERPNext implementation using only this hub plus the linked skills repo.

### Added

- **Learn: Frappe Framework — Level 4 (5 lessons)**
  - `learn/framework/level-4/17-studio-flow.md` — Studio mini-app
    (hands-on) and Flow (beta, permission-aware AI in Desk).
  - `learn/framework/level-4/18-insights.md` — Insights dashboards in
    Desk: Workbook, Query, Chart, Dashboard.
  - `learn/framework/level-4/19-website-portal.md` — Frappe Website,
    Web Forms, customer portal pages (`www/`, `get_context`).
  - `learn/framework/level-4/20-upgrades.md` — upgrades, lesson-length
    version (deep reference: upgrade guide).
  - `learn/framework/level-4/21-ops.md` — backups, monitoring,
    multi-site benches, Frappe Cloud vs self-hosted.
- **Guides**
  - `guides/choosing-apps.md` — when to install an app vs build it:
    the 5 questions, install/build/extend, red flags, worked example,
    upgrade cost of every app.

### Fixed

- Corrected the portal example in `learn/framework/level-4/19-website-portal.md`:
  Contact has no direct `customer` field — the Customer link lives in
  its Dynamic Link child table, resolved in two steps (verified against
  the Contact DocType in Frappe v16).
- Aligned Frappe Flow's status to **beta** (official docs) in
  `learn/erpnext/v16/13-studio-flow-insights.md` — it was called alpha
  in the v16.60 launch notes; the history entry for the launch keeps the
  original wording.

## v0.2.0-beta — 2026-11-26

### Added

- **Learn: Frappe Framework — Level 2 (6 lessons)**
  - `learn/framework/level-2/05-server-scripts-events.md` — controller
    hooks, Server Scripts, `doc_events` in hooks.py.
  - `learn/framework/level-2/06-client-scripts.md` — form behaviour,
    validation hints, UX (`frm` events, `set_query`, buttons).
  - `learn/framework/level-2/07-apis.md` — `frappe.call`, whitelisted
    methods, REST API, `bench execute`.
  - `learn/framework/level-2/08-reports-print-formats.md` — Script Reports,
    Query Reports, Jinja print formats.
  - `learn/framework/level-2/09-permissions-roles.md` — Role Permissions,
    field-level permissions, User Permissions, sharing.
  - `learn/framework/level-2/10-workflows-assignments.md` — Workflows
    (states, transitions, docstatus rules) and Assignment Rules.
- **Learn: Frappe Framework — Level 3 (6 lessons)**
  - `learn/framework/level-3/11-scheduler-jobs.md` — Scheduler,
    background jobs, queues (`frappe.enqueue`, `scheduler_events`).
  - `learn/framework/level-3/12-notifications-email.md` — Notifications,
    `frappe.sendmail`, realtime, webhooks.
  - `learn/framework/level-3/13-testing.md` — unit/integration tests,
    test data, UI tests (Cypress).
  - `learn/framework/level-3/14-performance.md` — N+1 queries, indexes,
    caching, denormalizing.
  - `learn/framework/level-3/15-security.md` — SQL injection, XSS,
    permissions, secrets, files, audit.
  - `learn/framework/level-3/16-debugging.md` — tracebacks, logs,
    `bench console`, common errors, asking for help.
- **Learn: ERPNext — remaining 10 modules**
  - `learn/erpnext/operations/05-manufacturing.md` — BOM, Work Orders,
    Job Cards, Production Plan, subcontracting (fmc examples).
  - `learn/erpnext/operations/06-quality.md` — Quality Inspections,
    quarantine, Quality Goals and Actions.
  - `learn/erpnext/operations/07-projects.md` — Projects, Tasks,
    Timesheets, costing, profitability.
  - `learn/erpnext/operations/08-assets.md` — Asset lifecycle,
    depreciation, maintenance, movement.
  - `learn/erpnext/people/09-hr.md` — Employees, leave, attendance,
    payroll, shifts (Frappe HR in v16).
  - `learn/erpnext/people/10-crm.md` — Frappe CRM (leads, deals, web
    forms); legacy ERPNext CRM scheduled for removal in v17.
  - `learn/erpnext/people/11-helpdesk.md` — HD Tickets, SLAs, knowledge
    base (Frappe Helpdesk).
  - `learn/erpnext/people/12-support-portal.md` — customer portal,
    Portal Users, communication.
  - `learn/erpnext/v16/13-studio-flow-insights.md` — Studio mini-apps,
    Flow AI, Insights dashboards in Desk.
  - `learn/erpnext/v16/14-cross-module-flows.md` — forecast → MPS → MRP,
    sales → stock → accounts, production → QC → sales.

### Fixed

- Corrected the legacy ERPNext CRM removal claim: it is scheduled for
  removal in **v17**, not v16 (ERPNext docs, Frappe Blog Nov 2026).
  Fixed in `learn/erpnext/people/10-crm.md` and
  `research/history-2024-2026.md`.
- **Guides**
  - `guides/upgrade-v14-v15-v16.md` — upgrade rules, readiness check,
    backup + restore test, upgrade order, breaking changes v14→v15 and
    v15→v16, patches, staging test plan, rollback, checklists.
  - `guides/go-live-checklist.md` — data import order, opening balances,
    permissions, training, cutover, backups, monitoring, rollback,
    go-live day runbook, tickable checklist.

## v0.1.0-alpha — 2026-11-26

First real content. The beginner path is no longer an outline — it has
lessons you can actually follow.

### Added

- **Learn: Frappe Framework — Level 1 (4 lessons)**
  - `learn/framework/level-1/01-what-is-frappe.md` — Framework vs ERPNext
    vs Frappe Cloud.
  - `learn/framework/level-1/02-bench-sites-apps.md` — bench install, first
    site, first app (v16 commands).
  - `learn/framework/level-1/03-first-doctype.md` — your first DocType:
    fields, field types, layout rules (Section / Column Breaks, 2 fields
    per row, child table in its own section, max 4–5 list columns).
  - `learn/framework/level-1/04-desk-list-form.md` — Desk, List View,
    Form View: how users actually work.
- **Learn: ERPNext — Core modules (4 lessons)**
  - `learn/erpnext/core/01-accounting.md` — Chart of Accounts, GL,
    invoicing, payments, tax.
  - `learn/erpnext/core/02-stock-inventory.md` — warehouses, batches,
    serials, FEFO, valuation.
  - `learn/erpnext/core/03-selling.md` — quotations, sales orders,
    delivery, pricing.
  - `learn/erpnext/core/04-buying.md` — purchase orders, receipts,
    supplier workflow (three-way match).
  - Every module lesson ends with a real use case and a "How we can use it"
    line for NexTash / client work.
- **Guides**
  - `guides/common-mistakes.md` — field layout, hooks in the wrong place,
    permission mistakes, performance mistakes (N+1, missing indexes),
    ledger/stock rules, plus a pre-ship checklist.
- **Research — complete as of 26 Nov 2026**
  - `research/history-2024-2026.md` — 18 major changes, Nov 2024–Nov 2026.
  - `research/apps-catalog.md` — 66 useful apps in 11 categories, each
    category in its own file under `research/apps-catalog/`.

## v0.1.0 — 2026-11-26

Skeleton live: README, learn outlines (21 framework topics, 14 ERPNext
modules), guides outline, CONTRIBUTING, research history + 66-app catalog.
No lessons yet — outlines only.
