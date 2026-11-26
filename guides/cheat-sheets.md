# Cheat Sheets — Frappe & ERPNext Quick Reference

The pages to keep open while you work. No explanations — just the
command, the hook, or the call, and one line on what it does. If you
need the why, the linked lesson has it. `<site>` means your site name,
e.g. `erp.local`.

---

## 1. Bench commands

Run these from inside your bench directory (`~/frappe-bench`).
`bench --site <site> <command>` targets one site; run
`bench use <site>` once and you can drop `--site <site>` after that.

| Command | What it does |
|---|---|
| `bench --version` | Show the bench CLI version |
| `bench version` | Show the version of every app on the bench |
| `bench init <name>` | Create a new bench (run from your home directory) |
| `bench new-site <site>` | Create a new site |
| `bench use <site>` | Make `<site>` the default, so `--site` is optional |
| `bench get-app <app>` | Download an app into `apps/` (name or git URL) |
| `bench --site <site> install-app <app>` | Install an app on a site |
| `bench --site <site> uninstall-app <app>` | Remove an app from a site |
| `bench --site <site> list-apps` | List the apps installed on a site |
| `bench start` | Start the dev server (foreground — `Ctrl+C` stops it) |
| `bench restart` | Restart all bench services (workers, scheduler, web) |
| `bench --site <site> migrate` | Run database migrations / patches for a site |
| `bench build` | Rebuild JS + CSS assets for all apps |
| `bench build --app <app>` | Rebuild assets for one app only |
| `bench update` | Pull + migrate + build + restart, for everything |
| `bench --site <site> backup` | Back up the site database |
| `bench --site <site> backup --with-files` | Back up database + public and private files |
| `bench --site <site> restore <file>` | Restore a site from a backup file |
| `bench --site <site> clear-cache` | Clear the site cache (stale lists, old values) |
| `bench --site <site> console` | Python console with Frappe loaded — try things live |
| `bench --site <site> mariadb` | Open the MariaDB console for the site |
| `bench doctor` | Health check: scheduler, workers, Redis, Socket.IO |
| `bench --site <site> enable-scheduler` | Turn the scheduler on for a site |
| `bench --site <site> disable-scheduler` | Turn the scheduler off for a site |
| `bench --site <site> set-config <key> <value>` | Set a value in `site_config.json` |
| `bench --site <site> show-config` | Show the site's current config |
| `bench --site <site> execute <dotted.path>` | Run one Python function, e.g. `bench --site <site> execute frappe.utils.scheduler.enqueue_scheduler_events` |
| `bench drop-site <site>` | Delete a site (destructive — back up first) |

!!! warning "Before `bench update` or `bench restore`"
    Back up first: `bench --site <site> backup`. An update you can
    undo is an update you can try. See [Troubleshooting](troubleshooting.md)
    if the update fails halfway.

---

## 2. Hooks (`hooks.py`)

All of these live in your app's `hooks.py`. One line each — copy the
shape, change the names.

| Hook | Minimal example |
|---|---|
| `doc_events` | `doc_events = {"Sales Order": {"on_submit": "my_app.api.on_sales_order_submit"}}` |
| `before_insert` | `"Sales Order": {"before_insert": "my_app.api.set_defaults"}` — runs before the first save |
| `validate` | `"Sales Order": {"validate": "my_app.api.check_credit_limit"}` — runs on every save, before insert/update |
| `on_submit` | `"Sales Order": {"on_submit": "my_app.api.create_gate_pass"}` — runs when the document is submitted |
| `on_cancel` | `"Sales Order": {"on_cancel": "my_app.api.reverse_gate_pass"}` — runs when a submitted document is cancelled |
| `after_migrate` | `after_migrate = "my_app.setup.after_migrate"` — runs once, after every `bench migrate` |
| `fixtures` | `fixtures = ["Custom Field", "Property Setter"]` — export these DocTypes with the app |
| `scheduler_events` | `scheduler_events = {"daily": ["my_app.tasks.send_daily_report"], "hourly": ["my_app.tasks.sync_stock"], "cron": {"0 9 * * *": ["my_app.tasks.morning_job"]}, "all": ["my_app.tasks.every_minute"]}` |
| `override_doctype_class` | `override_doctype_class = {"Sales Order": "my_app.overrides.CustomSalesOrder"}` |
| `permission_query_conditions` | `permission_query_conditions = {"Sales Order": "my_app.permissions.sales_order_condition"}` |
| `get_permission_query_conditions` | `get_permission_query_conditions = {"Sales Order": "my_app.permissions.sales_order_condition"}` — newer form of the same hook |
| `jinja` | `jinja = {"methods": ["my_app.utils.format_amount"], "filters": ["my_app.utils.to_words"]}` |
| `page_js` | `page_js = {"sales-order": "public/js/sales_order_list.js"}` — JS on one Desk page |
| `app_include_js` | `app_include_js = "/assets/my_app/js/my_app.js"` — JS on every Desk page |
| `app_include_css` | `app_include_css = "/assets/my_app/css/my_app.css"` — CSS on every Desk page |
| `website_route_rules` | `website_route_rules = [{"from_route": "/track/<order_id>", "to_route": "track-order"}]` |
| `notification_config` | `notification_config = "my_app.notifications.get_notification_config"` |

!!! tip "Doc events vs `validate`"
    `validate` runs on **every** save; `before_insert` runs once, on
    the first save; `on_submit` / `on_cancel` only run on submitted
    documents. Pick the narrowest event that fits — see Lesson 05.

---

## 3. Server Script / API essentials

