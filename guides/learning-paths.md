---
description: "Two learning paths through the hub — a Developer Mastery Track to master Frappe by building, and a Functional Guidance Track for non-developers."
---

# Learning Paths — Developer Mastery or Functional Guidance

This hub is a personal mastery path, not a reading list. It is built
for one person working through it, alone, until they can do the work
without the guide. There are two ways through it, depending on who
you are — pick one, and follow it in order. Do not jump around; each
stage assumes the one before it.

## Which track are you?

- **Developer Mastery Track** — you write code, or you want to. You
  will build real things on a real bench, with your hands on the
  keyboard, and prove each stage by doing it without looking at the
  guide. Follow this track if your goal is to *master* Frappe work.
- **Functional Guidance Track** — you do not write code: ERP
  consultant, business user, manager, or the person who decides what
  the system must do. You will read to understand, to evaluate, and
  to guide an implementation — no code required.

You can switch tracks at any time. A developer who finishes the
Mastery Track should still read the Functional Track's case studies;
a functional person who gets curious about how a DocType works can
dip into Level 1. The tracks are routes, not walls.

---

## Track 1 — Developer Mastery: Noob to Pro

**How it works:** read the lessons, then do the checkpoint. A
checkpoint is only done when you can complete it *without opening
the hub* — no guide, no notes, just a blank bench and your memory.
If you cannot, go back and re-read; that is the point. Time
estimates below are a rough guide for someone studying a few
evenings a week.

### Stage 1 — Foundations (about 1 week)

Read, in order:

- [Lesson 01 — What is Frappe](../learn/framework/level-1/01-what-is-frappe.md)
- [Lesson 02 — Bench, Sites & Apps](../learn/framework/level-1/02-bench-sites-apps.md)
- [Lesson 03 — Your First DocType](../learn/framework/level-1/03-first-doctype.md)
- [Lesson 04 — Desk, List & Form](../learn/framework/level-1/04-desk-list-form.md)

**Checkpoint:** on a fresh bench, create a new app and build the
Gate Pass DocType from scratch — fields `naming_series`,
`gate_pass_date`, `visitor_name`, `company`, `purpose`, plus the
Gate Pass Item child table (`item_name`, `qty`, `direction`) — then
create a Gate Pass in Desk and submit it. No guide open.

### Stage 2 — Build (about 2 weeks)

Read, in order:

- [Lesson 05 — Server Scripts & Document Events](../learn/framework/level-2/05-server-scripts-events.md)
- [Lesson 06 — Client Scripts](../learn/framework/level-2/06-client-scripts.md)
- [Lesson 07 — APIs](../learn/framework/level-2/07-apis.md)
- [Lesson 08 — Reports & Print Formats](../learn/framework/level-2/08-reports-print-formats.md)
- [Lesson 09 — Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md)
- [Lesson 10 — Workflows & Assignments](../learn/framework/level-2/10-workflows-assignments.md)

Then the documents you will automate — the ERPNext Core modules:

- [Module 01 — Accounting](../learn/erpnext/core/01-accounting.md)
- [Module 02 — Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md)
- [Module 03 — Selling](../learn/erpnext/core/03-selling.md)
- [Module 04 — Buying](../learn/erpnext/core/04-buying.md)

**Checkpoint:** add server-side validation to your Gate Pass (no
future dates, positive quantities) and a client script that sets the
date and reacts to the direction — written by you, from memory.
Check your work against the demo app afterwards, not before. When
you get stuck, use the [Cheat Sheets](cheat-sheets.md) — they are
for looking things up, not for copying whole solutions.

### Stage 3 — Ship (about 2 weeks)

Read, in order:

- [Lesson 11 — Scheduler & Background Jobs](../learn/framework/level-3/11-scheduler-jobs.md)
- [Lesson 12 — Notifications, Email & Integrations](../learn/framework/level-3/12-notifications-email.md)
- [Lesson 13 — Testing](../learn/framework/level-3/13-testing.md)
- [Lesson 14 — Performance](../learn/framework/level-3/14-performance.md)
- [Lesson 15 — Security](../learn/framework/level-3/15-security.md)
- [Lesson 16 — Debugging](../learn/framework/level-3/16-debugging.md)

