# 19 — Website & Portal

## What it is

Frappe has two faces: **Desk** (the internal app, logged-in users,
roles) and the **Website** (public pages anyone can open). The portal
is the middle ground — logged-in customers who see only their own
documents. Three building blocks:

| Block | For |
|---|---|
| **Web Page** | A static public page (About, Terms, a landing page) |
| **Web Form** | A public form that creates a document — no Desk access for the submitter |
| **Portal** | Logged-in customers seeing their own orders, invoices, tickets |

**Website Settings** (a Single DocType) holds the site-wide chrome:
home page, brand, top navigation, footer. Pages in your app's `www/`
folder map directly to routes — `www/about.html` is `/about` — with
an optional same-named `.py` file whose `get_context()` supplies the
data.

## Minimal working example — a "Request a Quote" Web Form

Desk → search **Web Form** → New:

| Field | Value |
|---|---|
| Title | Request a Quote |
| DocType | CRM Lead |
| Route | `request-quote` |

Click **Get Fields** to pull the fields from CRM Lead, keep name,
company, email, phone and requirements, make email and requirements
mandatory, then **Publish**. Click **See on Website** — the form is
live at `/request-quote`. Every submission creates a CRM Lead with
source "Web Form" (the CRM app also has its own form builder under
Settings → Forms, for Lead/Deal capture).

Options to know: **Login Required** off means guests can submit —
keep it off for a public form, on for anything internal. **Allow
Multiple** lets one person submit more than once. **Allow Edit** lets
them edit their submission later. A guest-facing form with no rate
limiting is a spam target — keep it simple, and check submissions
daily at first.

## Minimal working example — a customer portal page

ERPNext already ships portal views for Sales Orders, Invoices and
tickets. To add your own page, put it in your app's `www/` folder —
`my_app/www/my-orders.html` is `/my-orders` — with a controller
`my_app/www/my-orders.py`:

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

The context function is the access control: bounce Guest, resolve
the Customer from the logged-in user's Contact, and scope the query
to that customer. Add the page to the portal menu with
`portal_menu_items` in `hooks.py`, gated by role.

## When to use — and when not to

| Situation | Use |
|---|---|
| A static public page (About, Terms) | Web Page DocType, or `www/` HTML |
| Data entry by external users | Web Form |
| Customers seeing their own documents | Portal (built-in views, or a `www/` page) |
| A custom app with sidebar and toolbar | Custom portal page in `www/` |
| A full public website with blog and shop | Frappe Website + Webshop — or a dedicated CMS, if the site is the product |
| Internal work | Desk — never expose Desk screens to the public web |

## Common mistakes

- **Portal access without testing permissions.** Log in as a real
  portal user and check they see only their own documents — a portal
  login that can see another customer's invoices is a data leak.
- **Guest Web Form with no checks.** Public forms get spam. Keep the
  fields minimal, require an email, and review submissions daily.
- **Web Form fieldnames that do not match the DocType.** The form
  writes by fieldname — a renamed field silently drops the value.
- **Putting internal logic on a public page.** A `www/` page runs
  with the visitor's permissions. Never show data the visitor may
  not see, and never trust a parameter from the URL.
- **Forgetting Website Settings.** A site with no home page, no brand
  and no navigation looks unfinished, however good the forms are.

## Next

[20 — Upgrades](20-upgrades.md) — moving a live site from v14 to v15
to v16 without breaking it: the lesson-length version, with the full
guide as the deep reference.
