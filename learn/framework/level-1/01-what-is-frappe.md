# 01 — What Frappe Is: Framework vs ERPNext vs Frappe Cloud

## What it is

Three different things share the name "Frappe". Mixing them up is the first
mistake most beginners make.

**Frappe Framework — the platform.** A full-stack web framework in Python and
JavaScript, on MariaDB, Redis and Node.js. It gives you, out of the box:

- **DocTypes** — one definition that creates the database table, the form,
  the list view, the API and the permissions.
- **Desk** — the admin UI your users work in every day.
- **REST API, background jobs, scheduler, workflows, reports, print formats,
  email and notifications** — all built in, no extra libraries to wire up.

The Framework is MIT-licensed and open source. Current version: **v16**,
with monthly releases (16.60, 16.61, …). Since v16.60, Studio (no-code app
builder) and Flow (AI in Desk) ship inside the Framework itself.

**ERPNext — the business app built on Frappe.** Accounting, Stock, Selling,
Buying, Manufacturing, HR, CRM, Projects, Assets, Helpdesk. It is *one app*
that runs on a Frappe site, the same way your own custom app does. GPL-3.0
licensed. When someone says "we run ERPNext", they mean a Frappe site with
the ERPNext app installed.

**Frappe Cloud — hosted Frappe.** Your sites run on Frappe's infrastructure.
You deploy custom apps from a Git repo through the dashboard. There is no
shell access, and no Server Scripts on shared benches. You trade control for
zero server work.

Other Frappe apps follow the same pattern: HRMS, CRM, Helpdesk, Insights,
Raven, Builder, Wiki, Drive — each is an app you install on a site.

> One-line mental model: **Framework is the engine, ERPNext is the car built
> on it, Frappe Cloud is renting the car with a driver.**

## How the pieces fit

```text
bench  (a folder on your machine or server)
 ├── apps/      frappe, erpnext, my_app, hrms, ...
 └── sites/     site1.local, client-a.com, ...
                 └── each site = one database + files
```

One bench holds many sites. One site runs many apps. A document (a Sales
Order, an Employee, a custom record) always belongs to one site.

## When to use which

| Goal | Use |
|---|---|
| Learn to build, or build a custom app | Framework on a local bench |
| Run a business end to end | ERPNext (Cloud or self-hosted) |
| Client wants zero server work | Frappe Cloud |
| Need shell access, custom infra, local-only data rules | Self-hosted bench |
| Build a product to sell | Custom app on Framework (plus ERPNext if it extends the ERP) |
| Quick prototype for one client | Framework + Studio (v16.60+) before writing code |

## Minimal example — see it yourself

On a bench that already has ERPNext installed:

```bash
bench --version        # the bench CLI version
bench list-apps        # apps on this bench: frappe, erpnext, ...
bench --site mysite.local list-apps   # apps installed on one site
```

Then open `http://mysite.local:8000` and sign in as Administrator:

- Search **"Company"** in the top search bar — that is an ERPNext DocType.
- Search **"DocType"** — that is the Framework's own list of DocTypes.
- Search **"Sales Invoice"** — ERPNext again. Every screen you see is a
  DocType rendered by the Framework.

## Common mistakes

- **Thinking ERPNext *is* Frappe.** ERPNext is one app. The Framework is the
  platform everything runs on. You can run Frappe with no ERPNext at all.
- **Editing ERPNext's files directly.** Never edit another app's code. Extend
  it from your own app with hooks, overrides and fixtures instead.
- **Self-hosting for a small client who just needs ERPNext.** A server plus
  your maintenance time costs more than Frappe Cloud for most small sites.
- **Choosing Cloud when the client needs shell-level work** — custom system
  packages, local-only data, or direct database access. Cloud has no shell.
- **Starting with code before checking what already exists.** ERPNext, HRMS,
  CRM and the Apps Catalog already solve most requirements. Build only the
  gap.

## Key terms — keep these

- **DocType** — the definition of a record type (table + form + list + rules).
- **Document** — one record (one Sales Order, one Employee).
- **Desk** — the web UI.
- **bench** — the CLI and folder that holds apps and sites.
- **site** — one database + one set of installed apps.
- **app** — a package of DocTypes, code and fixtures (frappe, erpnext, yours).
- **docstatus** — 0 Draft, 1 Submitted, 2 Cancelled. You will meet it in
  every ERPNext lesson.

## Next

[02 — Bench, sites & apps](02-bench-sites-apps.md) — install it and create
your first site and app.
