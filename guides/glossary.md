---
description: "Frappe and ERPNext glossary — 56 terms explained in plain language, each with a link to the lesson that teaches it."
---

# Glossary — Frappe & ERPNext Words, in Plain Language

Every confusing word in this hub, explained in one or two lines. Terms
stay in English (they are the words you will see on screen); the
definition is the plain meaning. Where a term is taught, the entry
links to the lesson that teaches it.

For both tracks: developers meet these terms in the lessons, functional
people meet them in meetings. If a word is missing, open an issue —
the request template is in the repo.

**Jump to a letter:** [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [L](#l) · [M](#m) · [N](#n) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w)

No terms under K, O, X, Y, Z — yet.

---

## A

**API** — A way for one system to ask another system for data or an
action, using a defined address (URL) and format. In Frappe, a
whitelisted server method becomes an API you can call from a browser,
another app, or `bench execute`. Taught in
[Lesson 07](../learn/framework/level-2/07-apis.md).

**App** — A package of DocTypes, code and reports that adds a feature
set to a bench. ERPNext itself is an app built on Frappe, and your
custom code lives in your own app. Taught in
[Lesson 02](../learn/framework/level-1/02-bench-sites-apps.md).

## B

**Background Job** — A task that runs out of sight, after the user
clicks — for example sending a bulk email or generating a big report —
so the screen does not freeze while it works. Taught in
[Lesson 11](../learn/framework/level-3/11-scheduler-jobs.md).

**Batch** — A group of stock received or made together, tracked as one
lot with its own batch number — so you know which batch a faulty item
came from, and can use the oldest batch first (FEFO). Taught in
[Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md).

**Bench** — The command-line tool (`bench`) that manages a Frappe
installation: it creates sites, installs apps, runs migrations and
starts the server. The folder it creates is also called the bench.
Taught in
[Lesson 02](../learn/framework/level-1/02-bench-sites-apps.md).

**BOM** — Bill of Materials: the recipe for making one item — which raw
materials, in what quantity, go into one finished unit. A Work Order
is made from a BOM. Taught in
[Manufacturing](../learn/erpnext/operations/05-manufacturing.md).

## C

**Child Table** — A table inside a form: a list of rows (like invoice
lines or gate-pass items) that belong to the parent document and are
saved with it. Taught in
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**Client Script** — JavaScript that runs in the user's browser and
changes how a form behaves — showing or hiding a field, filling a
default, or checking a value before save. It cannot be trusted for
security, because it never runs on the server. Taught in
[Lesson 06](../learn/framework/level-2/06-client-scripts.md).

**Controller** — The Python class behind a DocType (in the app's
`doctype/<name>/<name>.py`) where the document's server-side logic
lives: `validate`, `before_save`, `on_submit` and similar methods.
Taught in
[Lesson 05](../learn/framework/level-2/05-server-scripts-events.md).

**Currency** — A field type that stores money, with the currency symbol
and decimals of the company's currency. Taught in
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

## D

**Dashboard** — A page of charts and number cards that shows the state
of the business at a glance — sales this month, open orders, low stock.
Built in Desk, or in Insights. Taught in
[Lesson 04](../learn/framework/level-1/04-desk-list-form.md).

**Data** — A field type for a short line of text, such as a name or a
code. Taught in
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**Date** — A field type for a calendar date, without a time. Taught in
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**Desk** — Frappe's main work screen: the sidebar, workspaces, list
views and forms where users do their daily work. Taught in
[Lesson 04](../learn/framework/level-1/04-desk-list-form.md).

**DocStatus** — The state of a document as a number: 0 = Draft,
1 = Submitted, 2 = Cancelled. Workflows and permissions often depend
on it. Taught in
[Lesson 10](../learn/framework/level-2/10-workflows-assignments.md).

**DocType** — The definition of one kind of document: its fields, its
behaviour, and its permissions. Frappe turns a DocType into a database
table, a form, a list view and an API. Taught in
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

## E

**ERPNext** — The open-source ERP app built on Frappe: accounting,
stock, selling, buying, manufacturing, HR, CRM and more, in one
system. Taught in
[Lesson 01](../learn/framework/level-1/01-what-is-frappe.md).

## F

**Field** — One box of information on a form — a name, a date, a link
to another document. Every field has a type (Data, Link, Currency…)
that decides what it can hold. Taught in
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**Fixture** — Data that an app ships with itself and re-installs on
every migrate — for example a standard Role, a Workflow or a Print
Format that the app needs to work. Listed in
[Cheat Sheets](cheat-sheets.md).

**Frappe Framework** — The open-source, Python-and-JavaScript web
framework that ERPNext is built on: it gives you DocTypes, permissions,
reports, APIs and the Desk interface, so an app is mostly definitions,
not plumbing. Taught in
[Lesson 01](../learn/framework/level-1/01-what-is-frappe.md).

## G

**GL Entry** — General Ledger Entry: one line in the accounts. Every
invoice, payment and stock movement writes GL Entries, and the trial
balance is the sum of them. Taught in
[Accounting](../learn/erpnext/core/01-accounting.md).

## H

**Hook** — A line in an app's `hooks.py` that plugs the app's code into
Frappe — for example "when a Sales Order is submitted, run this
function", or "run this job every day at midnight". Taught in
[Lesson 05](../learn/framework/level-2/05-server-scripts-events.md).

**HTML** — A field type that shows fixed text, instructions or a
formatted note on a form. It stores no data, it only displays. Taught
in [Lesson 03](../learn/framework/level-1/03-first-doctype.md).

## I

**Insights** — Frappe's dashboard tool (v16): build a Workbook from a
query, turn it into charts, and put the charts on a Dashboard — no code
needed. Taught in
[Lesson 18](../learn/framework/level-4/18-insights.md).

## J

**Jinja** — The template language used in Print Formats and
notifications: `{{ doc.customer }}` prints a field's value, and
`{% if %}` / `{% for %}` add conditions and loops. Taught in
[Lesson 08](../learn/framework/level-2/08-reports-print-formats.md).

## L

**Link** — A field type that points at another document, such as a
Customer or an Item. The user picks from a list, and Frappe checks the
linked document exists. Taught in
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**List View** — The table that shows many documents at once — all Sales
Orders, all Items — with filters, sorting and columns you can choose.
Taught in
[Lesson 04](../learn/framework/level-1/04-desk-list-form.md).

## M

**MariaDB** — The database Frappe stores everything in (Postgres is
also supported): every DocType becomes a table, every document a row.
Taught in
[Lesson 01](../learn/framework/level-1/01-what-is-frappe.md).

**Migration** — Running `bench migrate` after code changes: it updates
the database tables to match the DocTypes, runs patches, and reloads
fixtures. Taught in
[Lesson 02](../learn/framework/level-1/02-bench-sites-apps.md).

**Module** — A folder inside an app that groups related DocTypes — for
example, the Selling module holds Sales Order, Delivery Note and
Customer. Taught in
[Lesson 02](../learn/framework/level-1/02-bench-sites-apps.md).

## N

**Naming Series** — The pattern that generates document numbers, like
`SO-2026-0001`: a prefix plus a running number, set per DocType.
Taught in
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**Notification** — An automatic message — email, Desk alert or both —
sent when something happens, such as an order waiting for approval or
a leave request needing a decision. Taught in
[Lesson 12](../learn/framework/level-3/12-notifications-email.md).

## P

**Payment Entry** — The document that records money actually paid or
received — against invoices, or as an advance — and writes the matching
GL Entries. Taught in
[Accounting](../learn/erpnext/core/01-accounting.md).

**Permission** — The rule that decides who can read, write, create,
submit or delete one DocType: set per Role, per DocType, in the Role
Permission Manager. Taught in
[Lesson 09](../learn/framework/level-2/09-permissions-roles.md).

**Print Format** — The layout used when a document is printed or turned
into a PDF — built with Jinja templates on top of the document's
fields. Taught in
[Lesson 08](../learn/framework/level-2/08-reports-print-formats.md).

## Q

**Quality Inspection** — The document that records the result of
checking goods — accepted or rejected, with readings — and can block a
delivery or a receipt until it passes. Taught in
[Quality](../learn/erpnext/operations/06-quality.md).

**Query Report** — A report written as one SQL query (plus a small
Python file for columns and filters): the fastest way to build a
list-style report. Taught in
[Lesson 08](../learn/framework/level-2/08-reports-print-formats.md).

## R

**Redis** — The in-memory store Frappe uses for caching and for the job
queue: background jobs wait in Redis until a worker picks them up.
Taught in
[Lesson 11](../learn/framework/level-3/11-scheduler-jobs.md).

**Role** — A label given to users — Sales User, Stock Manager, System
Manager — that decides which DocTypes they can see and what they can
do with them. Taught in
[Lesson 09](../learn/framework/level-2/09-permissions-roles.md).

## S

**Sales Order** — The customer's confirmed order: what they will buy,
at what price, and when. The starting document of the selling flow.
Taught in
[Selling](../learn/erpnext/core/03-selling.md).

**Scheduler** — Frappe's clock: it wakes up every minute and runs the
jobs that are due — hourly, daily, or on a cron schedule written in
`hooks.py`. Taught in
[Lesson 11](../learn/framework/level-3/11-scheduler-jobs.md).

**Script Report** — A report written in Python: full control over the
query, the columns and the logic, for reports a single SQL query
cannot express. Taught in
[Lesson 08](../learn/framework/level-2/08-reports-print-formats.md).

**Section Break** — A layout field that starts a new section on a form,
with an optional heading — used to group related fields together.
Taught in
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**Server Script** — Python code that runs on the server when a document
event fires (`validate`, `before_save`, `on_submit`…) — where the real
rules live, because the browser cannot be trusted. Taught in
[Lesson 05](../learn/framework/level-2/05-server-scripts-events.md).

**Site** — One Frappe installation's data: a site has its own database,
its own users and its own installed apps. One bench can host many
sites. Taught in
[Lesson 02](../learn/framework/level-1/02-bench-sites-apps.md).

**Stock Entry** — The document that moves stock: receive it, move it
between warehouses, consume it in production, or write it off. Taught
in [Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md).

**Submit** — The action that makes a draft document final: it changes
DocStatus from 0 to 1, runs the `on_submit` code, and posts the ledger
and stock effects. Submitted documents can be cancelled, not edited.
Taught in
[Lesson 05](../learn/framework/level-2/05-server-scripts-events.md).

## T

**Tab Break** — A layout field that starts a new tab on a form — used
to keep long forms tidy by splitting them across tabs. Taught in
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**Table** — A field type that holds a child table: a list of rows inside
the form, each row a document of the child DocType. Taught in
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

## U

**User** — A login account: one person with an email, a password, roles
and permissions. Taught in
[Lesson 09](../learn/framework/level-2/09-permissions-roles.md).

## V

**Validation** — The check that runs before a document is saved
(`validate`): if it fails, Frappe shows an error and refuses to save —
for example "qty must be positive". Taught in
[Lesson 05](../learn/framework/level-2/05-server-scripts-events.md).

## W

**Website** — Frappe's built-in website: public pages, web forms and
customer portal pages, served from the same site as Desk. Taught in
[Lesson 19](../learn/framework/level-4/19-website-portal.md).

**Work Order** — The production order: make this quantity of this item,
from this BOM, by this date. It drives material issue, job cards and
the finished-goods receipt. Taught in
[Manufacturing](../learn/erpnext/operations/05-manufacturing.md).

**Workflow** — A set of states and the transitions between them —
Draft → Pending Approval → Approved — with rules about who can move a
document from one state to the next. Taught in
[Lesson 10](../learn/framework/level-2/10-workflows-assignments.md).

**Workspace** — A Desk home page: a set of shortcuts, charts and links
arranged for one job — Sales, Stock, or a custom workspace for your
team. Taught in
[Lesson 04](../learn/framework/level-1/04-desk-list-form.md).