```python
# Read
doc = frappe.get_doc("Sales Order", "SO-0001")      # one document, by name
docs = frappe.get_list("Sales Order",
    filters={"status": "To Deliver"}, fields=["name", "customer"])
rows = frappe.get_all("Item", filters={"is_stock_item": 1},
    fields=["item_code", "item_name"])              # like get_list, no permissions
value = frappe.db.get_value("Customer", "CUST-001", "customer_name")

# Create / change
doc = frappe.new_doc("Gate Pass")
doc.visitor_name = "Ahmed"
doc.insert()                                        # save as draft
doc.submit()                                        # submit (needs a submittable DocType)
frappe.db.set_value("Sales Order", "SO-0001", "status", "Closed")

# SQL — always parameterised, never string formatting
frappe.db.sql(
    "select name from `tabSales Order` where customer=%s and status=%s",
    ("CUST-001", "To Deliver"))

# Talk to the user
frappe.msgprint("Gate Pass created")                # green message
frappe.throw("Credit limit exceeded")               # red error, stops the save
```

!!! danger "Never build SQL with f-strings"
    `frappe.db.sql(f"... where customer='{name}'")` is an SQL injection
    hole. Always pass values as the second argument, with `%s`
    placeholders — as above.

```python
# Expose a function to the browser
@frappe.whitelist()
def create_gate_pass(sales_order):
    ...
```

```javascript
// Call it from a Client Script
frappe.call({
    method: "my_app.api.create_gate_pass",
    args: { sales_order: frm.doc.name },
    callback: function(r) {
        frappe.msgprint(r.message);
    }
});
```

```javascript
// Client Script skeleton — frm is the form, not cur_frm
frappe.ui.form.on("Sales Order", {
    refresh: function(frm) {
        // runs every time the form opens or refreshes
    },
    customer: function(frm) {
        // runs when the customer field changes
    },
    validate: function(frm) {
        // runs before save — frappe.throw() here blocks the save
    }
});
```

!!! tip "`frm` vs `cur_frm`"
    `frm` is the form object passed into your function — use it.
    `cur_frm` is an old global that points at whatever form happens
    to be open. In new code, always use `frm`.

**Filters you will actually use:** `{"status": "Open"}` (equals),
`{"status": ["!=", "Cancelled"]}` (not equals),
`{"creation": [">", "2026-01-01"]}` (comparison),
`{"name": ["in", ["SO-0001", "SO-0002"]]}` (in a list),
`{"customer": ["like", "%Ahmed%"]}` (partial match).

---

## 4. DocType field types

| Type | Use when |
|---|---|
| Data | Short single-line text — names, codes, phone numbers |
| Link | A reference to another DocType (Customer, Item, Warehouse) |
| Select | A fixed list of options the user picks from |
| Check | A yes/no checkbox |
| Date | A calendar date, no time |
| Datetime | Date + time (created on, scheduled at) |
| Currency | Money — always with a currency field next to it |
| Float | A decimal number that is not money (rate, weight) |
| Int | A whole number (quantity, count) |
| Text | A few lines of text — addresses, short notes |
| Long Text | Long free text — descriptions, remarks |
| Table | A child table — line items, e.g. Gate Pass Item |
| Attach | One file upload |
| HTML | Formatted text shown on the form (instructions, banners) |
| Button | A clickable button that runs code |
| Section Break | Start a new labelled section on the form |
| Column Break | Split the current section into columns |
| Tab Break | Start a new tab on the form |

!!! tip "Layout rule"
    Section Break → fields → Column Break → fields. A field with no
    Section Break above it lands in the wrong place. See
    [Common Mistakes](common-mistakes.md).

---

## 5. Permissions & roles

| Role | Typically controls |
|---|---|
| Administrator | Everything — the built-in super user |
| System Manager | Setup, users, roles, customisations (not data) |
| Sales User / Sales Manager | Selling: Quotation, Sales Order, Delivery Note, Customer |
| Stock User / Stock Manager | Stock: Item, Warehouse, Stock Entry, Stock Ledger |
| Accounts User / Accounts Manager | Accounting: invoices, payments, journals, reports |
| HR User / HR Manager | Employee, Leave, Attendance, Payroll |
| Manufacturing User / Manufacturing Manager | BOM, Work Order, Production |
| Projects User / Projects Manager | Project, Task, Timesheet |
| Support Team | Issue, Helpdesk tickets |
| Customer / Supplier | Portal access only — their own orders, invoices, tickets |
| Guest | Public website pages, no Desk access |
| All | Every logged-in user (use sparingly — it means everyone) |

Permissions live in **Role Permission Manager** (search it in the
awesome bar): pick a DocType, pick a role, tick Read / Write / Create /
Submit / Cancel / Delete, and set a **permlevel** for field-level
control. Print/export/share are separate checkboxes on the same row.

### The 3 permission mistakes that hurt most

1. **Hiding a field in JS is not security.** Anyone can read the
   field through the API. Hide it with permlevel, not JavaScript.
2. **`ignore_permissions=True` without a reason.** If you pass it,
   write the reason in a comment next to it — otherwise the next
   developer copies it everywhere.
3. **`allow_guest=True` on anything that writes.** Guest endpoints
   are read-only, rate-limited, and must validate every input.

Full lesson: [Lesson 09 — Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md).

---

## Where to go next

- Lesson 02 — [Bench, Sites & Apps](../learn/framework/level-1/02-bench-sites-apps.md) for bench setup
- Lesson 05 — [Server Scripts & Document Events](../learn/framework/level-2/05-server-scripts-events.md) for hooks and server code
- Lesson 06 — [Client Scripts](../learn/framework/level-2/06-client-scripts.md) for `frappe.ui.form.on`
- Lesson 07 — [APIs](../learn/framework/level-2/07-apis.md) for `frappe.whitelist` and `frappe.call`
- Lesson 09 — [Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md) for the full permissions model
- [Troubleshooting](troubleshooting.md) — when a command above fails
