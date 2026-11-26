# 07 — APIs

## Yeh kya hai

Har DocType ki API pehle se maujood hai — form, list aur REST API, sab ke
neeche wohi server hai. Isay call karne ke teen tareeqe hain:

| Tareeqa | Kahan se | Kis ke liye |
|---|---|---|
| `frm.call("method")` | Khula hua form | Maujooda document ke controller ka method |
| `frappe.call({ method: "app.module.file.fn" })` | Koi bhi form JS | Module-level whitelisted function |
| REST: `/api/resource/...`, `/api/method/...` | Koi bhi system, curl, Postman | Doosri apps aur integrations |

Python function bahar se call tab hi ho sakti hai jab us par
`@frappe.whitelist()` laga ho. Decorator ke baghair, call 403 hoti hai. Aur har
whitelisted function ek public endpoint hai — usay data return karne se pehle
permissions check karni chahiye, baad mein nahi.

## Chhoti si working example — available stock check karein

Aap ki app mein ek whitelisted function:

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

Sales Order form se isay call karein — ek "Check Stock" button:

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

Wohi logic Frappe ke bahar se, REST par call karein. Pehle minimal roles wala
**dedicated API user** banayein (kabhi Administrator keys use na karein),
phir us ki keys generate karein (User → API Access → Generate Keys):

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

`GET /api/resource/<DocType>` records list karta hai, `GET .../<name>` ek
record parhta hai, `POST` banata hai, `PUT` update karta hai, `DELETE` delete
karta hai. Bina kisi HTTP ke, bench se whitelisted method test karein:

```bash
bench --site mysite.local execute my_app.stock.api.get_available_qty \
  --args '["SPICE-MIX-01", "Stores - NT"]'
```

## Kab use karein — aur kab nahi

| Situation | Use karein |
|---|---|
| Screen par khule hue document ke liye logic | Controller method par `frm.call` |
| Kai forms / DocTypes mein shared logic | Module-level `@frappe.whitelist()` + `frappe.call` |
| Doosra system Frappe data parhe ya likhe | Dedicated API user ke saath REST `/api/resource/...` |
| Doosre system ko ek custom operation chahiye | Whitelisted function par REST `/api/method/...` |
| Koi bhi cheez jo likhti hai | `POST`, decorator par `methods=["POST"]` ke saath |
| Frappe se external API call karna | Timeout ke saath `on_update` / `on_submit` + `frappe.enqueue` — kabhi `validate` mein nahi |
| Guest (logged-out) user ko data chahiye | Sirf reads ke liye `allow_guest=True`, input validation ke saath — writes ke liye kabhi nahi |

## Aam ghaltiyan

- **Permission check nahi.** Whitelisted method jis mein
  `frappe.has_permission(..., throw=True)` (ya `doc.check_permission`)
  nahi hai, woh data usay bhi de deti hai jo URL guess kar le.
- **`@frappe.whitelist()` missing.** Call 403 par fail hoti hai aur
  method Python mein theek kaam karta hai — decorator hi isay expose
  karta hai.
- **Write ke liye GET.** State changes POST se hoti hain. GET jo likhta
  hai, woh link, prefetch, ya retry se trigger ho sakta hai.
- **Administrator API keys.** Keys user ki hoti hain, aur us user ke wohi
  roles hote hain jo us ke paas hain. Minimal roles wala dedicated API user
  nuqsan limit karta hai agar key leak ho jaye.
- **Secrets JS mein ya hardcoded.** API keys aur passwords Settings
  Single DocType mein Password field ke saath
  (`doc.get_password("api_key")`) ya `frappe.conf` mein jate hain — kabhi
  client code mein nahi.
- **Outbound calls par timeout nahi.** `requests.post(url, json=...,
  timeout=30)`, try/except mein wrapped, errors `frappe.log_error` mein.
  Latka hua external API kabhi save ko nahi latkana chahiye.
- **API se poore documents return karna.** Wohi fields return karein jo
  caller ko chahiye — poora doc woh fields bhi leak kar deta hai jo caller
  ko nahi dekhne chahiye.

## Agla

[08 — Reports & Print Formats](08-reports-print-formats.md) — Script
Reports, Query Reports, aur Jinja print formats. Jo data aap ki API ne
abhi return kiya hai, usay aisi cheez mein badalna jo manager parh sake.