**Checkpoint:** add a daily scheduler job to your app that finds
stale draft Gate Passes, and write a Script Report that lists Gate
Passes by day. Then deliberately break something — a bad migration,
a wrong permission — and fix it using only the traceback and
[Lesson 16](../learn/framework/level-3/16-debugging.md). Debugging
is part of the job, not an interruption to it.

### Stage 4 — Operations (about 2 weeks)

The ERPNext modules that run a real business. Read Manufacturing
and Quality *before* the practice project's stock phases — you will
need them there:

- [Module 05 — Manufacturing](../learn/erpnext/operations/05-manufacturing.md)
- [Module 06 — Quality](../learn/erpnext/operations/06-quality.md)
- [Module 07 — Projects](../learn/erpnext/operations/07-projects.md)
- [Module 08 — Assets](../learn/erpnext/operations/08-assets.md)
- [Module 09 — HR](../learn/erpnext/people/09-hr.md)
- [Module 10 — CRM](../learn/erpnext/people/10-crm.md)
- [Module 11 — Helpdesk](../learn/erpnext/people/11-helpdesk.md)
- [Module 12 — Support & Portal](../learn/erpnext/people/12-support-portal.md)

**Checkpoint:** explain the order-to-cash flow (Sales Order →
Delivery Note → Sales Invoice → Payment Entry) and the buy-to-pay
flow (Purchase Order → Purchase Receipt → Purchase Invoice →
Payment Entry) to someone else, without notes, naming the DocType
at each step and what happens to stock and the ledger. If you
cannot explain it, you do not know it yet.

### Stage 5 — Advanced (about 2 weeks)

Read, in order:

- [Module 13 — Studio, Flow & Insights](../learn/erpnext/v16/13-studio-flow-insights.md)
- [Module 14 — Cross-Module Flows](../learn/erpnext/v16/14-cross-module-flows.md)
- [Lesson 17 — Studio & Flow](../learn/framework/level-4/17-studio-flow.md)
- [Lesson 18 — Insights](../learn/framework/level-4/18-insights.md)
- [Lesson 19 — Website & Portal](../learn/framework/level-4/19-website-portal.md)
- [Lesson 20 — Upgrades](../learn/framework/level-4/20-upgrades.md)
- [Lesson 21 — Ops](../learn/framework/level-4/21-ops.md)

**Checkpoint:** back up your site, restore it on a second site,
and upgrade it following the
[Upgrade guide](upgrade-v14-v15-v16.md). A developer who cannot
restore a backup has not finished this stage.

### Stage 6 — Capstone: the practice project (about 1 week)

Build the [Practice Project — a spice factory, end to
end](practice-project.md), all 8 phases, on your own bench. This is
the whole track in one project: Gate Pass, BOM and Work Order,
stock, sales, the Quality Inspection gate, invoicing, payment, the
report and the print format, then permissions, backup and go-live.

