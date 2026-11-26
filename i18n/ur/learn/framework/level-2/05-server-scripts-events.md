# 05 — Server Scripts & Document Events

## Yeh kya hai

Server-side logic woh logic hai jo **lazmi** chalni chahiye — validation, totals,
status changes, linked records banana. Yeh server par chalti hai, is liye koi
bhi isay browser ya API se bypass nahi kar sakta. Is ke rehne ki teen jagahain
hain, aur ghalat jagah chunna Level 2 ki sab se aam ghalti hai:

| Kahan | Kis ke liye |
|---|---|
| **Controller** (`gate_pass.py`) | Apni app ke DocType par logic |
| **Server Script** (Desk → Server Script) | Ek quick rule, app deploy kiye baghair |
| **`doc_events` in hooks.py** | Doosri app ke DocType par logic (Sales Order, Delivery Note) |

Controller document ki zindagi ke fixed points par chalta hai — yeh **hooks**
hain:

| Hook | Kab chalta hai |
|---|---|
| `before_insert` | Naya document pehli dafa save hone se pehle |
| `validate` | Har save se pehle (yeh "Before Save" hai) |
| `before_save` | Validate ke baad, save likhne se pehle |
| `on_update` | Har save ke baad |
| `before_submit` / `on_submit` | Submit ke aas paas (posting yahin hoti hai) |
| `before_cancel` / `on_cancel` | Cancel ke aas paas (reversals yahin hote hain) |
| `on_trash` | Delete se pehle |

## Chhoti si working example — Gate Pass controller

Pehle, Lesson 03 wale Gate Pass DocType par **Is Submittable** tick karein, taake
Submit maujood ho. Phir controller:

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

`validate` / `before_save` ke andar rules: `self` par fields direct set karein,
kabhi `self.save()` call na karein. `on_update` / `on_submit` ke andar, agar aap
ko apne hi fields badalne hon, to `self.db_set("field", value)` use karein.
`frappe.utils` helpers use karein (`flt`, `getdate`, `add_days`, `date_diff`) — doc
fields par kabhi `float()` / `int()` na use karein, jo `None` bhi ho sakte hain.

## Wohi rule, code deploy kiye baghair — ek Server Script

Desk → **Server Script** search karein → New. Type: **Document Event**,
Document Type: **Sales Order**, DocType Event: **Before Save**:

```python
# No import statements — frappe and frappe.utils are pre-loaded
if doc.delivery_date and frappe.utils.date_diff(doc.delivery_date, frappe.utils.today()) < 0:
    frappe.throw(_("Delivery Date cannot be in the past"))
```

Server Scripts RestrictedPython sandbox mein chalte hain: koi `import` nahi, koi
`raise` nahi ( `frappe.throw` use karein), aur v14–v15 par `try/except` blocked
hai — `frappe.db.exists()` jaise `if` checks use karein. v15+ par yeh by default
disabled hote hain; `bench set-config -g server_script_enabled 1` se enable
karein. Frappe Cloud shared benches par available nahi hain.

**Event name trap:** Server Script mein "Before Save" `validate`
hook hai, `before_save` nahi. "After Save" `on_update` hai, "Before Submit"
`before_submit` hai, "After Submit" `on_submit` hai.

## Wohi rule, doosri app ke DocType ke liye — `doc_events`

Aap ki app Sales Order ki malik nahi hai, is liye aap us ke controller ko nahi
chhedein ge. Aap `hooks.py` mein ek hook register karte hain — sirf ek registry,
is mein koi logic nahi hoti:

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

## Kab use karein — aur kab nahi

| Situation | Use karein |
|---|---|
| Apne DocType par logic | Controller method (`validate`, `on_submit`, …) |
| Ek quick rule, abhi app release nahi hui | Server Script |
| ERPNext ke DocType par logic | `doc_events` in hooks.py → apni app mein override file |
| 50 lines se bara rule, imports ya tests chahiye | Controller — kabhi Server Script nahi |
| Field show/hide karna, button, hint | Client Script (Lesson 06), server nahi |
| External API call karna | `on_update` / `on_submit` + `frappe.enqueue` — kabhi `validate` mein nahi |

## Aam ghaltiyan

- **Logic `hooks.py` ke andar.** Yeh dotted paths ki registry hai. Code us
  file mein rehta hai jis ki taraf path ishara karta hai.
- **Apni app ke DocType ke liye `doc_events`.** Controller use karein —
  hooks entry ki bilkul zaroorat nahi.
- **`"*"` doc_events.** Yeh har DocType ke har save par chalega, hamesha.
- **Validation sirf JS mein.** JS UX hai (Lesson 06). Sirf JS mein lagaya
  gaya rule rule nahi hai — API isay bypass kar deti hai.
- **Sirf submit ka kaam `validate` mein.** `validate` har save par chalta
  hai, drafts par bhi. Posting aur ledger ka kaam `on_submit` mein hai.
- **`validate` ke andar `self.save()` call karna.** Aap pehle se save ke
  andar hain. `self` par fields set karein aur return karein.
- **Doosri app ki files edit karna.** Kabhi `apps/erpnext/...` edit na
  karein — agli update isay mita degi. Apni app se extend karein.
- **Server Script jo app ban gaya.** 50 lines se zyada, external
  libraries, ya tests chahiye? Isay controller mein le jayein.

## Agla

[06 — Client Scripts](06-client-scripts.md) — form behaviour, validation
hints, aur UX. Browser mein kya rehta hai, aur server par kya rehna chahiye.
