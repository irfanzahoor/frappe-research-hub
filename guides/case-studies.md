# Case Studies — ERPNext in Production

Lessons teach you the pieces. These case studies show what happens
when the pieces meet a real business — the decisions, the mistakes,
and the results. They are anonymised patterns from production
ERPNext work: company types and sizes are real, names are changed,
and every number is approximate — "around" and "roughly" mean exactly
that, not a measured benchmark.

Each case follows the same shape: background, the problem, the
solution, what went wrong, the results, and what you should take
from it. The last two sections of every case are the point: read the
solution for ideas, read the mistakes so you do not repeat them.

---

## Case 1 — A spice manufacturer in Lahore

### Background

A small spice manufacturer — roughly 20–30 people, one factory,
one warehouse — grinding and packing red chilli powder, turmeric and
spice mixes, and selling them to distributors across Punjab. The
business had grown past the point where a spreadsheet and a paper
register could keep up: around 40–60 sales orders a month, 3–4 raw
materials bought in bulk, and every dispatch going out in 1 kg and
5 kg packs.

This is the same kind of business as the
[Practice Project](practice-project.md) factory — same flow, same
documents, at real scale instead of demo scale.

### The problem

Three things hurt every week:

1. **Nobody knew what was actually in stock.** The storekeeper kept
   a paper register; the sales team kept a spreadsheet. The two
   disagreed most days, and the disagreement was only discovered
   when a customer order could not be fulfilled. A distributor would
   order 200 packs, the spreadsheet would say they were in stock,
   and the warehouse would find 140.
2. **Quality was checked after dispatch, not before.** A bad batch
   was found by the customer, not by the factory. One returned
   consignment meant a lost distributor — and distributors talk to
   each other.
3. **Nobody knew the real cost of a pack.** Raw chilli prices move
   with the season. The selling price was set by feel, and nobody
   could say whether a 1 kg pack made a profit in a given month.

### The solution

The core was standard ERPNext, with a small custom app for the one
thing ERPNext does not do out of the box:

- **Manufacturing with BOMs and batch-wise stock.** Each finished
  product got a BOM (raw chilli → ground powder → packed product),
  and every batch of raw material and finished goods was tracked
  batch-wise, so a quality problem could be traced to one batch
  instead of the whole month's production. See
  [Lesson 05 — Manufacturing](../learn/erpnext/operations/05-manufacturing.md)
  and [Lesson 02 — Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md).
- **A Quality Inspection gate before dispatch.** No Delivery Note
  could be submitted until the batch passed inspection — a
  validation in a Server Script that checks the linked Quality
  Inspection and blocks the submit if it is missing or failed.
  The gate is one `validate` hook; the discipline it enforces is
  the whole point. See
  [Lesson 06 — Quality](../learn/erpnext/operations/06-quality.md)
  and [Lesson 05 — Server Scripts](../learn/framework/level-2/05-server-scripts-events.md).
- **Gate Pass for every truck in and out.** Raw material arrivals
  and finished-goods dispatches both passed through the custom
  Gate Pass DocType from
  [Lesson 03](../learn/framework/level-1/03-first-doctype.md), so
  the security guard's register and the stock ledger finally
  agreed with each other.
- **Costing from the BOM, not from feel.** The BOM's valuation rate
  gave the real cost of a pack, and a simple script report compared
  it against the selling price every month — the first time the
  owner could see, per product, which packs made money and which
  did not. See
  [Lesson 08 — Reports & Print Formats](../learn/framework/level-2/08-reports-print-formats.md).
- **Roles kept the factory floor honest.** Storekeepers could
  create Stock Entries but not submit them; only the production
  manager could submit. See
  [Lesson 09 — Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md).

### What went wrong

1. **The quality gate was added too late.** The first version let
   Delivery Notes submit without an inspection, because "we will
   add the gate after go-live". A bad batch went out in that gap —
   the exact failure the gate existed to prevent. The fix was to
   make the gate mandatory from day one and never ship a "we will
   add it later" control. A control that is not enforced on day one
   is not a control.
2. **Batch numbers were typed by hand.** Two storekeepers typed
   batch codes differently (`BATCH-12` vs `batch 12`), so the same
   batch appeared as two batches in reports. The fix was a naming
   series for batches — the system generates the code, humans never
   type it. See the field-layout rules in the
   [Common Mistakes](common-mistakes.md) guide.

### Results

Roughly, in the first three months: stock disagreements between the
register and the system dropped from a weekly argument to a rare
exception; no batch went out without a passed inspection after the
gate was enforced; and the monthly costing report showed that one
spice mix was selling below cost — its price was corrected the same
week. None of this was magic. The stock was right because every
movement went through one system; the quality gate worked because it
blocked the submit instead of asking nicely.

### How we can use it

If you are building for any manufacturer, start with the same three
things: batch-wise stock, a submit-blocking quality gate, and a
costing report. Build the gate first, before go-live, not after.
And never let humans type an identifier the system can generate —
naming series exist for exactly this reason.

