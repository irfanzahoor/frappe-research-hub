# 19 — Website & Portal

## Yeh kya hai

Frappe ke do chehre hain: **Desk** (internal app, logged-in users, roles) aur **Website** (public pages jinhein koi bhi khol sakta hai). Portal beech ka rasta hai — logged-in customers jo sirf apne documents dekhte hain. Teen building blocks:

| Block | For |
|---|---|
| **Web Page** | Ek static public page (About, Terms, ek landing page) |
| **Web Form** | Ek public form jo ek document banata hai — submit karne wale ko Desk access ki zaroorat nahi |
| **Portal** | Logged-in customers jo apne orders, invoices, tickets dekhte hain |

**Website Settings** (ek Single DocType) mein site-wide chrome hota hai: home page, brand, top navigation, footer. Aapki app ke `www/` folder mein pages seedha routes par map hote hain — `www/about.html`, `/about` hai — aur ek optional same-named `.py` file hoti hai jiska `get_context()` data deta hai.

## Minimal working example — ek "Request a Quote" Web Form

Desk → search **Web Form** → New:

| Field | Value |
|---|---|
| Title | Request a Quote |
| DocType | CRM Lead |
| Route | `request-quote` |

**Get Fields** par click karein taake fields CRM Lead se pull hon, name, company, email, phone aur requirements rakhein, email aur requirements mandatory bana dein, phir **Publish** karein. **See on Website** par click karein — form `/request-quote` par live hai. Har submission source "Web Form" ke saath ek CRM Lead banati hai (CRM app ka apna form builder bhi hai, Settings → Forms ke neeche, Lead/Deal capture ke liye).

Options jo jaanna zaroori hain: **Login Required** off ka matlab hai guests submit kar sakte hain — public form ke liye off rakhein, internal cheez ke liye on karein. **Allow Multiple** ek shakhs ko ek se zyada dafa submit karne deta hai. **Allow Edit** unhein apni submission baad mein edit karne deta hai. Bina rate limiting ke guest-facing form spam ka target hota hai — use simple rakhein, aur pehle submissions roz check karein.

## Minimal working example — ek customer portal page

ERPNext mein Sales Orders, Invoices aur tickets ke portal views pehle se mojood hain. Apna page add karne ke liye, use apni app ke `www/` folder mein rakhein — `my_app/www/my-orders.html`, `/my-orders` hai — ek controller `my_app/www/my-orders.py` ke saath:

```python
# my_app/www/my-orders.py
import frappe


def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("Please log in first"), frappe.PermissionError)
    # Contact has no direct customer field — the link lives in its
    # Dynamic Link child table (links), so resolve it in two steps.
    contact = frappe.db.get_value("Contact",
        {"user": frappe.session.user}, "name")
    customer = frappe.db.get_value("Dynamic Link",
        {"parenttype": "Contact", "parent": contact,
         "link_doctype": "Customer"}, "link_name") if contact else None
    if not customer:
        frappe.throw(_("No customer linked to your account"),
                     frappe.PermissionError)
    context.orders = frappe.get_list("Sales Order",
        filters={"customer": customer, "docstatus": 1},
        fields=["name", "transaction_date", "grand_total", "status"],
        order_by="transaction_date desc")
    return context
```

Context function hi access control hai: Guest ko bounce karein, logged-in user ke Contact se Customer resolve karein, aur query ko us customer tak scope karein. Page ko `hooks.py` mein `portal_menu_items` se portal menu mein add karein, role se gated.

## Kab istemal karein — aur kab nahi

| Situation | Use |
|---|---|
| Ek static public page (About, Terms) | Web Page DocType, ya `www/` HTML |
| External users se data entry | Web Form |
| Customers apne documents dekhte hain | Portal (built-in views, ya ek `www/` page) |
| Sidebar aur toolbar wala custom app | `www/` mein custom portal page |
| Blog aur shop wala poora public website | Frappe Website + Webshop — ya ek dedicated CMS, agar site hi product hai |
| Internal kaam | Desk — Desk screens ko kabhi public web par expose na karein |

## Common mistakes

- **Permissions test kiye baghair portal access.** Ek asal portal user ke tor par log in karein aur check karein ke woh sirf apne documents dekhta hai — ek portal login jo doosre customer ki invoices dekh sakta hai, woh data leak hai.
- **Bina checks ke Guest Web Form.** Public forms par spam aata hai. Fields minimal rakhein, email required karein, aur submissions roz review karein.
- **Web Form fieldnames jo DocType se match nahi karte.** Form fieldname se likhta hai — ek renamed field value ko khamoshi se drop kar deta hai.
- **Public page par internal logic rakhna.** Ek `www/` page visitor ki permissions ke saath chalta hai. Kabhi woh data na dikhayein jo visitor nahi dekh sakta, aur URL se aane wale kisi parameter par kabhi bharosa na karein.
- **Website Settings bhool jana.** Bina home page, brand aur navigation ke site adhoori lagti hai, forms kitne hi achhe kyun na hon.

## Next

[20 — Upgrades](20-upgrades.md) — ek live site ko v14 se v15 se v16 par le jana bina tode: lesson-length version, poora guide deep reference ke tor par.
