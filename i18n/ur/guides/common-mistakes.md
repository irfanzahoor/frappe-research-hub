# Aam Ghaltiyan — jo asal projects mein waqai hoti hain

Mukhtasar, concrete, NexTash ke asal kaam se. Har ghalti ke saath uska fix
bhi hai. Agar aap ko apna project kisi bhi section mein nazar aaye, to
pehle usi ko fix karein.

## 1. Kharab field layout

**Ghalti:** aik DocType jis mein 20 fields aik hi lambi column mein
stacked hon, na Section Breaks hon, na Column Breaks, aur har cheez par
"In List View" tick ho. Form aik aisi scroll ban jata hai jo koi nahi
parhta, aur list 12 columns chauri ho jati hai.

**Fix — paanch rules:**

1. **Pehle form parhein.** Field add karne se pehle maujooda form kholein.
   Jo flow pehle se hai, usi mein add karein.
2. **`insert_after` se place karein.** Har naya field us field ka naam
   bataye jis ke baad woh aaye. Jin fields ki koi position nahi hoti, woh
   neeche dher mein ja girti hain.
3. **Har row mein do fields.** Field, Column Break, field — phir Section
   Break se agli row shuru hoti hai.
4. **Child table ka apna section ho.** Us se pehle aik clear label
   ("Items") wala Section Break ho.
5. **List View mein zyada se zyada 4–5 columns.** Sirf woh fields jin ko
   dekh kar user record dhoondhta hai.

Kharab layout wale maujooda forms waisay hi rehne dein — ye rules aage
banne wale fields par lagte hain, purane forms ko dobara banane par nahi.

## 2. Hooks ghalat jagah par

**Ghalti:** business logic `hooks.py` ke andar likhi ho, apni app ke apne
DocType ke liye `doc_events`, ya aik `"*"` doc_event jo har DocType ke
har save par chale. Ya is se bhi bura: kisi behaviour ko badalne ke liye
ERPNext ki files ko seedha edit kar dena.

**Fix — placement ke rules:**

| Kya | Kahan jata hai |
|---|---|
| Apne DocType par logic | Us ka controller (`validate`, `on_submit`, …) |
| Doosri app ke DocType par logic | hooks.py mein `doc_events` → apni app mein aik override file |
| Doosri app ke DocType ke liye Form JS | `public/js/<name>.js` + hooks.py mein `doctype_js` |
| Custom Field / Property Setter | Fixtures, module se filter kar ke |

Aur sakht rules:

- **hooks.py aik registry hai, code file nahi.** Sirf dotted paths, koi logic nahi.
- **Kabhi doosri app ki files edit na karein.** "Sirf aik chhoti line" bhi nahi. Apni app se extend karein, warna agli update usay mita degi.
- **Kabhi `"*"` doc_events nahi** jab tak logic waqai har DocType par
  lagoo na hota ho — woh har save par, har jagah, hamesha chalta hai.
- **Aik hi DocType ke liye duplicate `frappe.ui.form.on` blocks nahi** — maujooda handler ko extend karein.
- **Validation server par karein.** JS sirf UX ke liye hai. Jo rule sirf JS mein enforce ho, woh rule hi nahi — API usay bypass kar deti hai.

```python
# hooks.py — registry only
doc_events = {
    "Sales Invoice": {
        "validate": "my_app.selling.overrides.sales_invoice.validate",
    },
}
```

## 3. Permissions ki ghaltiyan

**Ghalti:** users jo apne documents dekh nahi sakte, ya users jo sab
kuch dekh sakte hain. Dono aam tor par wohi teen ghaltiyan hoti hain.

**Fix:**

- **JS mein field chhupana security nahi hai.** Koi bhi field ko API se
  parh sakta hai. Is ke bajaye **permlevel** (field-level permission)
  use karein.
- **Bina wajah `ignore_permissions=True`.** Agar aap ye pass karte hain,
  to us ke saath aik comment mein wajah likhein. Warna agla developer
  isay har jagah copy kar lega.
- **`allow_guest=True` kisi bhi cheez par jo write karti ho.** Guest
  endpoints read-only hote hain, rate-limited hote hain, aur har input
  ko validate karna zaroori hota hai.
