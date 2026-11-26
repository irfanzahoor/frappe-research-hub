# 04 — Desk, List View, Form View

## What it is

**Desk** is the web UI every Frappe user lives in. It has three parts you
need to understand: the **Workspace** (the home screen), the **List View**
(find records), and the **Form View** (work on one record). Your DocType
automatically gets all three — your job is to make them usable.

## The Desk shell

- **Sidebar** — modules and workspaces. Workspaces group the DocTypes, reports
  and dashboards one role needs. A workspace without a Module set is visible
  to every Desk user — set the module, and restrict finance/HR workspaces by
  role.
- **Search bar (Awesomebar)** — type a DocType, a document name, or a report
  and jump straight to it. This is how experienced users navigate; the sidebar
  is for discovery.
- **Notifications & assignments** — the bell, and the "Assigned To" list on
  forms. Work comes to the user instead of the user hunting for it.
- **The user menu (top right)** — "About" shows the versions the site runs.

## List View — finding and triaging

The List View answers one question: *which records need attention?*

- **Columns** come from fields marked `In List View` (max 4–5 — see
  Lesson 03). They are what a user scans. Pick the fields that identify a
  record: name, date, party, status, amount.
- **Filters** — filter by status, date, company, owner. Save a filter as a
  named view ("My open orders", "Overdue invoices") so the team shares it.
- **Sort** — newest first is the default for transactions; change it when the
  job needs oldest-first (for example, oldest unpaid invoice).
- **Views** — List, Report, Kanban (by status), Calendar, Gantt, Tree. Kanban
  is the right view for a pipeline (leads, support tickets); the plain list
  is right for triage.
- **Bulk actions** — select rows and Assign, print, export or delete in bulk.
- **List Settings** (the gear icon) — pick which columns show, without code.

A good list lets a user find a record in seconds and see its state at a
glance. A bad list is 12 columns wide, unfiltered, and sorted wrong.

## Form View — working on one record

The Form View answers: *what is this record, and what do I do with it?*

- **Sections and tabs** — the layout you defined in the DocType. Sections
  group related fields; tabs split a long form (Details / Items / Terms).
- **Child tables** — rows inside the form (items, taxes). They have their own
  section and their own columns.
- **Status bar** — Draft / Submitted / Cancelled (docstatus), plus the
  workflow state when a Workflow is active.
- **Save / Submit / Cancel / Amend** — Save keeps a Draft editable. Submit
  locks it and posts its effects (stock moves, GL entries). Cancel reverses
  them. Amend creates a new Draft linked to the cancelled one. Never edit a
  submitted document's fields directly.
- **Timeline** — every comment, assignment, attachment and version change, in
  order. This is the audit trail — it is why "just call me" is not a process.
- **Actions menu** — Print, Email, Share, Duplicate, and "New" for a linked
  document (for example, a Sales Invoice from a Sales Order).
- **Customize (in developer mode)** — add a field or change a label from the
  form itself. Handy for a quick fix; ship it as a fixture afterwards.

## Minimal example — a morning's work in Desk

You are the sales user. It is 9 a.m.

1. Open the **Selling** workspace — your quotations and orders are there.
2. Open **Sales Order → List**, filter Status = "To Deliver", sort by
   Delivery Date. The overdue ones are on top.
3. Open the first order. The form shows the customer, items, taxes, and the
   status bar ("To Deliver and Bill").
4. From the actions menu, create the **Delivery Note**. Submit it — stock
   moves out. The timeline records who did it and when.
5. Back in the list, the order now reads "To Bill". Create the **Sales
   Invoice** the same way. Done — the order is "Completed".

No code was written. That whole flow is DocTypes, lists and forms doing
their job.

## When to use which view

| Job | View |
|---|---|
| Find a record | List, with a filter |
| See what is overdue / pending | List, sorted and filtered |
| Work a pipeline (leads, tickets) | Kanban |
| Enter or check one record | Form |
| See everything that happened to a record | Form → Timeline |
| Export for a meeting | List → Report view or Export |

## Common mistakes

- **Treating the list as the place to edit.** The list is for finding. Edit
  on the form — that is where validation, permissions and the timeline live.
- **Too many list columns.** More than 4–5 and nobody can scan the list.
- **No saved filters.** Every user re-builds "my open orders" daily. Save
  the filter once, share it with the role.
- **Hiding a field in JS to "secure" it.** Hiding is not security — anyone
  can read the field through the API. Use permlevel (field-level permission)
  instead.
- **Working from memory instead of the timeline.** If it is not in the
  timeline, it did not happen. Comments and assignments belong on the
  document.
- **One workspace for everyone.** A sales user does not need the payroll
  workspace. Workspaces are per role, not per site.

## Next

You have finished Level 1. You can explain Frappe, run a bench, define a
DocType with a clean layout, and work in Desk. Level 2 starts with
Server Scripts & Document Events — where the logic belongs.
