# 01 — Frappe Kya Hai: Framework vs ERPNext vs Frappe Cloud

## Yeh kya hai

Teen alag cheezein ek hi naam "Frappe" share karti hain. In ko aapas mein
mila dena woh pehli ghalti hai jo aksar beginners karte hain.

**Frappe Framework — platform.** Python aur JavaScript mein aik full-stack
web framework, MariaDB, Redis aur Node.js par. Yeh aap ko, box se bahar hi,
yeh sab deta hai:

- **DocTypes** — aik definition jo database table, form, list view, API
  aur permissions bana deti hai.
- **Desk** — admin UI jis mein aap ke users har roz kaam karte hain.
- **REST API, background jobs, scheduler, workflows, reports, print formats,
  email aur notifications** — sab built-in hain, koi extra libraries jorne
  ki zaroorat nahi.

Framework MIT-licensed hai aur open source hai. Current version: **v16**,
monthly releases ke saath (16.60, 16.61, …). v16.60 se, Studio (no-code app
builder) aur Flow (Desk mein AI) Framework ke andar hi aate hain.

**ERPNext — Frappe par bana hua business app.** Accounting, Stock, Selling,
Buying, Manufacturing, HR, CRM, Projects, Assets, Helpdesk. Yeh *aik app*
hai jo aik Frappe site par chalta hai, bilkul usi tarah jaise aap ka apna
custom app chalta hai. GPL-3.0 licensed hai. Jab koi kehta hai "hum ERPNext
chalate hain", to us ka matlab hai aik Frappe site jis par ERPNext app
install hai.

**Frappe Cloud — hosted Frappe.** Aap ki sites Frappe ki infrastructure par
chalti hain. Aap dashboard se Git repo se custom apps deploy karte hain.
Is mein shell access nahi hai, aur shared benches par Server Scripts bhi
nahi hain. Aap control ke badle mein zero server work lete hain.

Doosri Frappe apps bhi isi pattern par chalti hain: HRMS, CRM, Helpdesk,
Insights, Raven, Builder, Wiki, Drive — har aik aik app hai jo aap site
par install karte hain.

> Aik line mein mental model: **Framework engine hai, ERPNext us par bani
> hui gaari hai, Frappe Cloud driver ke saath gaari kiraye par lena hai.**

## Yeh pieces aapas mein kaise fit hote hain

```text
bench  (a folder on your machine or server)
 ├── apps/      frappe, erpnext, my_app, hrms, ...
 └── sites/     site1.local, client-a.com, ...
                 └── each site = one database + files
```

Aik bench mein kai sites hoti hain. Aik site par kai apps chalte hain. Aik
document (aik Sales Order, aik Employee, aik custom record) hamesha aik hi
site se belong karta hai.

## Kis cheez ko kab use karein

| Goal | Use |
|---|---|
| Seekhna hai, ya custom app banana hai | Local bench par Framework |
| Business ko end to end chalana hai | ERPNext (Cloud ya self-hosted) |
| Client ko zero server work chahiye | Frappe Cloud |
| Shell access, custom infra, local-only data rules chahiye | Self-hosted bench |
| Bechne ke liye product banana hai | Framework par custom app (agar ERP ko extend kare to ERPNext bhi) |
| Aik client ke liye jaldi prototype banana hai | Code likhne se pehle Framework + Studio (v16.60+) |

## Chhoti si misaal — khud dekh lein

Aik bench par jis par ERPNext pehle se install hai:

```bash
bench --version        # the bench CLI version
bench list-apps        # apps on this bench: frappe, erpnext, ...
bench --site mysite.local list-apps   # apps installed on one site
```

Phir `http://mysite.local:8000` kholein aur Administrator ke tor par sign in
karein:

- Upar wale search bar mein **"Company"** search karein — yeh aik ERPNext
  DocType hai.
- **"DocType"** search karein — yeh Framework ki apni DocTypes ki list hai.
- **"Sales Invoice"** search karein — yeh phir ERPNext hai. Har screen jo
  aap dekhte hain, woh aik DocType hai jo Framework render karta hai.

## Aam ghaltiyan

- **Yeh samajhna ke ERPNext hi Frappe hai.** ERPNext aik app hai. Framework
  woh platform hai jis par sab kuch chalta hai. Aap Frappe bilkul ERPNext
  ke baghair bhi chala sakte hain.
- **ERPNext ki files ko seedha edit karna.** Kabhi doosri app ka code edit
  na karein. Usay apni app se hooks, overrides aur fixtures ke zariye
  extend karein.
- **Aik chhote client ke liye self-hosting karna jise sirf ERPNext
  chahiye.** Aik server plus aap ka maintenance time, aksar chhoti sites
  ke liye Frappe Cloud se zyada kharcha karta hai.
- **Cloud chunna jab client ko shell-level kaam chahiye** — custom system
  packages, local-only data, ya direct database access. Cloud mein shell
  nahi hai.
- **Code se shuru karna, yeh check kiye baghair ke kya pehle se mojood
  hai.** ERPNext, HRMS, CRM aur Apps Catalog pehle se aksar requirements
  hal kar chuke hote hain. Sirf gap banayein.

## Ahem terms — yeh yaad rakhein

- **DocType** — record type ki definition (table + form + list + rules).
- **Document** — aik record (aik Sales Order, aik Employee).
- **Desk** — web UI.
- **bench** — CLI aur folder jo apps aur sites ko sambhalta hai.
- **site** — aik database + installed apps ka aik set.
- **app** — DocTypes, code aur fixtures ka aik package (frappe, erpnext,
  aap ka apna).
- **docstatus** — 0 Draft, 1 Submitted, 2 Cancelled. Aap ko yeh har ERPNext
  lesson mein milega.

## Next

[02 — Bench, sites aur apps](02-bench-sites-apps.md) — isay install karein
aur apni pehli site aur app banayein.
