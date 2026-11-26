# Changelog

All notable changes to the Frappe Research Hub. Dates are in Asia/Karachi.

## Unreleased — Beta v0.2.0 in progress

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