- **v16: `has_permission` ko saaf `True` return karna hota hai.** `None`
  return karna ab access deny kar deta hai (v14/v15 mein `None` ka
  matlab tha "koi raye nahi"). Jo hook `True` return karna bhool jaye,
  woh sab ko lock out kar deta hai.
- **Sharing aik role nahi hai.** Aik document share karne se sirf us aik
  document tak access milti hai — user ko DocType par read permission
  phir bhi chahiye hoti hai. Jo user khaali list dekhta hai, us ke
  documents aam tor par User Permission (Company, Branch) chhupa rahi
  hoti hai, koi missing share nahi.
- **Whitelisted methods pehle permission check karte hain.** Data return
  karne se *pehle* `frappe.has_permission(..., throw=True)` se check
  karein, baad mein nahi. Jo method `@frappe.whitelist()` ke baghair ho,
  usay form ya API se bilkul call nahi kiya ja sakta (403).

**403? Is order mein check karein:** DocType par role permission → User
Permission jo document chhupa rahi ho → `has_permission` hook jo `None`
ya False return kar raha ho → whitelisted method jis mein decorator ya
check missing ho → API token ka user jis ke paas role na ho.

## 4. Performance ki ghaltiyan

**Ghalti:** aik report ya submit jo 30 seconds le, aam tor par in mein
se aik wajah se.

**Fix:**

**N+1 queries — sab se bari wajah.** Loop ke andar aik value parhne ke
liye kabhi `frappe.get_doc` na karein.

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

- **Sahi read use karein.** Aik field ke liye `frappe.db.get_value` /
  `frappe.get_cached_value` — `get_doc` nahi. Aggregates SQL mein karein,
  rows ko Python mein load kar ke nahi.
- **Frequent filters mein use hone wale fields par `search_index` lagayein.**
- **Request ke andar kabhi `frappe.db.commit()` na karein.** Framework
  commit karta hai. (Sirf lambe background jobs / patches mein allowed
  hai, batches mein.)
- **Slow kaam background job mein bhejein.** Kuch seconds se zyada ka
  kaam — bulk processing, bulk email, external APIs, bari reports —
  `frappe.enqueue(..., queue="long")` se jata hai, aur user ko
  completion par notify kiya jata hai.
- **`refresh` se server ko us data ke liye call na karein jo kabhi-kabhi
  badalta ho.** Aik dafa `onload` mein load karein, ya controller se
  `frm.doc.__onload` set karein.

## 5. Ledger aur stock — na-qabil-e-maafi ghaltiyan

- **Kabhi GL Entry ya Stock Ledger Entry seedha insert na karein.** Ye
  submit par automatically banti hain. Agar koi posting missing hai, to
  document ghalat hai — document ko fix karein.
- **Submitted document ke fields kabhi edit na karein.** Cancel karein
  aur amend karein. Edited submitted document aur us ka ledger hamesha
  ke liye disagree karte hain.
- **Bin ko haath se kabhi edit na karein.** Balance ghalat hai? Stock
  Reconciliation karein, posting date aur reason ke saath.

## Pre-ship checklist

Kisi bhi custom app ke client ke paas jane se pehle, check karein:

- [ ] Har naya field `insert_after` se place ho, har row mein 2, child tables apne section mein, ≤ 5 list columns
- [ ] hooks.py mein koi logic nahi; koi `"*"` doc_events nahi; doosri apps mein koi edit nahi
- [ ] Validation server par ho, sirf JS mein nahi
- [ ] Bina comment ke koi `ignore_permissions=True` nahi; koi `allow_guest` writes nahi
- [ ] Loop mein koi `get_doc` nahi; slow kaam enqueue ho
- [ ] Haath se likhi koi GL / SLE rows nahi; submitted documents mein koi edit nahi
- [ ] `bench --site <site> migrate` run ho, aur us se pehle backup liya gaya ho

## Sources

Deep reference: [frappe_core_skills](https://github.com/irfanzahoor/frappe_core_skills)
— frappe-core (placement, review checklist), frappe-permissions,
frappe-performance, frappe-ui (field layout).
