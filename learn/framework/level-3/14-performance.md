# 14 — Performance

## What it is

Slow Frappe code is almost always one of four things: too many queries,
the wrong query, no index, or work done in the request that belongs in a
background job. The fixes are small and mechanical — but only if you
measure first. A report that takes 30 seconds has a cause you can find;
guessing rewrites is how a 30-second report becomes a 40-second report.

## Minimal working example — the N+1 query

The big one. Never `frappe.get_doc` (or `get_value`) inside a loop to
read one value — that is one database query per row.

```python
# ❌ 200 items = 200 queries
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

Same rule for totals: aggregate in SQL, don't load rows into Python.

```python
# ❌ loads every Stock Ledger Entry row
total = sum(e.actual_qty for e in frappe.get_all("Stock Ledger Entry",
    filters={"item_code": item_code}, fields=["actual_qty"]))

# ✅ the database sums
total = frappe.db.sql("""
    SELECT SUM(actual_qty) FROM `tabStock Ledger Entry`
    WHERE item_code = %s
""", item_code)[0][0] or 0
```

## Pick the right read

| Need | Use | Why |
|---|---|---|
| One field of one document | `frappe.db.get_value` | One cheap query |
| A rarely-changing master (Company, settings) | `frappe.get_cached_value` / `frappe.get_cached_doc` | Served from Redis, no query |
| A list the user may see | `frappe.get_list` | Permission-aware — respects roles |
| A list for system code | `frappe.get_all` | Faster, but **no** permission check |
| Just the names | `frappe.get_all(..., pluck="name")` | No dicts built |
| A count or sum | `frappe.db.sql` / `frappe.qb` aggregate | The DB aggregates, Python doesn't |

`get_list` vs `get_all` is a security decision as much as a speed one
(Lesson 15): `get_all` returns rows the user is not allowed to see. Use
`get_list` for anything user-facing.

## Caching — what rarely changes

Item groups, price lists, tax templates: read on almost every document,
changed once a month. Cache them in Redis with a generator — the first
call computes, later calls read the cache:

```python
def get_item_group(item_code):
    return frappe.cache().get_value(
        f"item_group:{item_code}",
        generator=lambda: frappe.db.get_value("Item", item_code, "item_group"),
    )
```

Rules: cache **shared, rarely-changing** data under a key that names what
it is. Never cache per-user data under a shared key — the next user gets
the first user's answer. Invalidate when the source changes (clear the
key in the DocType's `on_update`), or the cache serves yesterday's truth.

## Indexes

A filter on a field without an index scans the whole table. Tick **Search
Index** on DocType fields used in frequent filters — `item_code` on Stock
Ledger Entry, `customer` on Sales Order, `batch_no` on Quality
Inspection. Check a slow query with `EXPLAIN` in MariaDB before adding
an index; an index on the wrong column helps nothing and slows writes.

## Reports and denormalizing

A Script Report that loads 10,000 rows and filters in Python is slow
twice: once to fetch, once to filter. Filter in the query
(`frappe.db.sql` with `WHERE`, or Query Builder), fetch only the fields
the report shows, and paginate.

When a value is computed from many rows on every read — a customer's
total outstanding, a batch's remaining qty — **denormalize**: store the
computed value on the parent document and update it when the children
change (in the controller, Lesson 05). Reads become one field lookup.
The price is write complexity, so denormalize only values that are read
far more often than they change.

## When to use — and when not to

| Situation | Use |
|---|---|
| A value read in a loop | Bulk fetch once, dict lookup |
| A count, sum, or average | SQL aggregate, not Python |
| A master read on every document | `get_cached_value` / `frappe.cache()` |
| A slow report | Filter in SQL, fetch only shown fields |
| Work over a few seconds | `frappe.enqueue` (Lesson 11) |
| A value read 100× more than written | Denormalize onto the parent |
| A one-off admin query | Slow is fine — don't optimise it |

## Common mistakes

- **`get_doc` in a loop.** The single most common performance bug in
  Frappe apps. Bulk fetch and map.
- **`get_all` for user-facing reads.** Fast — and leaks rows the user
  must not see. `get_list` for users, `get_all` for system code.
- **`frappe.db.commit()` inside a request.** The framework commits.
  (Allowed only in long background jobs / patches, in batches.)
- **Calling the server from `refresh`** for data that rarely changes.
  Load once in `onload`, or set `frm.doc.__onload` from the controller.
- **No index on the filtered field.** The query is fast on 100 rows and
  dead on 100,000. Add `search_index` before the client grows.
- **Caching per-user data under a shared key.** Every user sees the
  first user's data. Key by user, or don't cache it.
- **Optimising without measuring.** Find the slow query first
  (Error Log, `bench --site <site> console`, `EXPLAIN`), then fix it.

## Next

[15 — Security](15-security.md) — the things that must never happen:
injection, leaked data, guest endpoints that write, and secrets in code.
