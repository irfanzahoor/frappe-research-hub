# 08 — Reports & Print Formats

## Yeh kya hai

Ek **report** kayi records par ek sawaal ka jawab deti hai ("is mahine kaun
se gate pass abhi bhi khule hain?"). Ek **print format** ek document ko
paper ya PDF ke liye render karta hai ("khud gate pass"). Pehle report ki
type chunein:

| Type | Kis ke liye |
|---|---|
| **Report Builder** (bina code) | Ek DocType ki filtered list — jab yeh kaafi ho to isi ko tarjeeh dein |
| **Query Report** | Ek SQL query, bina Python logic |
| **Script Report** | Logic, kayi sources, computed columns — custom reports ke liye default |

Ek standard report aapki app mein rehti hai, is liye yeh versioned hoti hai:

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

Columns dicts hote hain jinn mein asal `fieldtype` hota hai (Currency, Link,
Date) — naye code mein `"Customer:Link/Customer:180"` strings nahi. Filters
query mein lagaye jate hain, Python mein nahi. `frappe.get_list` permissions
ka khayal rakhta hai; `frappe.db.sql` **tamam** permission checks ko bypass
kar deta hai — user-facing reads ke liye isay kabhi istemal na karein.

## Minimal example — ek Print Format (Jinja)

Desk → **Print Format** → New, DocType: Gate Pass, Print Format Type:
**Jinja**. Template ko `doc` (document) aur `frappe` milta hai:

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

Currency aur dates ke liye `doc.get_formatted("field")` istemal karein,
labels ke liye `_()`, aur database calls ko loops se bahar rakhein
(`frappe.db.get_value` kam se kam, kabhi bhi har row par ek nahi). Print
Format Builder ko tarjeeh dein, ya ek Jinja format jo aapki app mein
standard print format ke tor par save ho, taake yeh app ke saath ship ho.

## Kab istemal karein — aur kab nahi

| Situation | Use |
|---|---|
| Ek DocType ki filtered list | Report Builder — bilkul code nahi |
| Ek SQL query, fixed columns | Query Report |
| Logic, kayi DocTypes, computed values | Script Report |
| Paper / PDF par ek document | Print Format (pehle Builder, layout control chahiye ho to Jinja) |
| Har client ke liye wohi report | App mein standard report (`Is Standard = Yes`, module set) |
| Ek user ke liye ek baar ka sawaal | Report Builder, ya List View par save kiya hua filter — coded report nahi |

## Aam ghaltiyan

- **Loop ke andar `frappe.get_doc` (N+1).** Har row par ek query se 500-row
  wali report 30 second leti hai. Ek dafa fetch karein, phir dict mein
  lookup karein (dekhein `guides/common-mistakes.md` §4).
- **Filters Python mein lagana.** Filter query mein lagayein — database
  aapke loop se tez hai, aur yeh permissions ka khayal rakhta hai.
- **User-facing report ke liye `frappe.db.sql`.** Yeh permissions ko bypass
  karta hai. `frappe.get_list`, Query Builder, ya permission-aware query
  istemal karein.
- **Naye code mein columns strings ke tor par.** `fieldtype` wale dicts
  istemal karein — report links, currency aur dates ko sahi render karta
  hai.
- **Jinja loop ke andar database queries.** Print format mein har row par
  ek `get_value` wohi N+1 ghalti hai, paper par.
- **Ek baar ke sawaal ke liye coded report.** Agar Report Builder jawab de
  de to kuch ship na karein. Code maintenance hai.

## Next

[09 — Permissions & Roles](09-permissions-roles.md) — kaun yeh sab dekh
sakta hai, edit kar sakta hai, submit kar sakta hai, aur print kar sakta
hai. Role Permissions, field-level permissions, User Permissions, aur
sharing.
