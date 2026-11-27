---
description: "Interview prep for Frappe and ERPNext developers — 36 questions with model answers, code spot-the-bug, scenarios and a one-week revision plan."
---

# Interview Prep — Frappe & ERPNext Developer Interviews

The page to open the week before an interview. 36 questions a Frappe /
ERPNext developer is actually asked, each with a short model answer —
long enough to show you understand it, short enough to say out loud.
Every section links to the hub lesson that teaches it, and the
[one-week plan](#one-week-plan-before-the-interview) at the end tells
you what to revise each day.

How to use this guide: read a question, answer it out loud **before**
reading the model answer. If you cannot say it in your own words, go
back to the linked lesson. The code questions are the ones that decide
junior vs mid-level — practise those twice.

---

## 1. Frappe Framework basics

Revise: [Lesson 01](../learn/framework/level-1/01-what-is-frappe.md),
[Lesson 02](../learn/framework/level-1/02-bench-sites-apps.md),
[Lesson 03](../learn/framework/level-1/03-first-doctype.md),
[Lesson 05](../learn/framework/level-2/05-server-scripts-events.md),
[Lesson 09](../learn/framework/level-2/09-permissions-roles.md),
[Lesson 11](../learn/framework/level-3/11-scheduler-jobs.md).

**Q1. What is the Frappe Framework?**

A full-stack, metadata-driven web framework in Python and JavaScript,
backed by MariaDB (or Postgres). You define a DocType and Frappe gives
you the database table, the form, the list view, the permissions and
the REST API for free. ERPNext is an app built on Frappe — the framework
is the platform, ERPNext is the business logic on top of it.

**Q2. What is a DocType?**

One definition that is a database table, a form, a list view, a
permission set and an API endpoint at the same time. A DocType has
fields (Data, Link, Select, Table…), and can be standard (shipped with
an app) or custom (built by you). Child DocTypes are small DocTypes
that only live inside a parent — for example, Sales Order Item lives
inside a Sales Order as a table of lines.

**Q3. Bench, site, app — what is the difference?**

A bench is a folder that holds apps and sites. A site is one database
plus one config — one company, one set of data. An app is a code
package (DocTypes, scripts, reports) that you install on one or more
sites. One bench can host many sites, and one site can run many apps.

**Q4. What are hooks, and where do they live?**

Hooks are the app's `hooks.py` file telling Frappe when to run its
code: `doc_events` (run this function on Sales Order submit),
`scheduler_events` (run this every day at 9am), `fixtures` (ship these
records with the app), `override_doctype_class`. If you want your code
to run at a framework moment, there is almost always a hook for it.

**Q5. Server Script vs Client Script — when do you use which?**

Server Script is Python on the server: it can read and write the
database, call APIs, and enforce rules — it is the only place business
logic is safe. Client Script is JavaScript in the browser: form
behaviour, showing or hiding fields, quick feedback. Anything a user
must not be able to bypass belongs on the server — a Client Script can
always be skipped.

**Q6. In what order do document events run on save and submit?**

On first save: `before_insert`, then `validate`, then `before_save`,
then `after_insert`. On every later save: `validate`, `before_save`,
then `on_update`. On submit: `before_submit`, then `on_submit`. On
cancel: `on_cancel`. The rule to remember: `validate` runs on **every**
save, so put checks that must always hold there — never in
`before_insert` alone, or an edit will bypass them.

**Q7. What is a submittable DocType?**

A DocType with a `docstatus`: 0 = Draft, 1 = Submitted, 2 = Cancelled.
Sales Invoice, Delivery Note and Stock Entry are submittable — once
submitted, the document is locked and has already posted its stock and
ledger effects. The only way back is Cancel, which reverses those
effects. Drafts can be edited freely; submitted documents cannot.

**Q8. How do permissions work in Frappe?**

Permissions are role-based, per DocType, set in Role Permission
Manager: for each role you tick Read, Write, Create, Submit, Cancel
and Delete. Field-level control uses permlevel — a field at permlevel 1
is invisible to roles that only have permlevel 0. User Permissions go
further and restrict *which records* a user sees, for example only
their own warehouse or territory.

**Q9. What is the scheduler, and how do background jobs work?**

The scheduler runs jobs on a timetable defined in `scheduler_events`
in `hooks.py` — `all` (every minute), `hourly`, `daily`, `weekly`,
`monthly`, or a `cron` expression. Heavy work goes to background jobs
with `frappe.enqueue`, so the web request returns immediately and a
worker does the slow part in the `short`, `default` or `long` queue.
`bench enable-scheduler` turns the scheduler on for a site.

**Q10. What is a child table, technically?**

A child DocType with `istable` set — it has no list view and no
standalone records. Its rows are stored in their own table with three
link columns: `parent` (the parent document name), `parenttype` (the
parent DocType) and `parentfield` (which table field holds it). That is
why a child row is always fetched and saved together with its parent.

---

## 2. ERPNext functional

Revise: [Accounting](../learn/erpnext/core/01-accounting.md),
[Stock](../learn/erpnext/core/02-stock-inventory.md),
[Selling](../learn/erpnext/core/03-selling.md),
[Buying](../learn/erpnext/core/04-buying.md),
[Manufacturing](../learn/erpnext/operations/05-manufacturing.md),
[Quality](../learn/erpnext/operations/06-quality.md),
[HR](../learn/erpnext/people/09-hr.md),
[CRM](../learn/erpnext/people/10-crm.md).

**Q11. Walk me through the order-to-cash flow.**

Quotation → Sales Order → Delivery Note → Sales Invoice → Payment
Entry. The Quotation is a price offer. The Sales Order is the
commitment. The Delivery Note moves stock out and books the cost of
goods. The Sales Invoice books the revenue and the receivable. The
Payment Entry closes the receivable against the bank. Each step is a
separate submittable document, so every step is auditable.

**Q12. What happens in the General Ledger when you submit a Sales Invoice?**

Debit the Customer (accounts receivable — the customer owes us),
credit the Income account (sales), and credit the Tax account for any
tax charged. When the Payment Entry is submitted, it debits the Bank
and credits the Customer, closing the receivable. Every ERPNext
transaction is a balanced double entry — that is what makes the
reports trustworthy.

**Q13. Walk me through the buying / stock flow.**

Purchase Requisition → Purchase Order → Purchase Receipt → Purchase
Invoice → Payment Entry. The Purchase Receipt is the key step: it
increases stock and posts Debit Stock, Credit "Stock Received But Not
Billed". The Purchase Invoice then clears that account — Debit "Stock
Received But Not Billed", Credit Supplier. That three-way match (order
vs receipt vs invoice) is how you catch over-billing.

