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
  (59 files: all 21 Framework lessons, 14 ERPNext modules, 6 guides,
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
