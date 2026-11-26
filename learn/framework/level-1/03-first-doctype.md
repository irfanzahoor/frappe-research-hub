# 03 — Your First DocType

## What it is

A **DocType** is the definition of a record type. One definition gives you
five things at once: the database table, the form, the list view, the REST
API, and the permissions. If you can define a DocType well, you can build
most of Frappe.

Every DocType is a JSON file in your app:

```text
my_app/
  my_app/doctype/gate_pass/gate_pass.json   # the definition
  my_app/doctype/gate_pass/gate_pass.py     # server logic (controller)
  my_app/doctype/gate_pass/gate_pass.js     # form behaviour (UX only)
```

## Minimal working example — a Gate Pass

A factory needs a gate pass: who came, for which company, why, and what they
carried in or out. Create it in the UI first (**Desk → search "DocType" →
New**), with **Module** set to your app and `developer_mode` on, so the JSON
is saved into your app.

Fields — in this order:

| # | Fieldname | Label | Type | Notes |
|---|---|---|---|---|
| 1 | `naming_series` | Series | Select | Options: `GP-.YYYY.-.####` |
| 2 | `gate_pass_date` | Date | Date | Default: Today |
| 3 | `visitor_name` | Visitor | Data | Required |
| 4 | `company` | Company | Link | Options: Company |
| 5 | `purpose` | Purpose | Select | Visit / Delivery / Pickup |
| 6 | `section_break_1` | Details | Section Break | starts the items section |
| 7 | `items` | Items | Table | Options: Gate Pass Item |
| 8 | `remarks` | Remarks | Small Text | |

The child table **Gate Pass Item** (its own DocType, marked "Is Child Table"):

| Fieldname | Label | Type | Notes |
|---|---|---|---|
| `item_name` | Item | Data | In List View |
| `qty` | Qty | Int | In List View |
| `direction` | Direction | Select | In / Out |

Naming: set **Autoname** to `naming_series`. The first pass becomes
`GP-2026-0001`. If you leave Autoname blank, Frappe names records by a hash
nobody can read — always set it.

After creating it in the UI, apply it to the site:

```bash
bench --site mysite.local migrate
```

Then open **Gate Pass → New** in Desk and create one. You have just built a
working app screen with zero code.

## Field types you will use most

| Type | For | Example |
|---|---|---|
| Data | short text | visitor name |
| Link | a record in another DocType | Company, Customer, Item |
| Select | fixed list of options | purpose, status |
| Date / Datetime | dates | pass date, due date |
| Currency / Float / Int | numbers | amount, qty, rate |
| Check | yes/no | is active |
| Text / Small Text | longer text | remarks, address |
| Table | child rows | items, taxes |
| Attach / Attach Image | files | CNIC copy, photo |
| Section Break / Column Break / Tab Break | layout only | (no data stored) |

Rule of thumb: if the value must match a master record, use **Link**, never
free text. Free text for a company name means ten spellings of the same
company later.

## Layout rules — read these before adding any field

Bad field layout is the most common beginner mistake. These five rules come
from real projects (see `guides/common-mistakes.md`):

1. **Read the form first.** Open the existing form before adding a field.
   Add to the flow that is already there — do not bolt fields on at the end.
2. **Place with `insert_after`.** Every new field names the field it goes
   after. Fields without a position land at the bottom in a pile.
3. **Two fields per row.** A row is: field, **Column Break**, field, then a
   **Section Break** starts the next row. Never stack six fields in one
   column — the form becomes a long, unreadable scroll.
4. **A child table gets its own section.** Put a Section Break before it,
   with a clear label ("Items"). A table squeezed between two data fields
   looks broken and is easy to miss.
5. **Max 4–5 columns in List View.** Only tick `In List View` for the fields
   a user scans to find a record. Everything else belongs on the form.

Applied to the Gate Pass: Section 1 holds series, date, visitor, company,
purpose (two per row); Section 2 ("Items") holds only the table; remarks sit
in their own row at the end.

## When to use a DocType vs a Custom Field

- **New record type** (Gate Pass, Sample Request, Service Ticket) → new
  DocType in your app.
- **One extra field on someone else's DocType** (a "Transporter" field on
  Delivery Note) → Custom Field, exported as a fixture — never edit the
  other app's DocType JSON.
- **One-off field on your own DocType** → add it to the DocType, in the
  right position, following the five rules above.

## Common mistakes

- **No Section / Column Breaks.** One long column of 20 fields. Users hate
  it, and it is the first thing a reviewer will flag.
- **Free text where a Link belongs.** "Customer" as Data instead of Link to
  Customer — reports and filters break.
- **Child table without its own section.** It renders cramped and gets missed.
- **Everything `In List View`.** Ten columns in the list, half of them empty.
  Keep it to 4–5.
- **No naming series.** Records named by hash are unfindable on the phone.
- **Creating the DocType in the wrong module.** It lands in the wrong app and
  cannot be shipped. Set Module before you start.
- **Skipping `migrate`.** The DocType exists in the UI but the table is not
  created until you migrate.

## Next

[04 — Desk, List View, Form View](04-desk-list-form.md) — how users actually
work with the records you just defined.
