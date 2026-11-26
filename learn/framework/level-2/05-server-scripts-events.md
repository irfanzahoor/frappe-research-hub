# 05 — Server Scripts & Document Events

## What it is

Server-side logic is the logic that **must** run — validation, totals,
status changes, creating linked records. It runs on the server, so no one
can bypass it from the browser or the API. There are three places it can
live, and picking the wrong one is the most common Level 2 mistake:

| Where | For |
|---|---|
| **Controller** (`gate_pass.py`) | Logic on a DocType your own app owns |
| **Server Script** (Desk → Server Script) | A quick rule, no app deploy needed |
| **`doc_events` in hooks.py** | Logic on another app's DocType (Sales Order, Delivery Note) |

The controller runs at fixed points in a document's life — the **hooks**:

| Hook | When it runs |
|---|---|
| `before_insert` | Before a new document is saved the first time |
| `validate` | Before every save (this is "Before Save") |
| `before_save` | After validate, before the save writes |
| `on_update` | After every save |
| `before_submit` / `on_submit` | Around submit (posting happens here) |
| `before_cancel` / `on_cancel` | Around cancel (reversals happen here) |
| `on_trash` | Before delete |

## Minimal working example — Gate Pass controller

First, tick **Is Submittable** on the Gate Pass DocType from Lesson 03, so
Submit exists. Then the controller:

```python
# my_app/my_module/doctype/gate_pass/gate_pass.py
import frappe
from frappe import _
from frappe.model.document import Document


class GatePass(Document):
    def validate(self):
        # Delivery / Pickup passes must list what is carried
        if self.purpose in ("Delivery", "Pickup") and not self.items:
            frappe.throw(
                _("Add at least one item for a {0} pass").format(self.purpose)
            )
        for row in self.items:
            if row.qty <= 0:
                frappe.throw(
                    _("Row {0}: Qty must be greater than 0").format(row.idx)
                )

    def on_submit(self):
        # A reminder for whoever submitted it — created by the system
        frappe.get_doc({
            "doctype": "ToDo",
            "description": _("Gate Pass {0} for {1} submitted").format(
                self.name, self.visitor_name
            ),
            "reference_type": self.doctype,
            "reference_name": self.name,
            "allocated_to": frappe.session.user,
            "status": "Open",
        }).insert(ignore_permissions=True)  # system-created, not a user action
```

Rules inside `validate` / `before_save`: set fields on `self` directly,
never call `self.save()`. Inside `on_update` / `on_submit`, if you must
change your own fields, use `self.db_set("field", value)`. Use
`frappe.utils` helpers (`flt`, `getdate`, `add_days`, `date_diff`) — never
`float()` / `int()` on doc fields, which may be `None`.

## Same rule, no code deploy — a Server Script

Desk → search **Server Script** → New. Type: **Document Event**,
Document Type: **Sales Order**, DocType Event: **Before Save**:

```python
# No import statements — frappe and frappe.utils are pre-loaded
if doc.delivery_date and frappe.utils.date_diff(doc.delivery_date, frappe.utils.today()) < 0:
    frappe.throw(_("Delivery Date cannot be in the past"))
```

Server Scripts run in a RestrictedPython sandbox: no `import`, no `raise`
(use `frappe.throw`), and `try/except` is blocked on v14–v15 — use `if`
checks such as `frappe.db.exists()`. On v15+ they are disabled by default;
enable with `bench set-config -g server_script_enabled 1`. Not available
on Frappe Cloud shared benches.

**Event name trap:** in a Server Script, "Before Save" is the `validate`
hook, not `before_save`. "After Save" is `on_update`, "Before Submit" is
`before_submit`, "After Submit" is `on_submit`.

## Same rule, another app's DocType — `doc_events`

Your app does not own Sales Order, so you do not touch its controller. You
register a hook in `hooks.py` — a registry only, no logic in it:

```python
# hooks.py
doc_events = {
    "Sales Order": {
        "validate": "my_app.selling.overrides.sales_order.validate",
    },
}
```

```python
# my_app/selling/overrides/sales_order.py
import frappe
from frappe import _


def validate(doc, method=None):
    if frappe.db.get_value("Customer", doc.customer, "disabled"):
        frappe.throw(
            _("Customer {0} is disabled").format(frappe.bold(doc.customer))
        )
```

## When to use — and when not to

| Situation | Use |
|---|---|
| Logic on your own DocType | Controller method (`validate`, `on_submit`, …) |
| One quick rule, no app release yet | Server Script |
| Logic on ERPNext's DocType | `doc_events` in hooks.py → override file in your app |
| Rule over 50 lines, needs imports or tests | Controller — never a Server Script |
| Showing/hiding a field, a button, a hint | Client Script (Lesson 06), not the server |
| Calling an external API | `on_update` / `on_submit` + `frappe.enqueue` — never in `validate` |

## Common mistakes

- **Logic inside `hooks.py`.** It is a registry of dotted paths. The code
  lives in the file the path points to.
- **`doc_events` for a DocType your own app owns.** Use the controller —
  no hooks entry is needed at all.
- **`"*"` doc_events.** It runs on every save of every DocType, forever.
- **Validation only in JS.** JS is UX (Lesson 06). A rule enforced in JS
  alone is not a rule — the API bypasses it.
- **Submit-only work in `validate`.** `validate` runs on every save,
  including drafts. Posting and ledger work belongs in `on_submit`.
- **Calling `self.save()` inside `validate`.** You are already inside a
  save. Set fields on `self` and return.
- **Editing another app's files.** Never edit `apps/erpnext/...` — the
  next update wipes it. Extend from your app.
- **A Server Script that grew into an app.** Over 50 lines, external
  libraries, or tests needed? Move it to a controller.

## Next

[06 — Client Scripts](06-client-scripts.md) — form behaviour, validation
hints, and UX. What belongs in the browser, and what must stay on the
server.
