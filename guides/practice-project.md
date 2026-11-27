---
description: "Build a spice factory end to end in Frappe and ERPNext — Gate Pass, stock, sales, quality gate, invoicing — in 8 guided phases."
---

# Practice Project — Build a Spice Factory, End to End

Reading lessons teaches you the pieces. This project teaches you how
they fit together. You will build a working ERP for a small spice
manufacturer — **Lal Mirch Foods** — from an empty bench to a live
order-to-cash flow, in your own app, on your own site.

The factory buys raw chillies, grinds and packs them into 1 kg packs of
Red Chilli Powder, sells them to distributors, checks quality before
dispatch, invoices, and collects payment. Every step uses a real
ERPNext document — the same ones the lessons teach — plus one custom
DocType of your own (the Gate Pass from Lesson 03).

**Time:** about 3–4 evenings, roughly an hour a phase. **Result:** a
site you can demo to a client, and the confidence that you can build
the next one from scratch.

## Get the code

The working code is in this repo at [`demo-app/`](https://github.com/irfanzahoor/frappe-research-hub/tree/main/demo-app):
the `lal_mirch_foods` app with the Gate Pass DocType, its controller,
the client script, and the hooks. It is a reference, not a shortcut:
build the Gate Pass yourself first (Phase 2), then install the app and
compare what you built with the shipped code, line by line. The goal
is to reach the point where you can build it without the guide.
Install it with:

```bash
cd ~/frappe-bench
cp -r /path/to/frappe-research-hub/demo-app/lal_mirch_foods apps/
bench --site spice.local install-app lal_mirch_foods
bench --site spice.local migrate
```

The rest of the project (BOMs, Work Orders, reports) stays as guide
steps: type those yourself, that is where the learning is.

## Before you start

**You need:** a working bench with ERPNext v16 (see
[Lesson 02 — Bench, Sites & Apps](../learn/framework/level-1/02-bench-sites-apps.md)).
Read [Lesson 03 — Your First DocType](../learn/framework/level-1/03-first-doctype.md)
before Phase 2 — the Gate Pass there is the one you will build on.

**The demo data** — use exactly these names everywhere, so every phase
lines up:

| Master | Values |
|---|---|
| Company | Lal Mirch Foods |
| Items | `RAW-CHILLI` — Raw Chilli (Whole), Kg, valuation rate 400 |
| | `RCP-1KG` — Red Chilli Powder 1 Kg Pack, Nos, standard rate 650 |
| Warehouses | Stores, Work In Progress, Finished Goods |
| Customer | Karachi Spice Traders |
| Price List | Standard Selling (the default) |

**The flow you are building:**

```text
Gate Pass → BOM → Work Order → Stock Entry (Manufacture)
    → Sales Order → Delivery Note → Quality Inspection
    → Sales Invoice → Payment Entry → Report + Print Format
```

Each phase ends with a **checkpoint** — something you must be able to
do before moving on. Do not skip checkpoints; Phase 4 silently breaks
if Phase 3's stock is wrong.

---

## Phase 1 — Bench, site, app and masters

**Uses:** [Lesson 02 — Bench, Sites & Apps](../learn/framework/level-1/02-bench-sites-apps.md)

### Steps

1. Create the app and the site:

   ```bash
   cd ~/frappe-bench
   bench new-app spice_factory
   bench new-site spice.local --install-app erpnext
   bench --site spice.local install-app spice_factory
   ```

2. Turn on developer mode for this site, so DocTypes you create in
   Desk are saved into your app:

   ```bash
   bench --site spice.local set-config developer_mode 1
   bench --site spice.local migrate
   bench start
   ```

3. In Desk, create the masters from the table above:
   **Company** (Lal Mirch Foods), **Item** `RAW-CHILLI` (Item Group
   Raw Material, UOM Kg) and `RCP-1KG` (Item Group Products, UOM Nos,
   Standard Selling Rate 650), **Warehouses** (Stores, Work In
   Progress, Finished Goods), **Customer** (Karachi Spice Traders).

4. Put 200 kg of `RAW-CHILLI` into Stores with a **Stock Entry**,
   purpose **Material Receipt**, `t_warehouse` Stores, valuation
   rate 400. Submit it. This is your opening stock — without it,
   Phase 3 has nothing to consume.

### Checkpoint

You should now be able to open `spice.local` in the browser, see your
app installed, and find 200 kg of `RAW-CHILLI` in Stores in the Stock
Balance report.

### Common mistakes

- **Skipping `migrate` after installing the app.** The app is listed
  but its tables do not exist until you migrate.
- **Creating the masters on the wrong site.** Check the site name in
  the URL bar — `spice.local`, not your other dev site.
- **Forgetting developer mode.** Without it, the Gate Pass in Phase 2
  is saved to the database only, not into your app, and you cannot
  ship it.

---

## Phase 2 — Gate Pass register

**Uses:** [Lesson 03 — Your First DocType](../learn/framework/level-1/03-first-doctype.md),
[Lesson 04 — Desk, List View, Form View](../learn/framework/level-1/04-desk-list-form.md),
[Lesson 06 — Client Scripts](../learn/framework/level-2/06-client-scripts.md)

### Steps

1. Build the **Gate Pass** DocType exactly as in Lesson 03 — same
   fields, same order:

   | Fieldname | Label | Type | Notes |
   |---|---|---|---|
   | `naming_series` | Series | Select | Options: `GP-.YYYY.-.####` |
   | `gate_pass_date` | Date | Date | Default: Today |
   | `visitor_name` | Visitor | Data | Required |
   | `company` | Company | Link | Options: Company |
   | `purpose` | Purpose | Select | Visit / Delivery / Pickup |
   | `items` | Items | Table | Options: Gate Pass Item |
   | `remarks` | Remarks | Small Text | |

   Child table **Gate Pass Item**: `item_name` (Data, In List View),
   `qty` (Int, In List View), `direction` (Select: In / Out).
   Set Autoname to `naming_series`.

2. Add one Client Script — the date fills itself in, and a Delivery
   or Pickup pass without items is refused:

   ```js
   // spice_factory/spice_factory/doctype/gate_pass/gate_pass.js
   frappe.ui.form.on("Gate Pass", {
       refresh(frm) {
           // New passes always start with today — the guard should not type it.
           if (frm.is_new()) {
               frm.set_value("gate_pass_date", frappe.datetime.nowdate());
           }
       },
       validate(frm) {
           if (
               (frm.doc.purpose === "Delivery" || frm.doc.purpose === "Pickup") &&
               !frm.doc.items.length
           ) {
               frappe.throw(__("Add at least one item for a Delivery or Pickup pass."));
           }
       },
   });
   ```

   Run `bench --site spice.local migrate` and reload Desk.

3. Create two passes: a **Delivery** (a supplier brings 50 kg
   `RAW-CHILLI`, direction In) and a **Visit** (a buyer, no items).
   Submit both.

### Checkpoint

You should now be able to create a Gate Pass in under a minute, see it
in the list as `GP-2026-0001`, and get a clear error if you try to save
a Delivery pass with no items.

### Common mistakes

- **Putting the Client Script in the wrong file.** Form behaviour lives
  in `gate_pass.js` in the DocType folder — not in a Server Script,
  not in hooks.py.
- **Forgetting `migrate` after adding the script.** The `.js` file is
  only picked up when the DocType is reloaded from the app.
- **Validating in `refresh` instead of `validate`.** `refresh` runs
  every time the form opens; a check there fires when the user is only
  looking.

---

## Phase 3 — Make it: BOM, Work Order, Stock Entry

**Uses:** [Manufacturing](../learn/erpnext/operations/05-manufacturing.md),
[Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md)

### Steps

1. Create a **BOM** for `RCP-1KG`, quantity 1:

   | Item | Qty | UOM |
   |---|---|---|
   | `RAW-CHILLI` | 1.05 | Kg |

   (1 kg of powder needs 1.05 kg of raw chilli — grinding loses
   about 5%. Submit the BOM.)

2. Create a **Work Order**: `production_item` `RCP-1KG`, qty **100**,
   `bom_no` (fetched from the BOM), `fg_warehouse` Finished Goods,
   `wip_warehouse` Work In Progress. Submit it. The Work Order now
   reserves the plan: 105 kg of raw chilli in, 100 packs out.

3. Post the production with a **Stock Entry**, purpose
   **Manufacture**, against the Work Order:

   | Row | Item | Qty | Source | Target |
   |---|---|---|---|---|
   | 1 | `RAW-CHILLI` | 105 | Stores | — |
   | 2 | `RCP-1KG` | 100 | — | Finished Goods |

   Submit it. Stock Balance should now show 95 kg `RAW-CHILLI` in
   Stores and 100 packs of `RCP-1KG` in Finished Goods.

### Checkpoint

You should now be able to explain, from the Stock Ledger, where every
kilo went: 200 in, 105 consumed, 100 packs produced. If the numbers do
not match, do not continue — Phase 4 sells stock that Phase 3 made.

### Common mistakes

- **Posting the Stock Entry before submitting the Work Order.** The
  Manufacture entry needs a submitted Work Order to link to.
- **Wrong purpose.** A Manufacture entry with purpose Material Receipt
  moves stock but never consumes the raw material — the ledger will
  not balance.
- **Editing a submitted Work Order to change the qty.** Cancel and
  amend it instead — it has already reserved and moved stock.

---

## Phase 4 — Sell it: Sales Order → Delivery Note → Sales Invoice

**Uses:** [Selling](../learn/erpnext/core/03-selling.md),
[Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md),
[Accounting](../learn/erpnext/core/01-accounting.md),
[Lesson 05 — Server Scripts & Document Events](../learn/framework/level-2/05-server-scripts-events.md)

### Steps

1. Create a **Sales Order** for Karachi Spice Traders: item `RCP-1KG`,
   qty **50**, rate 650, `delivery_date` next week, warehouse
   Finished Goods. Submit it. (Order-to-cash is always
   Quotation → Sales Order → Delivery Note → Sales Invoice →
   Payment Entry.)

2. From the Sales Order, **Create → Delivery Note**. Check the item
   row: it carries `against_sales_order` back to the order, and the
   warehouse is Finished Goods. Submit it — stock drops to 50 packs.

3. From the Delivery Note, **Create → Sales Invoice**. Check the
   totals (50 × 650 = 32,500), then submit it.

4. Add one guard so this can never be oversold. A `validate` hook
   would block even drafts, so hook `on_submit` instead:

   ```python
   # spice_factory/hooks.py
   doc_events = {
       "Sales Order": {
           "on_submit": "spice_factory.api.check_stock_before_submit",
       },
   }
   ```

   ```python
   # spice_factory/api.py
   import frappe
   from frappe import _


   def check_stock_before_submit(doc, method):
       """Block submitting a Sales Order we cannot fulfil from stock."""
       for row in doc.items:
           if not row.warehouse:
               continue
           available = frappe.db.get_value(
               "Bin",
               {"item_code": row.item_code, "warehouse": row.warehouse},
               "actual_qty",
           ) or 0
           if row.qty > available:
               frappe.throw(
                   _("Not enough stock for {0} in {1}: need {2}, have {3}").format(
                       row.item_code, row.warehouse, row.qty, available
                   )
               )
   ```

   Run `bench --site spice.local migrate` and test it: a second Sales
   Order for 60 packs (only 50 left) must refuse to submit; one for
   40 packs must go through.

### Checkpoint

You should now be able to trace one sale end to end: Sales Order
`SO-0001` → Delivery Note → Sales Invoice `SINV-0001`, and show that
the invoice's `outstanding_amount` is 32,500 until it is paid.

### Common mistakes

- **Invoicing before delivering.** The invoice is the money document;
   the Delivery Note is the stock document. Skip the Delivery Note and
   stock never moves.
- **Hooking `validate` for a submit-only rule.** `validate` runs on
   every save, so drafts get blocked too. `on_submit` is the right
   event for "refuse to commit".
- **Checking stock with `frappe.db.sql`.** Use `frappe.db.get_value`
   on Bin — raw SQL bypasses nothing here, but it is a habit that
   breaks permissions elsewhere. (See Lesson 08.)

---

## Phase 5 — Quality gate before dispatch

**Uses:** [Quality](../learn/erpnext/operations/06-quality.md)

### Steps

1. Create a **Quality Inspection Template** for `RCP-1KG` with two
   parameters:

   | Parameter | Type | Acceptance |
   |---|---|---|
   | Moisture % | Numeric | Minimum 0, Maximum 10 |
   | Colour | Value-based | Accepted value: Red |

2. On the `RCP-1KG` **Item**, tick **Inspection Required before
   Delivery** and set the Quality Inspection Template. From now on,
   ERPNext itself enforces the gate: a Delivery Note for this item
   cannot be submitted until a passing inspection exists — and a
   rejected inspection blocks it outright.

3. Make a second Delivery Note (from the 40-pack Sales Order in Phase
   4). In the item row, click the **Quality Inspection** field and
   create one: `inspection_type` **Outgoing**, `reference_type`
   Delivery Note, `sample_size` 5. Enter readings — Moisture 8%,
   Colour Red — and submit it. `status` becomes **Accepted**.

4. Submit the Delivery Note. It goes through, because the gate passed.

### Checkpoint

You should now be able to show a Delivery Note that was blocked until
its inspection passed, and explain why: the inspection is a
precondition of the transaction, not a parallel activity.

### Common mistakes

- **Creating the inspection with the wrong type.** Outgoing is for
  dispatch; Incoming is for purchases; In Process is for Job Cards.
  The wrong type passes the wrong gate.
- **Setting the template but not ticking the Item checkbox.** The
  template alone does nothing — the Item's inspection flag is what
  turns the gate on.
- **Inspecting after dispatch.** If the goods have left, the
  inspection is paperwork. The check belongs before the Delivery Note
  submits.

---

## Phase 6 — Get paid, and approve the gate pass

**Uses:** [Accounting](../learn/erpnext/core/01-accounting.md),
[Lesson 10 — Workflows & Assignments](../learn/framework/level-2/10-workflows-assignments.md)

### Steps

1. Open Sales Invoice `SINV-0001` and **Create → Payment Entry**.
   Check the fields: `payment_type` **Receive**, `party_type`
   **Customer**, `party` Karachi Spice Traders, `paid_amount`
   32,500. Click **Get Outstanding Invoices**, allocate the full
   amount against `SINV-0001` (the `references` table:
   `reference_doctype` Sales Invoice, `reference_name` the invoice,
   `allocated_amount` 32,500), and submit. The invoice's
   `outstanding_amount` is now 0 and its `status` is Paid.

2. Now give the Gate Pass an approval. Create a **Workflow**,
   Document Type **Gate Pass**, Is Active ticked:

   | State | Docstatus |
   |---|---|
   | Draft | 0 |
   | Pending Approval | 0 |
   | Approved | 1 |
   | Rejected | 0 |

   Transitions: Draft → Pending Approval ("Send for Approval",
   allowed role Gatekeeper), Pending Approval → Approved ("Approve",
   allowed role Manufacturing Manager), Pending Approval → Rejected
   ("Reject", allowed role Manufacturing Manager).

3. Create a Gate Pass as Gatekeeper and send it for approval. Log in
   as a Manufacturing Manager user and approve it. Notice the Submit
   button is gone — the workflow now drives the document.

### Checkpoint

You should now be able to show a Paid invoice with a zero outstanding
amount, and a Gate Pass that no one person can create and approve
alone.

### Common mistakes

- **Allocating the payment without clicking Get Outstanding
  Invoices.** The `references` table stays empty, the money lands as
  an unallocated advance, and the invoice stays Unpaid.
- **Giving the approver role to everyone.** A workflow where the
  creator can approve their own pass is decoration, not control.
- **Leaving the Workflow inactive.** An inactive Workflow changes
  nothing — the old Submit button stays, and the approval never
  happens.

---

## Phase 7 — See it: Order-to-Cash report + invoice print format

**Uses:** [Lesson 08 — Reports & Print Formats](../learn/framework/level-2/08-reports-print-formats.md)

### Steps

1. Create a **Script Report** "Order to Cash" (Report Type: Script
   Report, Reference DocType: Sales Invoice, Module: your app) with
   this code:

   ```python
   # spice_factory/spice_factory/report/order_to_cash/order_to_cash.py
   import frappe
   from frappe import _


   def execute(filters=None):
       filters = frappe._dict(filters or {})
       return get_columns(), get_data(filters)


   def get_columns():
       return [
           {"label": _("Invoice"), "fieldname": "name", "fieldtype": "Link", "options": "Sales Invoice", "width": 130},
           {"label": _("Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
           {"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 180},
           {"label": _("Grand Total"), "fieldname": "grand_total", "fieldtype": "Currency", "width": 120},
           {"label": _("Outstanding"), "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 120},
           {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
       ]


   def get_data(filters):
       query_filters = {"docstatus": 1}
       if filters.get("customer"):
           query_filters["customer"] = filters.customer
       if filters.get("from_date") and filters.get("to_date"):
           query_filters["posting_date"] = ("between", [filters.from_date, filters.to_date])
       return frappe.get_list(
           "Sales Invoice",
           filters=query_filters,
           fields=["name", "posting_date", "customer", "grand_total", "outstanding_amount", "status"],
           order_by="posting_date desc",
       )
   ```

   ```js
   // spice_factory/spice_factory/report/order_to_cash/order_to_cash.js
   frappe.query_reports["Order to Cash"] = {
       filters: [
           { fieldname: "from_date", label: __("From Date"), fieldtype: "Date", default: frappe.datetime.month_start() },
           { fieldname: "to_date", label: __("To Date"), fieldtype: "Date", default: frappe.datetime.month_end() },
           { fieldname: "customer", label: __("Customer"), fieldtype: "Link", options: "Customer" },
       ],
   };
   ```

   Run it: `SINV-0001` shows Grand Total 32,500, Outstanding 0,
   Status Paid.

2. Create a **Print Format** for Sales Invoice (Print Format Type:
   Jinja) with your factory's header and an items table:

   ```jinja
   <div style="text-align: center;">
     <h2>{{ doc.company }}</h2>
     <p>Tax Invoice — {{ doc.name }}</p>
   </div>
   <p><strong>Customer:</strong> {{ doc.customer_name }}<br>
   <strong>Date:</strong> {{ frappe.utils.formatdate(doc.posting_date) }}<br>
   <strong>Due Date:</strong> {{ frappe.utils.formatdate(doc.due_date) }}</p>
   <table style="width: 100%; border-collapse: collapse;">
     <tr><th style="text-align: left;">Item</th><th>Qty</th><th>Rate</th><th>Amount</th></tr>
     {% for row in doc.items %}
     <tr>
       <td>{{ row.item_name }}</td>
       <td>{{ row.qty }}</td>
       <td>{{ row.get_formatted("rate") }}</td>
       <td>{{ row.get_formatted("amount") }}</td>
     </tr>
     {% endfor %}
   </table>
   <p style="text-align: right;"><strong>Grand Total: {{ doc.get_formatted("grand_total") }}</strong></p>
   ```

   Print `SINV-0001` with it and check the totals match Desk.

### Checkpoint

You should now be able to answer, from your own report, "who owes us
what" — and hand a customer a printed invoice that looks like it came
from your factory, not from a default template.

### Common mistakes

- **Filtering in Python instead of in the query.** Filters belong in
  `query_filters` — fetching every invoice and filtering in a loop is
  the N+1 mistake in report form (see Lesson 14).
- **Using `frappe.db.sql` for a user-facing read.** It bypasses all
  permission checks. `frappe.get_list` respects them — use it.
- **Hard-coding the company name in the print format.** Use
  `{{ doc.company }}` — the format is reused on every company.

---

## Phase 8 — Lock it down: permissions, backup, go-live

**Uses:** [Lesson 09 — Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md),
[Lesson 21 — Ops](../learn/framework/level-4/21-ops.md),
[Go-Live Checklist](go-live-checklist.md)

### Steps

1. Create a **Role** "Gatekeeper" and give it Gate Pass permissions
   only: read, write, create — no submit, no delete, no access to
   Sales Invoice or Payment Entry. Assign it to the guard's user.
   Log in as that user and confirm: Gate Pass works, Sales Invoice
   does not open.

2. Take a backup before you call it done:

   ```bash
   bench --site spice.local backup
   ```

   Check the file exists under `sites/spice.local/private/backups/`.

3. Walk the [Go-Live Checklist](go-live-checklist.md) for this site:
   opening balances (your 200 kg receipt), permissions (step 1),
   training (show the guard the Gate Pass, show the manager the
   approval), and the rollback plan (restore from the backup in
   step 2).

### Checkpoint

You should now be able to hand the site to someone else: they can log
in with their own role, do only their job, and the whole thing can be
restored from backup if the bench dies.

### Common mistakes

- **Testing permissions as Administrator.** Administrator sees
  everything. Test with the real user accounts, or you have tested
  nothing.
- **One role for everything.** A "do everything" role is how a guard
  ends up able to cancel invoices.
- **No backup before go-live.** The first backup is always taken the
  day after the disaster. Take it now.

---

## What to build next

You have a working factory. These are the next real features, in the
order a client would ask for them:

1. **Production Plan** — turn open Sales Orders into Work Orders
   automatically instead of creating them by hand. See
   [Manufacturing](../learn/erpnext/operations/05-manufacturing.md).
2. **Batch tracking** — give each `RAW-CHILLI` receipt a Batch No and
   sell oldest-first (FEFO). See
   [Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md).
3. **Low-stock alert** — a nightly Scheduler job that emails when
   `RAW-CHILLI` falls below 50 kg. See
   [Lesson 11 — Scheduler & Background Jobs](../learn/framework/level-3/11-scheduler-jobs.md).
4. **Distributor portal** — let Karachi Spice Traders see their own
   orders and invoices, nothing else. See
   [Lesson 19 — Website & Portal](../learn/framework/level-4/19-website-portal.md).
5. **Insights dashboard** — monthly sales, outstanding amounts, and
   stock value on one page. See
   [Lesson 18 — Insights](../learn/framework/level-4/18-insights.md).

## How we can use it

This project is the demo NexTash shows a manufacturing client in the
first meeting: the same Gate Pass, the same spice flow, the same
quality gate — running on a laptop, with the client's own numbers
swapped in. A prospect who sees their own order go from Sales Order
to Paid invoice in ten minutes stops asking "does ERPNext do this?"
and starts asking "when can we start?".

## Sources

DocType fields verified against ERPNext v16 source (Sales Order,
Delivery Note Item, Stock Entry, Quality Inspection, Payment Entry)
and the ERPNext docs (order-to-cash flow, Quality Inspection
enforcement, Payment Entry references). Lesson links point at this
hub's own lessons; the Gate Pass fields match
[Lesson 03](../learn/framework/level-1/03-first-doctype.md) exactly.