---

## Case 2 — A trading and distribution business

### Background

A distributor — around 10–15 people, one warehouse, two delivery
vans — buying packaged goods from manufacturers and supplying them
to shops across a city. Roughly 150–200 deliveries a month, most of
them small, most of them on credit. The business lived or died on
two things: knowing what each shop owed, and knowing where each van
was.

### The problem

1. **Credit was given by memory.** The owner knew which shops paid
   on time and which did not — until he went on leave, and nobody
   else knew. Goods went out to shops that were already months
   behind on payment.
2. **Deliveries were tracked by phone call.** The office called the
   driver, the driver called the shop, the shop said "not yet".
   A delivery that was actually made could sit as "pending" for
   days, and an invoice could not be raised against a pending
   delivery.
3. **Warehouse in/out had no paper trail.** Goods left the warehouse
   without a document, so when stock went missing there was no way
   to say when, or on whose watch.

### The solution

Almost entirely standard ERPNext — this case is mostly about using
the standard flow properly instead of working around it:

- **The standard order-to-cash flow, enforced end to end.**
  Sales Order → Delivery Note → Sales Invoice → Payment Entry,
  with no step skipped. An invoice could only be created from a
  submitted Delivery Note, so "delivered but not invoiced" stopped
  being a category. See
  [Lesson 03 — Selling](../learn/erpnext/core/03-selling.md) and
  [Lesson 01 — Accounting](../learn/erpnext/core/01-accounting.md).
- **Credit limits on every Customer.** Each shop got a credit limit
  based on its payment history, and the system blocked new Sales
  Orders over the limit — the rule no longer lived in one person's
  head. Overdue invoices got a daily email to the owner through a
  scheduled report. See
  [Lesson 11 — Scheduler & Background Jobs](../learn/framework/level-3/11-scheduler-jobs.md).
- **Delivery tracking from the Delivery Note itself.** The driver's
  name and van went on the Delivery Note, and the submitted
  Delivery Note was the proof of delivery — the shop signed the
  print format, and the signed copy came back to the office.
  See [Lesson 08 — Reports & Print Formats](../learn/framework/level-2/08-reports-print-formats.md).
- **Gate Pass for warehouse movements.** Every load leaving the
  warehouse got a Gate Pass linked to its Delivery Notes, so the
  guard's register matched the stock ledger at the end of the day.
  This is the same Gate Pass from
  [Lesson 03](../learn/framework/level-1/03-first-doctype.md),
  reused in a completely different business.
- **A simple dashboard.** Accounts Receivable ageing, today's
  deliveries, and overdue customers on one Insights dashboard the
  owner checked every morning. See
  [Lesson 18 — Insights](../learn/framework/level-4/18-insights.md).

### What went wrong

1. **The credit limit was set too high at first.** The limits were
   copied from the old "gut feeling" numbers, which were generous.
   The system enforced them perfectly — and perfectly enforced a
   bad policy. The fix was to set limits from actual payment
   history (average monthly payment, not the biggest month), and
   to review them every quarter. Automation enforces the rule you
   write, not the rule you meant.
2. **Drivers resisted the signed Delivery Note.** The paper copy
   felt like extra work, and for two weeks vans left without it.
   The fix was not technical: the owner made the signed copy the
   condition for the driver's daily allowance being counted. The
   process stuck after that. A system change that nobody follows
   is not a system change — plan the human part, not just the
   DocType.

### Results

Roughly: overdue receivables fell noticeably within a couple of
months, because new orders to late payers simply stopped being
created; the "delivered but not invoiced" list, which used to run
to dozens of entries, went to near zero — an invoice now follows
the delivery the same day; and end-of-day stock reconciliation,
which used to take the storekeeper an hour of phone calls, became a
five-minute comparison of two lists that already agreed.

### How we can use it

For any trading business, the standard flow is the product — do not
customise before you have used it as designed for a month. Credit
limits belong in the system, not in one person's memory, and they
must come from payment history, not from optimism. And when a new
step meets resistance, fix the incentive, not the form.

---

## Case 3 — A services company

### Background

A small services company — around 8–12 people — doing client
projects: implementation work, support contracts, and the occasional
fixed-price job. The work was tracked in a spreadsheet, the hours
were tracked in a chat group, and the invoices were written from
memory at the end of the month. Roughly 6–8 active projects at any
time, each with a different client, a different rate, and a different
idea of what "done" meant.

### The problem

1. **Nobody knew if a project made money.** Hours were recorded
   late or not at all, so the cost of a project was a guess — and
   the invoice was a bigger guess.
2. **Approvals happened in chat.** A discount, a free extra, a
   change of scope — all agreed in a message, all forgotten by
   invoice time. The client remembered the promise; the company
   could not find it.
