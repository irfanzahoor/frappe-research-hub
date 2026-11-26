# 07 — APIs

## What it is

Every DocType already has an API — the form, the list and the REST API are
all the same server underneath. There are three ways to call it:

| Way | From | For |
|---|---|---|
| `frm.call("method")` | The open form | A method on the current document's controller |
| `frappe.call({ method: "app.module.file.fn" })` | Any form JS | A module-level whitelisted function |
| REST: `/api/resource/...`, `/api/method/...` | Any system, curl, Postman | Other apps and integrations |

A Python function is callable from outside **only** if it has
`@frappe.whitelist()`. Without the decorator, the call is a 403. And every
whitelisted function is a public endpoint — it must check permissions
before returning data, not after.

## Minimal working example — check available stock

A whitelisted function in your app:

```python
# my_app/stock/api.py
import frappe


@frappe.whitelist()
def get_available_qty(item_code, warehouse):
    frappe.has_permission("Bin", "read", throw=True)
    qty = frappe.db.get_value(
        "Bin",
        {"item_code": item_code, "warehouse": warehouse},
        "actual_qty",
    )
    return qty or 0
```

Call it from a Sales Order form — a "Check Stock" button:

```js
frm.add_custom_button(__("Check Stock"), () => {
    const row = (frm.doc.items || [])[0];
    if (!row) return;
    frappe.call({
        method: "my_app.stock.api.get_available_qty",
        args: { item_code: row.item_code, warehouse: row.warehouse },
        callback(r) {
            frappe.msgprint(__("Available qty: {0}", [r.message]));
        },
    });
}, __("Actions"));
```

Call the same logic from outside Frappe, over REST. First create a
**dedicated API user** with minimal roles (never use Administrator keys),
then generate its keys (User → API Access → Generate Keys):

```bash
# Read one Sales Order
curl "https://mysite.local/api/resource/Sales%20Order/SAL-ORD-2026-00001" \
  -H "Authorization: token <api_key>:<api_secret>" \
  -H "Accept: application/json"

# Call the whitelisted method over REST
curl -X POST "https://mysite.local/api/method/my_app.stock.api.get_available_qty" \
  -H "Authorization: token <api_key>:<api_secret>" \
  -H "Content-Type: application/json" \
  -d '{"item_code": "SPICE-MIX-01", "warehouse": "Stores - NT"}'
```

`GET /api/resource/<DocType>` lists records, `GET .../<name>` reads one,
`POST` creates, `PUT` updates, `DELETE` deletes. Test a whitelisted method
from the bench without any HTTP at all:

```bash
bench --site mysite.local execute my_app.stock.api.get_available_qty \
  --args '["SPICE-MIX-01", "Stores - NT"]'
```

## When to use — and when not to

| Situation | Use |
|---|---|
| Logic for the document open on screen | `frm.call` to a controller method |
| Logic shared by several forms / DocTypes | Module-level `@frappe.whitelist()` + `frappe.call` |
| Another system reads or writes Frappe data | REST `/api/resource/...` with a dedicated API user |
| Another system needs one custom operation | REST `/api/method/...` to a whitelisted function |
| Anything that writes | `POST`, with `methods=["POST"]` on the decorator |
| Calling an external API from Frappe | `on_update` / `on_submit` + `frappe.enqueue`, with a timeout — never in `validate` |
| A guest (logged-out) user needs data | `allow_guest=True` only for reads, with input validation — never for writes |

## Common mistakes

- **No permission check.** A whitelisted method without
  `frappe.has_permission(..., throw=True)` (or `doc.check_permission`)
  hands data to anyone who can guess the URL.
- **Missing `@frappe.whitelist()`.** The call fails with 403 and the
  method works fine in Python — the decorator is what exposes it.
- **GET for a write.** State changes go through POST. A GET that writes
  can be triggered by a link, a prefetch, or a retry.
- **Administrator API keys.** Keys belong to a user, and that user has
  that user's roles. A dedicated API user with minimal roles limits the
  damage if a key leaks.
- **Secrets in JS or hardcoded.** API keys and passwords go in a Settings
  Single DocType with a Password field (`doc.get_password("api_key")`)
  or `frappe.conf` — never in client code.
- **No timeout on outbound calls.** `requests.post(url, json=...,
  timeout=30)`, wrapped in try/except, errors in `frappe.log_error`.
  A hung external API must never hang a save.
- **Returning whole documents** from an API. Return the fields the
  caller needs — a full doc leaks fields the caller should not see.

## Next

[08 — Reports & Print Formats](08-reports-print-formats.md) — Script
Reports, Query Reports, and Jinja print formats. Turning the data your
API just returned into something a manager can read.
