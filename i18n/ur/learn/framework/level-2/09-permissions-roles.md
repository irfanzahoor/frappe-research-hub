# 09 — Permissions & Roles

## Yeh kya hai

Access sirf tab milti hai jab **har** layer ijazat de. Chaar layers hain,
tarteeb mein — kisi bhi ek par fail hone ka matlab hai "nahi":

1. **Role permission** — ek role ek DocType par kya kar sakta hai (read,
   write, create, submit, cancel, print, export, report…).
2. **User Permission** — kaun se documents: ek user jo ek Company ya Branch
   tak mehdood hai, sirf us company ke records dekhta hai.
3. **Sharing** — ek document, ek user ke saath share, exception ke tor par.
4. **`has_permission` hook** — code jo ek document par faisla karta hai.

Desk aur `/api/resource/...` **wohni** checks chalate hain. Agar yeh Desk
mein kaam karta hai lekin API se fail hota hai, to API user (token owner)
ke paas woh role nahi hai.

## Minimal working example — Gate Pass access

**1. Role permissions** — Desk → **Role Permissions Manager**, DocType:
Gate Pass. Pehle DocType par **Is Submittable** set karein (Lesson 05),
phir:

| Role | Read | Write | Create | Submit | Cancel |
|---|---|---|---|---|---|
| Gate Security | ✓ | ✓ | ✓ | — | — |
| Store Manager | ✓ | ✓ | ✓ | ✓ | ✓ |
| Auditor | ✓ | — | — | — | — |

Jis role ke paas read permission nahi, woh DocType ko bilkul khol nahi
sakta — ek document share karne se yeh theek nahi hota.

**2. Field-level permission (permlevel).** `remarks` field mein internal
notes hain. DocType par iska **Permlevel** `1` par set karein, phir Role
Permissions Manager mein level 1 read sirf Store Manager ko dein. Gate
Security form dekhta hai — remarks field ke baghair.

**3. User Permission** — ek gate user sirf ek company dekhta hai:

```python
frappe.permissions.add_user_permission("Company", "NexTash Pvt Ltd", "gate.security@example.com")
```

Yeh lists, links aur reports ko filter karta hai. Ek user jise khaali list
nazar aati hai, aam tor par us ke paas User Permission hoti hai jo
documents chhupa rahi hoti hai, share ki kami nahi.

**4. Sharing** — ek document, ek user, exception ke tor par:

```python
frappe.share.add("Gate Pass", "GP-2026-0001", "auditor@example.com", read=1)
frappe.share.remove("Gate Pass", "GP-2026-0001", "auditor@example.com")
```

Sharing sirf us ek document tak access deti hai. Yeh role permission ki
jagah **nahi** leti — user ko DocType par read abhi bhi chahiye. Routine
access roles mein hoti hai, shares mein nahi.

Code mein waise hi check karein jaise framework karta hai:

```python
frappe.has_permission("Gate Pass", "read", doc, throw=True)
```

## Kab istemal karein — aur kab nahi

| Situation | Use |
|---|---|
| Ek poori team ko DocType chahiye | Role permission (Role Permissions Manager) |
| Ek user ko sirf ek Company / Branch dekhni chahiye | User Permission |
| Ek document ek bahar wale shakhs ko, ek dafa | Sharing |
| Ek rule jiska faisla code kare ("sirf owner, ya manager") | `has_permission` hook — v16 par yeh **explicit `True` return karna lazmi hai**; `None` return karne se access deny hoti hai |
| Ek field ko ek role se chhupana | permlevel — kabhi JS nahi |
| Ek report ya page sirf ek role ke liye | Page aur Report ke liye Role Permission |

## Aam ghaltiyan

- **Field ko JS mein chhupana security nahi hai.** Koi bhi field ko API
  ke zariye parh sakta hai. permlevel istemal karein.
- **Bina wajah `ignore_permissions=True`.** Agar aap yeh pass karein to
  wajah us ke saath wale comment mein likhein — warna agla developer isay
  har jagah copy karta rahega.
- **Kisi bhi cheez par `allow_guest=True` jo likhti ho.** Guest endpoints
  read-only hote hain, rate-limited hote hain, aur har input ko validate
  karna lazmi hai.
- **v16 par `has_permission` ka `None` return karna.** v14/v15 par `None`
  ka matlab tha "koi rai nahi"; v16 par yeh access deny kar deta hai.
  Explicit tor par `True` return karein.
- **Sharing ek role nahi hai.** Ek document share karne se sirf us ek
  document tak access milti hai. User ko DocType par read abhi bhi chahiye.
- **Whitelisted methods permission ko aakhir mein check karte hain.**
  Data return karne se *pehle* `frappe.has_permission(..., throw=True)`
  se check karein, baad mein nahi (Lesson 07).
- **User-facing reads ke liye `frappe.db.sql`.** Yeh har permission layer
  ko bypass karta hai. `frappe.get_list` / `frappe.get_all` istemal karein,
  jo User Permissions khud lagate hain.

**403? Is tarteeb mein check karein:** DocType par role permission →
User Permission jo document chhupa rahi hai → `has_permission` hook jo
`None` ya False return kar raha hai → whitelisted method jis mein decorator
ya check missing hai → API token ka user jis ke paas woh role nahi hai.

## Next

[10 — Workflows & Assignments](10-workflows-assignments.md) — approvals
aur automatic routing. Kaun document ko aage barha sakta hai, aur yeh kis
ke paas jata hai.