3. **Clients could not see anything.** Every status question came
   as a phone call or a message: "where is my project?", "when is
   the next invoice?" The team answered the same questions every
   week.

### The solution

ERPNext Projects, with timesheets doing the heavy lifting:

- **One Project per engagement, with Tasks underneath.** Every
  piece of work was a Task with an owner and a due date, and every
  hour was a Timesheet entry linked to the Task. The project's cost
  became the sum of its Timesheet entries — no more guessing. See
  [Lesson 07 — Projects](../learn/erpnext/operations/07-projects.md).
- **Sales Invoices from Timesheets.** Billable hours were pulled
  straight from approved Timesheets into the invoice, so the
  invoice matched the work actually done. Fixed-price projects
  were invoiced against milestones instead. See
  [Lesson 01 — Accounting](../learn/erpnext/core/01-accounting.md).
- **An approval Workflow for anything that costs money.**
  Discounts, scope changes and free work went through a Workflow
  on the Sales Order — requested by the project lead, approved by
  the owner — so every promise existed as a document, not a chat
  message. See
  [Lesson 10 — Workflows & Assignments](../learn/framework/level-2/10-workflows-assignments.md).
- **A client portal for status and tickets.** Clients logged into
  the portal to see their project's progress and to raise support
  tickets, instead of calling. Tickets went through the Helpdesk,
  so nothing was lost in a chat thread. See
  [Lesson 12 — Support & Portal](../learn/erpnext/people/12-support-portal.md)
  and [Lesson 19 — Website & Portal](../learn/framework/level-4/19-website-portal.md).
- **A weekly project report.** Hours logged, hours billed, and
  project margin per client, emailed to the owner every Monday
  morning by a scheduled job. See
  [Lesson 11 — Scheduler & Background Jobs](../learn/framework/level-3/11-scheduler-jobs.md).

### What went wrong

1. **Timesheets were filled on Friday, from memory.** The team
   logged a week's hours in one sitting, which meant the hours
   were approximate — and "approximate" always rounded up. The fix
   was a daily reminder at 5 pm and a rule: a Timesheet more than
   two days old needs the project lead's approval before it can be
   billed. Hours got accurate when they got daily.
2. **The portal launched before anyone told the clients.**
   The portal was live for a month and almost nobody used it,
   because no client had been told it existed or given a login.
   The fix was a short email to every active client with their
   login and one line — "your project's status is here now" — and
   the phone calls dropped within a week. A feature nobody is told
   about is a feature that does not exist.

### Results

Roughly: the monthly invoice stopped being a negotiation, because
every line on it pointed at an approved Timesheet or a milestone;
one project was found to be running at a loss halfway through, and
its scope was renegotiated instead of discovered at the end; and
the weekly "where is my project?" calls fell away once clients
could see the status themselves. The margin report did the most
work of all — it turned "are we making money?" from a feeling into
a number the owner checked every Monday.

### How we can use it

For any services business, the Timesheet is the source of truth —
everything else (invoice, margin, project status) is derived from
it, so protect its accuracy first. Put every money decision through
a Workflow, because a promise made in chat is a dispute waiting to
happen. And when you build a portal, launching it is the easy half;
telling the clients is the other half.

---

## What the three cases have in common

1. **The standard flow did most of the work.** None of these
   businesses needed a big custom app. The manufacturing case
   needed one gate and one custom DocType; the trading case needed
   almost nothing custom; the services case needed a Workflow and a
   portal. Use the standard flow first, customise second.
2. **Every control that mattered blocked something.** The quality
   gate blocked the submit, the credit limit blocked the order, the
   approval Workflow blocked the discount. A control that only
   warns is a control that gets ignored.
3. **The human part decided whether it worked.** Drivers needed an
   incentive to carry the signed copy; timesheets needed a daily
   reminder; clients needed an email to use the portal. The DocType
   is half the implementation — the other half is the people who
   use it.
4. **The mistakes were all avoidable — and all familiar.** A gate
   added too late, limits copied from gut feeling, hours logged
   from memory, a portal nobody was told about. If you read these
   cases and think "we would never do that", read them again after
   your first go-live.

## Contribute your own case study

These three cases are a start, not a catalogue. If you have shipped
ERPNext in a real business — a factory, a shop, a school, a clinic,
a farm — write it up in this same shape and send it in. Anonymise
the names, keep the numbers approximate and honest, and say what
went wrong: the mistakes are the most useful part. See
[CONTRIBUTING.md](../CONTRIBUTING.md) for how to submit.

## Sources

Anonymised patterns from production ERPNext work at NexTash and from
the hub's own examples — the spice factory in the
[Practice Project](practice-project.md), the Gate Pass from
[Lesson 03](../learn/framework/level-1/03-first-doctype.md), and the
[Food Manufacturing app (fmc)](https://github.com/irfanzahoor/fmc).
Lesson links point at this hub's own lessons. No client names,
company names, quotes or measured metrics appear here: every number
is approximate, by design.