**Q14. Walk me through the manufacturing flow.**

BOM → Work Order → Stock Entry → Quality Inspection → Delivery. The
BOM lists the raw materials and operations for one finished item. The
Work Order plans the quantity. A Stock Entry of type "Material Transfer
for Manufacture" moves raw material to the work-in-progress warehouse,
and a Stock Entry of type "Manufacture" consumes it and produces the
finished item. Quality Inspection gates dispatch — nothing ships
before it passes.

**Q15. What is a BOM, and what does it contain?**

A Bill of Materials is the recipe for one finished item: the raw
materials (with quantities and rates), the operations (with workstations
and times), and the resulting cost. A BOM can be single-level (all raw
materials listed directly) or multi-level (a raw material is itself
made from another BOM). Change the BOM and every future Work Order
uses the new recipe — old orders keep the BOM they were created with.

**Q16. Batch vs Serial No — when do you use which?**

Batch when many identical units are tracked as one group: same
manufacturing date, same expiry, same quality result — medicines,
spices, food. Serial when every single unit is unique and must be
tracked on its own — machines, phones, vehicles. Batches use FEFO
(first-expiry-first-out); serials are picked one by one.

**Q17. What does the HR flow look like in ERPNext v16?**

Employee → Leave (Leave Allocation, then Leave Application) →
Attendance → Salary Structure → Payroll Entry. Leave, attendance,
shifts and payroll live in the Frappe HR app, which is installed
alongside ERPNext in v16. The rule that matters: payroll only runs on
approved attendance and approved leave — unapproved records never
reach a salary slip.

**Q18. What does the CRM flow look like, and what changed in v16?**

Lead → Opportunity / Deal → Quotation → Customer. In v16 the CRM lives
in the Frappe CRM app (leads, deals, web forms, communication), not
inside ERPNext itself. The legacy ERPNext CRM is still there but is
scheduled for removal in v17 — so new work should be built in Frappe
CRM, and old data should be migrated before the upgrade.

---

## 3. Code & debugging

Revise: [Lesson 05](../learn/framework/level-2/05-server-scripts-events.md),
[Lesson 06](../learn/framework/level-2/06-client-scripts.md),
[Lesson 07](../learn/framework/level-2/07-apis.md),
[Lesson 14](../learn/framework/level-3/14-performance.md),
[Lesson 15](../learn/framework/level-3/15-security.md),
[Lesson 16](../learn/framework/level-3/16-debugging.md),
[Cheat Sheets](cheat-sheets.md).

**Q19. Spot the bug in this code:**

```python
customer = frm.doc.customer  # JS side — ignore this line, the bug is below
frappe.db.sql(f"select name from `tabSales Order` where customer='{customer}'")
```