The [demo app code](https://github.com/irfanzahoor/frappe-research-hub/tree/main/demo-app)
is a **reference, not a shortcut**: build the Gate Pass yourself
first, then compare your code with the shipped app, line by line.
If your code and the demo app agree, you built it right. If they
differ, find out why — that difference is the lesson.

### Stage 7 — Final check: interview prep

Work through the [Interview Prep guide](interview-prep.md) — 36
questions with model answers, including the spot-the-bug code
questions. If you can answer the code and scenario questions
without hesitating, you are ready to be tested by someone else.

### What "master" means

You are a master when you can sit at a blank bench and build the
Gate Pass app plus the practice-project flow — DocTypes, validation,
client script, workflow, report, print format, permissions, backup
— **without opening the hub**. Not from memory of the words, but
from understanding of how the pieces fit.

That is the bar this track is built around. Everything after it is
keeping sharp: the [Troubleshooting guide](troubleshooting.md) when
something breaks, the [Cheat Sheets](cheat-sheets.md) when you need
a command, the [Case Studies](case-studies.md) for how real
implementations actually went, and the
[Common Mistakes](common-mistakes.md) list before every go-live.

---

## Track 2 — Functional Guidance: Understand ERPNext, Guide an Implementation

**How it works:** read to understand, not to build. No code, no
bench, no commands. Each stage ends with what you should be able
to *decide* or *explain* afterwards.

### Stage 1 — What Frappe and ERPNext are (a few evenings)

- [Lesson 01 — What is Frappe](../learn/framework/level-1/01-what-is-frappe.md) — what the Framework is, what ERPNext is, what Frappe Cloud is
- [Module 01 — Accounting](../learn/erpnext/core/01-accounting.md)
- [Module 02 — Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md)
- [Module 03 — Selling](../learn/erpnext/core/03-selling.md)
- [Module 04 — Buying](../learn/erpnext/core/04-buying.md)

**You should now be able to:** explain to a colleague, in plain
words, what ERPNext does for a business, and which module owns
money, stock, sales and purchasing.

### Stage 2 — The flows that run a business

- [Module 14 — Cross-Module Flows](../learn/erpnext/v16/14-cross-module-flows.md) — order-to-cash, buy-to-pay, forecast → production → sales
- [Module 05 — Manufacturing](../learn/erpnext/operations/05-manufacturing.md)
- [Module 06 — Quality](../learn/erpnext/operations/06-quality.md)
- [Module 07 — Projects](../learn/erpnext/operations/07-projects.md)
- [Module 09 — HR](../learn/erpnext/people/09-hr.md)
- [Module 10 — CRM](../learn/erpnext/people/10-crm.md)

**You should now be able to:** trace a sales order from quotation
to payment and say, at each step, which document is created and
what changes in stock and in the accounts.

### Stage 3 — Choose the right tools

- [Choosing Apps](choosing-apps.md) — when to install an app vs
  build it, and what each app costs you later
- [Apps Catalog](../research/apps-catalog.md) — what exists already,
  so you do not pay to build what is free
- [Go-Live Checklist](go-live-checklist.md) — what a real go-live
  needs: data, permissions, training, cutover

**You should now be able to:** judge whether a requirement needs a
new app, a small customisation, or just a change in process — and
say what it will cost to maintain.

### Stage 4 — Learn from real implementations

- [Case Studies](case-studies.md) — a spice manufacturer, a
  trading/distribution business, a services company: what was built,
  what went wrong, and what to take from each
- [Common Mistakes](common-mistakes.md) — the errors teams make
  most, so you can spot them in your own project before they happen

**You should now be able to:** name three things that commonly go
wrong in an ERPNext implementation, and what you would do
differently.

### Stage 5 — Work with developers

You do not need to write code to work with people who do. Read
these as concepts, not as instructions to run:

- [Lesson 04 — Desk, List & Form](../learn/framework/level-1/04-desk-list-form.md) — how users actually work in the system, so you can describe what you want in their terms
- [Lesson 10 — Workflows & Assignments](../learn/framework/level-2/10-workflows-assignments.md) — how approvals move, so you can design one
- [Lesson 09 — Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md) — who can see and do what, so you can ask for the right access
- [Lesson 13 — Testing](../learn/framework/level-3/13-testing.md) — how to check quality, so you can test a delivery properly

**You should now be able to:** write a requirement a developer can
build without guessing — "when X happens, the system should do Y,
and Z should not be allowed to do it" — and test whether what was
delivered matches it.

### Stage 6 — When things go wrong

- [Troubleshooting](troubleshooting.md) — read it as "what can go
  wrong", not as fixes to run yourself. You need to know which
  problems are small (a stuck email queue) and which are serious
  (a failed migration), so you can judge urgency.
- [Upgrade guide](upgrade-v14-v15-v16.md) — what an upgrade
  involves, so you can plan for it instead of being surprised by it.

### How to use this track in a real implementation

Walk into the implementation with Stage 2 in your head: the flows.
When a developer proposes a solution, ask three questions — which
documents does it create, what changes in stock and in the ledger,
and how will we test it. When a vendor proposes an app, check the
[Choosing Apps](choosing-apps.md) questions and the
[Apps Catalog](../research/apps-catalog.md) first. And before
go-live, run the [Go-Live Checklist](go-live-checklist.md) with the
team — it exists because real go-lives have failed without it.
