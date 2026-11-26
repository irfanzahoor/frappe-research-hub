# 06 — Client Scripts

## What it is

A **Client Script** is JavaScript that runs in the user's browser, on the
form. It controls behaviour and experience: show or hide a field, make a
field mandatory, filter a Link, add a button, fetch a value and show it.
It is **UX only** — it is not security and not validation. Anything the
browser can do, the API can skip.

For a DocType your app owns, the script lives with the DocType:

```text
my_app/doctype/gate_pass/gate_pass.js   # form behaviour for Gate Pass
```

For another app's DocType (Sales Order, Delivery Note), use the **Client
Script** DocType in Desk, or `doctype_js` in hooks.py pointing at a file in
`public/js/`. Never duplicate the same `frappe.ui.form.on` block for one
DocType — extend the existing handler.

## Minimal working example — Gate Pass form

```js
// gate_pass.js
frappe.ui.form.on("Gate Pass", {
    setup(frm) {
        // set_query belongs here — it runs once per form load
        frm.set_query("company", () => ({ filters: { disabled: 0 } }));
    },

    refresh(frm) {
        // Items are mandatory for Delivery / Pickup, optional for Visit
        frm.toggle_reqd("items", ["Delivery", "Pickup"].includes(frm.doc.purpose));
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__("Mark Returned"), () => {
                frappe.call({
                    method: "my_app.gate_pass.api.mark_returned",
                    args: { name: frm.doc.name },
                    callback() { frm.reload_doc(); },
                });
            }, __("Actions"));
        }
    },

    purpose(frm) {
        // Runs whenever the Purpose field changes
        frm.toggle_reqd("items", ["Delivery", "Pickup"].includes(frm.doc.purpose));
        frm.refresh_field("items");
    },

    validate(frm) {
        // A UX hint only — the server re-checks this in validate() (Lesson 05)
        if (["Delivery", "Pickup"].includes(frm.doc.purpose) && !frm.doc.items.length) {
            frappe.msgprint(__("Add at least one item for a Delivery or Pickup pass"));
        }
    },
});
```

The server side the button needs (Lesson 07 has the full pattern):

```python
# my_app/gate_pass/api.py
import frappe


@frappe.whitelist()
def mark_returned(name):
    doc = frappe.get_doc("Gate Pass", name)
    doc.check_permission("write")
    doc.db_set("status", "Returned")
```

> The Gate Pass needs a `status` field for this to work — add a Select
> (`Open` / `Returned`, default `Open`) to the DocType from Lesson 03.

## The form events you will use most

| Event | When it runs |
|---|---|
| `setup(frm)` | Once per form load — `set_query` goes here |
| `onload(frm)` | When the form loads (after setup) |
| `refresh(frm)` | Every time the form re-renders — buttons and visibility go here |
| `fieldname(frm)` | When one field changes (for example `purpose(frm)`) |
| `validate(frm)` | Before save — UX hint only, never the real check |
| `after_save(frm)` | After a successful save |

Child table rows get their own block, in the **parent's** file:

```js
frappe.ui.form.on("Gate Pass Item", {
    qty(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        if (row.qty <= 0) {
            frappe.msgprint(__("Row {0}: Qty must be greater than 0", [row.idx]));
        }
    },
    items_remove(frm) {
        frappe.show_alert({ message: __("Item removed"), indicator: "orange" }, 3);
    },
});
```

## When to use — and when not to

| Situation | Use |
|---|---|
| Show/hide a field, make it mandatory | Client Script (`toggle_display`, `toggle_reqd`) |
| Filter a Link field's options | `frm.set_query` in `setup` |
| Copy a field from a linked document | **Fetch From** on the field in the DocType — not JS |
| Static visibility / mandatory rules | **Depends On / Mandatory Depends On** in the DocType — not JS |
| A button that does server work | `frm.add_custom_button` + `frappe.call` to a whitelisted method |
| A rule that must hold | Server `validate()` (Lesson 05) — JS may only hint at it |
| Reading data that rarely changes | Load once in `onload` — do not call the server from `refresh` |

## Common mistakes

- **Validation only in JS.** The API bypasses the form entirely. Every
  rule that matters lives in the controller.
- **`set_query` in `refresh` or a field event.** It runs on every render.
  Put it in `setup`.
- **Hiding a field in JS to "secure" it.** Anyone can read the field
  through the API. Use permlevel — Lesson 09.
- **`cur_frm`.** Use the `frm` argument the event gives you.
- **Two `frappe.ui.form.on` blocks for the same DocType** in one file.
  Extend the one handler.
- **Direct DOM manipulation** (`$(...)` on form fields) when a `frm.*`
  API exists (`set_value`, `set_df_property`, `toggle_display`).
- **Synchronous server calls** (`async: false`). Use promises (`.then`)
  or `async/await`.
- **Saving through the API for the open form.** Use `frm.set_value`,
  then `frm.save()` — never `frappe.client.set_value` on the open form.

## Next

[07 — APIs](07-apis.md) — `frappe.call`, whitelisted methods, and the REST
API. How the browser, other systems, and your own code talk to the server.
