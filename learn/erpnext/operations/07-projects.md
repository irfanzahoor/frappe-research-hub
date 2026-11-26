# Projects — Tasks, Timesheets, Costing, Profitability

## What it does

Projects turns "do this work for a client" into something measurable: a
**Project** with **Tasks**, time booked on **Timesheets**, costs collected
from timesheets, expenses and purchases — and a profit number at the end.
Without it, a services business knows its revenue and guesses its cost.
With it, every project shows whether it made money or lost it, while there
is still time to fix it.

## Core DocTypes

| DocType | What it is |
|---|---|
| Project | The job: client, dates, expected dates, costing, billing status. |
| Task | One piece of work in a project, with an owner, dates and dependencies. |
| Timesheet | Time booked against a project / task, with billable and costing rates. |
| Timesheet Detail | One time entry: hours, activity type, billable or not. |
| Activity Type | The kind of work (Development, Consulting, Support) with a costing and billing rate. |
| Activity Cost | The cost rate for an Activity Type per employee. |
| Project Template | A reusable task list for a standard job (e.g. "ERPNext go-live"). |
| Project Type | A category (Internal, External, Support) for grouping and reporting. |
| Project Update | A status note on the project, shared with the team. |

## End-to-end flow

```text
Setup:   Activity Types + rates → Project Template for the standard job
Plan:    Project → Tasks (with dependencies) → assign owners
Work:    Timesheet entries against tasks (billable / non-billable)
Cost:    timesheets + Expense Claims + Purchase Invoices roll into the project
Bill:    Timesheet → Sales Invoice (time billed to the client)
Check:   Project Profitability report — revenue vs cost, per project
```

- A Task can depend on another Task — it cannot start until the first is
  done. Dependencies are what make the plan honest.
- A Timesheet entry has two rates: the **costing rate** (what the hour
  costs you) and the **billing rate** (what you charge). Profit is the gap
  between them.
- **Billable** hours go to the client invoice; **non-billable** hours are
  still cost — they just do not earn. Marking everything billable hides
  the real margin.
- The **Project Profitability** report is the one number the owner checks:
  revenue booked minus cost incurred, per project.

## Worked example — an ERPNext implementation, one project

NexTash takes an ERPNext implementation for a Lahore distributor:

1. **Project** "Al-Noor ERPNext Go-Live", type External, from the
   "ERPNext go-live" **Project Template**: setup → data import → training
   → go-live, with dependencies in order.
2. **Tasks** assigned: Irfaan (setup, data import), a colleague (training).
3. Each week the team books **Timesheets**: 30 hrs Development (billable),
   6 hrs internal meetings (non-billable).
4. Travel and a test server land as **Expense Claims** and a **Purchase
   Invoice** against the project.
5. At month end, the **Sales Invoice** bills the 30 hours at the agreed
   rate. The Project Profitability report shows revenue 450,000, cost
   280,000 — the project is on track, and the 6 non-billable hours are
   visible, not hidden.

## A real use case

A services company billed clients from memory at month end — hours were
forgotten, and nobody knew which client was profitable. After Projects +
Timesheets, every invoice came from booked time, and the profitability
report showed one "big" client was actually loss-making once internal
hours were counted. They repriced that client with the report as evidence.

**How we can use it:** run NexTash's own client work in Projects — it is
both our internal tool and the demo. When a client asks "how do you track
our project?", show them the live project: tasks, timesheets, profitability.
That demo sells the module better than any slide.

## Common mistakes

- **Timesheets filled at month end.** Memory is not a time record. Book
  time daily, or the billable hours are a guess.
- **No costing rate.** If only the billing rate is set, the project looks
  profitable until salaries are counted.
- **Everything marked billable.** Internal work billed to a client is a
  dispute waiting to happen — and it hides the real cost.
- **Tasks with no owner and no dates.** A task list without owners is a
  wish list. Every task needs one owner and one due date.
- **Ignoring the profitability report.** The report exists to catch a
  losing project early. Check it weekly, not at the end.

## Next

[08 — Assets](08-assets.md) — asset lifecycle, depreciation, maintenance.