It builds SQL with an f-string, so a customer name containing a quote
breaks the query — and a malicious value can run any SQL. That is an
SQL injection hole. Fix it with a parameterised query:

```python
frappe.db.sql(
    "select name from `tabSales Order` where customer=%s", (customer,))
```

**Q20. Spot the bug in this Client Script:**

```javascript
frappe.ui.form.on("Employee", {
    refresh: function(frm) {
        frm.set_df_property("salary", "hidden", 1);  // hide salary from everyone
    }
});
```

Hiding a field in JavaScript is not security — anyone can read the
field through the API or the browser console. The fix is a permlevel:
put `salary` at permlevel 1 and give that level only to the HR Manager
role. Client Scripts are for user experience, never for access control.

**Q21. A check in `before_insert` is being bypassed on edits. Why?**

`before_insert` runs once, on the first save only. An edit to an
existing document never runs it. Move the check to `validate`, which
runs on every save — before insert and before update. If the rule must
hold for the life of the document, `validate` is the only correct
event for it.

**Q22. Spot the bug in this code:**

```python
rate = frappe.db.get_value("Item Price", {"item_code": item}, "price_list_rate")
total = rate * qty
```

`get_value` returns `None` when no matching record exists, so `None *
qty` throws a `TypeError`. Guard it: `rate = frappe.db.get_value(...)
or 0`, or raise a clear `frappe.throw` ("No price found for this
item") so the user knows what is missing instead of seeing a traceback.

**Q23. What does this code do, and why would you write it?**

```python
frappe.enqueue("my_app.tasks.send_daily_report", queue="long")
```

It puts `send_daily_report` on a background queue instead of running it
inside the web request. The user gets a response immediately and a
worker runs the slow job later — `long` is the queue for jobs that take
minutes. You write it whenever a request would otherwise wait on
email, a big report, or an external API.

**Q24. What is wrong with using `cur_frm` in a Client Script?**

`cur_frm` is an old global that points at whatever form happens to be
open — in a list, a dialog, or a second tab it can be the wrong form.
The function already receives the correct form as `frm`. Always use
the `frm` parameter; `cur_frm` is legacy and should not appear in new
code.

**Q25. What is the difference between `doc.save()` and `doc.submit()`?**

`save()` writes the document as a Draft (docstatus 0) — editable,
no stock or ledger effect. `submit()` moves it to Submitted
(docstatus 1), runs `before_submit` and `on_submit`, and posts the
document's real effects: stock movements, GL entries, status changes.
A submitted document cannot be edited — only cancelled, which reverses
those effects.

**Q26. Spot the performance bug in this code:**

```python
for row in sales_order.items:
    item = frappe.get_doc("Item", row.item_code)   # one query per line
    row.description = item.description
```

One database query per line — an order with 200 lines makes 200
queries. That is the N+1 problem. Fix it with a single query up front:

```python
items = {d.name: d.description for d in frappe.get_all(
    "Item", filters={"name": ["in", [r.item_code for r in sales_order.items]]},
    fields=["name", "description"])}
for row in sales_order.items:
    row.description = items.get(row.item_code)
```

One query, then a dictionary lookup per line.

---

## 4. Scenario questions

Revise: [Lesson 08](../learn/framework/level-2/08-reports-print-formats.md),
[Lesson 10](../learn/framework/level-2/10-workflows-assignments.md),
[Lesson 12](../learn/framework/level-3/12-notifications-email.md),
[Practice Project](practice-project.md),
[Case Studies](case-studies.md).

**Q27. A client wants discounts above 10% to need a manager's approval. How do you build it?**

With a Workflow on Sales Order: states Draft → Pending Approval →
Approved, and a transition to Approved that only the Sales Manager
role can use. Then add a server-side `validate` as a backstop — if the
discount is above 10% and the document is not in the Approved state,
`frappe.throw`. The workflow gives the user a visible process; the
server check makes sure the API cannot skip it.

**Q28. A client wants a gate-pass register for everything leaving the warehouse. How do you build it?**

A custom DocType "Gate Pass" (naming series, date, visitor name,
company, purpose) with a child table "Gate Pass Item" (item, qty,
direction in/out), linked to Delivery Note where it applies. Add an
approval Workflow for the security desk, and a Script Report that
shows open gate passes — anything issued but not returned. That is
exactly the register built in the practice project and Lesson 03.

**Q29. A client wants a report that standard reports cannot do. What do you build?**

A Script Report when Python logic is needed — grouping, calculations
across DocTypes, or custom columns — and a Query Report when one SQL
query is enough. Start by checking whether a standard report plus a
filter already answers the question; only then write a Script Report,
with the filters the user actually needs, and link it from the module
it belongs to.

**Q30. A client has 5,000 products in Excel and wants them in ERPNext. How do you migrate them?**

Use the Data Import tool: export the template, fill it, import a
small batch first (50 rows) on a staging site, fix the errors the
Data Import Log reports, then import the rest. Validate mandatory
fields (item code, item group, stock UOM) and duplicates before the
real import, and never import directly into production without a
backup. For messy data, a small import script with
`frappe.get_doc(...).insert()` gives more control than the tool.

**Q31. A report takes two minutes to open. How do you find the problem?**

First reproduce it and read the slow-query log — is it one slow query
or many small ones? Many small ones in a loop is the N+1 problem:
fetch once, look up in memory. One slow query usually needs an index
on the filtered column, or a smaller date range. Also check whether the
report fetches rows it never shows. Fix the query, re-measure, and
only then consider caching or a bigger server.

**Q32. A production bug is reported at 5pm. What do you do?**

Do not hot-fix on live. Reproduce it on staging first, read the Error
Log and the last lines of the traceback, and find the smallest change
that fixes it. Test the fix on staging, back up production, deploy
through the normal path (`bench update` / `bench migrate`), verify on
live, and tell the users what happened. If data is wrong, fix the
code first — then decide, with the client, how the bad data gets
corrected.

---

## 5. HR / behavioural

**Q33. "Tell me about a project you worked on."**

Answer with the shape, not the feature list: the problem, what you
built, what went wrong, and the result. For example: "A spice
manufacturer was tracking dispatches on paper, so we built a gate-pass
register and a quality gate in ERPNext — the first version let a bad
batch ship because the gate was added too late, so we made the
inspection blocking before dispatch. Dispatch errors dropped and the
owner could finally see what had left the warehouse." One real story
beats five feature names.

**Q34. "How do you learn a new ERPNext module?"**

"I open the module on a test site and use it as a user first — create
the documents, submit them, and read the ledger and stock entries
they post. Then I read the DocTypes to see the fields and links, and
only then I write any customisation. If something is unclear, the
source code is the documentation."

**Q35. "A user says 'the system is wrong'. What do you do?"**

Reproduce it with their data before touching code. Most of the time
the system is right and the data is wrong — a wrong rate, a missing
stock entry, a cancelled document. Show them the ledger or the stock
ledger entry that proves what happened, explain it in their words,
and fix the data with them. If the code really is wrong, say so
plainly and fix it.

**Q36. "Why Frappe / ERPNext instead of another ERP?"**

Open source, one stack (Python + MariaDB + JavaScript), and
metadata-driven — a DocType gives you the form, the list, the
permissions and the API without boilerplate, so customisation is fast
and stays upgradeable. The honest trade-off: you need Python
developers, and upgrades need care because custom code can break.
It fits businesses that want their own workflows; it is not the right
choice for a company that wants zero customisation.

---

## One-week plan before the interview

Revise one block a day, and answer that block's questions out loud
before moving on. Day 7 is for the code questions and a mock run.

| Day | Revise | Then answer |
|---|---|---|
| 1 | [Lessons 01–04](../learn/framework/level-1/01-what-is-frappe.md) — what Frappe is, bench, DocTypes, Desk | Section 1, Q1–Q3, Q10 |
| 2 | [Lessons 05–07](../learn/framework/level-2/05-server-scripts-events.md) — server scripts, client scripts, APIs | Section 1, Q4–Q6; Section 3, Q19–Q25 |
| 3 | [Lessons 08–10](../learn/framework/level-2/08-reports-print-formats.md) — reports, permissions, workflows | Section 1, Q7–Q8; Section 4, Q27–Q29 |
| 4 | [ERPNext core](../learn/erpnext/core/01-accounting.md) — Accounting, Stock, Selling, Buying | Section 2, Q11–Q13, Q16 |
| 5 | [ERPNext operations & people](../learn/erpnext/operations/05-manufacturing.md) — Manufacturing, Quality, Projects, HR, CRM | Section 2, Q14–Q15, Q17–Q18; Section 4, Q30–Q32 |
| 6 | [Level 3](../learn/framework/level-3/11-scheduler-jobs.md) — scheduler, testing, performance, security, debugging + [Troubleshooting](troubleshooting.md) | Section 1, Q9; Section 3, Q26; Section 4, Q31–Q32 |
| 7 | [Practice Project](practice-project.md) — build the spice factory flow once, end to end | All of Section 3 + Section 5 out loud, as a mock interview |

---

## Where to go next

- [Cheat Sheets](cheat-sheets.md) — the commands, hooks and API calls from these answers, on one page
- [Troubleshooting](troubleshooting.md) — the 22 errors you will meet while preparing
- [Practice Project](practice-project.md) — build the whole flow once, so you can talk about it in Q33
- [Case Studies](case-studies.md) — real production stories to quote in scenario answers
