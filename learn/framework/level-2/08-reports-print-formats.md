# 08 — Reports & Print Formats

## What it is

A **report** answers a question over many records ("which gate passes are
still open this month?"). A **print format** renders one document for
paper or PDF ("the gate pass itself"). Pick the report type first:

| Type | For |
|---|---|
| **Report Builder** (no code) | A filtered list of one DocType — prefer it when it is enough |
| **Query Report** | One SQL query, no Python logic |
| **Script Report** | Logic, several sources, computed columns — the default for custom reports |

A standard report lives in your app, so it is versioned:

```text
my_app/my_module/report/gate_pass_register/
  gate_pass_register.json   # the Report definition
  gate_pass_register.py     # execute(filters) -> columns, data
  gate_pass_register.js     # filters
```

## Minimal working example — Gate Pass Register (Script Report)

```python
# gate_pass_register.py
import frappe
from frappe import _


def execute(filters=None):
    filters = frappe._dict(filters or {})
    validate_filters(filters)
    return get_columns(), get_data(filters)


def validate_filters(filters):
    if filters.from_date and filters.to_date and filters.from_date > filters.to_date:
        frappe.throw(_("From Date cannot be after To Date"))


def get_columns():
    return [
        {"label": _("Gate Pass"), "fieldname": "name", "fieldtype": "Link", "options": "Gate Pass", "width": 140},
        {"label": _("Date"), "fieldname": "gate_pass_date", "fieldtype": "Date", "width": 110},
        {"label": _("Visitor"), "fieldname": "visitor_name", "fieldtype": "Data", "width": 160},
        {"label": _("Company"), "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 160},
        {"label": _("Purpose"), "fieldname": "purpose", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    query_filters = {}
    if filters.get("company"):
        query_filters["company"] = filters.company
    if filters.get("purpose"):
        query_filters["purpose"] = filters.purpose
    if filters.get("from_date") and filters.get("to_date"):
        query_filters["gate_pass_date"] = ("between", [filters.from_date, filters.to_date])
    elif filters.get("from_date"):
        query_filters["gate_pass_date"] = (">=", filters.from_date)
    elif filters.get("to_date"):
        query_filters["gate_pass_date"] = ("<=", filters.to_date)
    return frappe.get_list(
        "Gate Pass",
        filters=query_filters,
        fields=["name", "gate_pass_date", "visitor_name", "company", "purpose"],
        order_by="gate_pass_date desc",
    )
```

```js
// gate_pass_register.js
frappe.query_reports["Gate Pass Register"] = {
    filters: [
        { fieldname: "from_date", label: __("From Date"), fieldtype: "Date", default: frappe.datetime.month_start(), reqd: 1 },
        { fieldname: "to_date", label: __("To Date"), fieldtype: "Date", default: frappe.datetime.month_end(), reqd: 1 },
        { fieldname: "company", label: __("Company"), fieldtype: "Link", options: "Company" },
        { fieldname: "purpose", label: __("Purpose"), fieldtype: "Select", options: "\nVisit\nDelivery\nPickup" },
    ],
};
```

Columns are dicts with a real `fieldtype` (Currency, Link, Date) — not
`"Customer:Link/Customer:180"` strings in new code. Filters are applied
in the query, not in Python. `frappe.get_list` respects permissions;
`frappe.db.sql` bypasses **all** permission checks — never use it for
user-facing reads.

## Minimal example — a Print Format (Jinja)

Desk → **Print Format** → New, DocType: Gate Pass, Print Format Type:
**Jinja**. The template gets `doc` (the document) and `frappe`:

```jinja
<h2>Gate Pass {{ doc.name }}</h2>
<p>{{ _("Date") }}: {{ doc.get_formatted("gate_pass_date") }}
&nbsp; {{ _("Visitor") }}: {{ doc.visitor_name }}</p>
<table>
  <tr><th>{{ _("Item") }}</th><th>{{ _("Qty") }}</th><th>{{ _("Direction") }}</th></tr>
  {% for row in doc.items %}
  <tr><td>{{ row.item_name }}</td><td>{{ row.qty }}</td><td>{{ row.direction }}</td></tr>
  {% endfor %}
</table>
```

Use `doc.get_formatted("field")` for currency and dates, `_()` for labels,
and keep database calls out of loops (`frappe.db.get_value` sparingly,
never one per row). Prefer the Print Format Builder, or a Jinja format
stored in your app as a standard print format, so it ships with the app.

## When to use — and when not to

| Situation | Use |
|---|---|
| A filtered list of one DocType | Report Builder — no code at all |
| One SQL query, fixed columns | Query Report |
| Logic, several DocTypes, computed values | Script Report |
| A document on paper / PDF | Print Format (Builder first, Jinja when you need layout control) |
| The same report for every client | Standard report in the app (`Is Standard = Yes`, module set) |
| A one-off question for one user | Report Builder, or a saved filter on the List View — not a coded report |

## Common mistakes

- **`frappe.get_doc` inside a loop (N+1).** One query per row makes a
  500-row report take 30 seconds. Fetch once, then look up in a dict
  (see `guides/common-mistakes.md` §4).
- **Filters applied in Python.** Filter in the query — the database is
  faster than your loop, and it respects permissions.
- **`frappe.db.sql` for a user-facing report.** It bypasses permissions.
  Use `frappe.get_list`, Query Builder, or a permission-aware query.
- **Columns as strings in new code.** Use dicts with `fieldtype` — the
  report renders links, currency and dates correctly.
- **Database queries inside a Jinja loop.** One `get_value` per row in a
  print format is the same N+1 mistake, on paper.
- **A coded report for a one-off question.** If Report Builder answers
  it, ship nothing. Code is maintenance.

## Next

[09 — Permissions & Roles](09-permissions-roles.md) — who can see, edit,
submit, and print all of this. Role Permissions, field-level permissions,
User Permissions, and sharing.
