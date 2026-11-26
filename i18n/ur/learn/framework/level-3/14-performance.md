# 14 — Performance

## Yeh kya hai

Slow Frappe code taqreeban hamesha in chaar mein se ek cheez hota hai:
bohat zyada queries, ghalat query, koi index nahi, ya woh kaam jo request
mein ho raha hai jabke woh background job mein hona chahiye. Fixes
chhote aur mechanical hain — lekin sirf tab jab aap pehle measure karein.
Aisi report jo 30 seconds leti hai, us ki wajah mil sakti hai; andaze se
rewrite karna hi woh tareeqa hai jis se 30-second report 40-second
report ban jati hai.

## Minimal working example — N+1 query

Sab se bara. Loop ke andar ek value padhne ke liye kabhi `frappe.get_doc`
(ya `get_value`) na karein — yeh har row par ek database query hai.

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

Totals ke liye bhi wohi rule: SQL mein aggregate karein, rows ko Python
mein load na karein.

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

## Sahi read chunein

| Zaroorat | Use karein | Kyun |
|---|---|---|
| Ek document ka ek field | `frappe.db.get_value` | Ek sasti query |
| Kabhi kabhi badalne wala master (Company, settings) | `frappe.get_cached_value` / `frappe.get_cached_doc` | Redis se milta hai, koi query nahi |
| Aisi list jo user dekh sakta hai | `frappe.get_list` | Permission-aware — roles ka khayal rakhta hai |
| System code ke liye list | `frappe.get_all` | Tez hai, lekin **koi** permission check nahi |
| Sirf naam | `frappe.get_all(..., pluck="name")` | Koi dicts nahi bante |
| Count ya sum | `frappe.db.sql` / `frappe.qb` aggregate | DB aggregate karta hai, Python nahi |

`get_list` vs `get_all` speed jitna hi security ka faisla hai
(Lesson 15): `get_all` aisi rows bhi deta hai jinhe user dekhne ki
ijazat nahi rakhta. User-facing cheezon ke liye `get_list` use karein.

## Caching — jo kabhi kabhi badalta hai

Item groups, price lists, tax templates: taqreeban har document par
padhe jate hain, mahine mein ek baar badalte hain. Unhe generator ke
saath Redis mein cache karein — pehli call compute karti hai, baad wali
calls cache se padhti hain:

```python
def get_item_group(item_code):
    return frappe.cache().get_value(
        f"item_group:{item_code}",
        generator=lambda: frappe.db.get_value("Item", item_code, "item_group"),
    )
```

Rules: **shared, kabhi kabhi badalne wala** data cache karein, aisi key
ke saath jo bataye ke woh kya hai. Per-user data ko kabhi shared key ke
neeche cache na karein — agle user ko pehle user ka jawab milega.
Jab source badle to invalidate karein (DocType ke `on_update` mein key
clear karein), warna cache kal ki sachchai serve karta hai.

## Indexes

Bina index wale field par filter poori table ko scan karta hai. Frequent
filters mein use hone wale DocType fields par **Search Index** tick
karein — Stock Ledger Entry par `item_code`, Sales Order par `customer`,
Quality Inspection par `batch_no`. Index add karne se pehle slow query
ko MariaDB mein `EXPLAIN` se check karein; ghalat column par index koi
faida nahi deta aur writes ko slow kar deta hai.

## Reports aur denormalizing

Script Report jo 10,000 rows load kare aur Python mein filter kare, do
baar slow hoti hai: ek baar fetch karne mein, ek baar filter karne mein.
Query mein filter karein (`frappe.db.sql` ke saath `WHERE`, ya Query
Builder), sirf woh fields fetch karein jo report dikhati hai, aur
paginate karein.

Jab koi value har read par kai rows se compute hoti hai — customer ka
total outstanding, batch ki baqi qty — to **denormalize** karein: computed
value ko parent document par store karein aur jab children badlein to
usay update karein (controller mein, Lesson 05). Reads ek field lookup
ban jate hain. Is ki qeemat write complexity hai, is liye sirf un values
ko denormalize karein jo badalne se kahin zyada baar padhi jati hain.

## Kab use karein — aur kab nahi

| Situation | Use karein |
|---|---|
| Loop mein padhi jane wali value | Ek baar bulk fetch, phir dict lookup |
| Count, sum, ya average | SQL aggregate, Python nahi |
| Har document par padha jane wala master | `get_cached_value` / `frappe.cache()` |
| Slow report | SQL mein filter, sirf dikhaye gaye fields fetch karein |
| Chand seconds se zyada ka kaam | `frappe.enqueue` (Lesson 11) |
| Aisi value jo likhne se 100× zyada padhi jati hai | Parent par denormalize karein |
| One-off admin query | Slow theek hai — usay optimise na karein |

## Aam ghaltiyan

- **Loop mein `get_doc`.** Frappe apps mein sab se aam performance bug.
  Bulk fetch karein aur map karein.
- **User-facing reads ke liye `get_all`.** Tez hai — aur aisi rows leak
  kar deta hai jinhe user nahi dekhna chahiye. Users ke liye `get_list`,
  system code ke liye `get_all`.
- **Request ke andar `frappe.db.commit()`.** Framework commit karta
  hai. (Sirf lambe background jobs / patches mein, batches mein, allowed
  hai.)
- **`refresh` se server call karna** aise data ke liye jo kabhi kabhi
  badalta hai. `onload` mein ek baar load karein, ya controller se
  `frm.doc.__onload` set karein.
- **Filtered field par koi index nahi.** Query 100 rows par tez hoti hai
  aur 100,000 par marr jati hai. Client ke barhne se pehle `search_index`
  add karein.
- **Shared key ke neeche per-user data cache karna.** Har user ko pehle
  user ka data nazar aata hai. User se key banayein, ya cache na karein.
- **Measure kiye baghair optimise karna.** Pehle slow query dhoondhein
  (Error Log, `bench --site <site> console`, `EXPLAIN`), phir usay fix
  karein.

## Agla

[15 — Security](15-security.md) — woh cheezein jo kabhi nahi honi
chahiye: injection, leaked data, guest endpoints jo likhte hain, aur
code mein secrets.
