# Common Mistakes — the ones real projects actually make

Short, concrete, from real NexTash work. Each mistake has the fix. If you
recognise your own project in any section, fix that one first.

## 1. Bad field layout

**The mistake:** a DocType with 20 fields stacked in one long column, no
Section Breaks, no Column Breaks, and everything ticked "In List View". The
form is a scroll nobody reads, and the list is 12 columns wide.

**The fix — five rules:**

1. **Read the form first.** Open the existing form before adding a field.
   Add to the flow that is already there.
2. **Place with `insert_after`.** Every new field names the field it goes
   after. Fields without a position land at the bottom in a pile.
3. **Two fields per row.** Field, Column Break, field — then a Section Break
   starts the next row.
4. **A child table gets its own section.** Section Break with a clear label
   ("Items") before it.
5. **Max 4–5 columns in List View.** Only the fields a user scans to find a
   record.

Existing forms with bad layout are left as-is — these rules apply to fields
created going forward, not to rebuilding old forms.

## 2. Hooks in the wrong place

**The mistake:** business logic written inside `hooks.py`, `doc_events` for
a DocType your own app owns, or a `"*"` doc_event that runs on every save of
every DocType. Or worse: editing ERPNext's files directly to change a
behaviour.

**The fix — the placement rules:**

| What | Where it goes |
|---|---|
| Logic on your own DocType | Its controller (`validate`, `on_submit`, …) |
| Logic on another app's DocType | `doc_events` in hooks.py → an override file in your app |
| Form JS for another app's DocType | `public/js/<name>.js` + `doctype_js` in hooks.py |
| Custom Field / Property Setter | Fixtures, filtered by module |

And the hard rules:

- **hooks.py is a registry, not a code file.** Only dotted paths, no logic.
- **Never edit another app's files.** Not even "one small line". Extend from
  your app, or the next update wipes it.
- **Never `"*"` doc_events** unless the logic truly applies to every
  DocType — it runs on every save, everywhere, forever.
- **No duplicate `frappe.ui.form.on` blocks** for the same DocType — extend
  the existing handler.
- **Validation on the server.** JS is UX only. A rule enforced in JS alone
  is not a rule — the API bypasses it.

```python
# hooks.py — registry only
doc_events = {
    "Sales Invoice": {
        "validate": "my_app.selling.overrides.sales_invoice.validate",
    },
}
```

## 3. Permission mistakes

**The mistake:** users who cannot see their own documents, or users who can
see everything. Both are usually the same three errors.

**The fix:**

- **Hiding a field in JS is not security.** Anyone can read the field
  through the API. Use **permlevel** (field-level permission) instead.
- **`ignore_permissions=True` without a reason.** If you pass it, write the
  reason in a comment next to it. Otherwise the next developer copies it
  everywhere.
- **`allow_guest=True` on anything that writes.** Guest endpoints are
  read-only, rate-limited, and must validate every input.
- **v16: `has_permission` must return an explicit `True`.** Returning `None`
  now denies access (on v14/v15, `None` meant "no opinion"). A hook that
  forgets to return `True` locks everyone out.
- **Sharing is not a role.** Sharing one document gives access to that one
  document only — the user still needs read permission on the DocType. A
  user who sees an empty list usually has a User Permission (Company,
  Branch) hiding the documents, not a missing share.
- **Whitelisted methods check permission first.** Check with
  `frappe.has_permission(..., throw=True)` *before* returning data, not
  after. A method without `@frappe.whitelist()` cannot be called from a
  form or the API at all (403).

**403? Check in this order:** role permission on the DocType → User
Permission hiding the document → `has_permission` hook returning `None` or
False → whitelisted method missing the decorator or the check → the API
token's user lacking the role.

## 4. Performance mistakes

**The mistake:** a report or a submit that takes 30 seconds, usually for one
of four reasons.

**The fix:**

**N+1 queries — the big one.** Never `frappe.get_doc` inside a loop to read
one value.

```python
# ❌ one query per row
for row in self.items:
    group = frappe.db.get_value("Item", row.item_code, "item_group")

# ✅ one query, then a dict lookup
item_codes = [row.item_code for row in self.items]
groups = dict(frappe.get_all("Item",
    filters={"name": ("in", item_codes)},
    fields=["name", "item_group"], as_list=True))
for row in self.items:
    group = groups.get(row.item_code)
```

- **Use the right read.** `frappe.db.get_value` / `frappe.get_cached_value`
  for one field — not `get_doc`. Aggregates in SQL, not by loading rows
  into Python.
- **Add `search_index`** on fields used in frequent filters.
- **Never `frappe.db.commit()` inside a request.** The framework commits.
  (Allowed only in long background jobs / patches, in batches.)
- **Slow work goes to a background job.** Anything over a few seconds —
  bulk processing, bulk email, external APIs, big reports — goes through
  `frappe.enqueue(..., queue="long")`, and the user is notified on
  completion.
- **Do not call the server from `refresh` for data that rarely changes.**
  Load once in `onload`, or set `frm.doc.__onload` from the controller.

## 5. Ledger and stock — the unforgivable ones

- **Never insert GL Entry or Stock Ledger Entry directly.** They are created
  automatically on submit. If a posting is missing, the document is wrong —
  fix the document.
- **Never edit a submitted document's fields.** Cancel and amend. An edited
  submitted document and its ledger disagree forever.
- **Never edit Bin by hand.** Wrong balance? Stock Reconciliation, with a
  posting date and a reason.

## Pre-ship checklist

Before any custom app goes to a client, check:

- [ ] Every new field placed with `insert_after`, 2 per row, child tables in
  their own section, ≤ 5 list columns
- [ ] No logic in hooks.py; no `"*"` doc_events; no edits to other apps
- [ ] Validation on the server, not only in JS
- [ ] No `ignore_permissions=True` without a comment; no `allow_guest` writes
- [ ] No `get_doc` in a loop; slow work enqueued
- [ ] No hand-written GL / SLE rows; no edits to submitted documents
- [ ] `bench --site <site> migrate` run, and a backup taken before it

## Sources

Deep reference: [frappe_core_skills](https://github.com/irfanzahoor/frappe_core_skills)
— frappe-core (placement, review checklist), frappe-permissions,
frappe-performance, frappe-ui (field layout).
