# 03 — Apna Pehla DocType

## Yeh kya hai

Aik **DocType** record type ki definition hai. Aik definition aap ko aik
saath paanch cheezein deti hai: database table, form, list view, REST API,
aur permissions. Agar aap DocType achhi tarah define kar sakte hain, to aap
Frappe ka zyada tar hissa bana sakte hain.

Har DocType aap ki app mein aik JSON file hai:

```text
my_app/
  my_app/doctype/gate_pass/gate_pass.json   # the definition
  my_app/doctype/gate_pass/gate_pass.py     # server logic (controller)
  my_app/doctype/gate_pass/gate_pass.js     # form behaviour (UX only)
```

## Chhoti si working misaal — aik Gate Pass

Aik factory ko gate pass chahiye: kaun aaya, kis company ke liye, kyun, aur
kya andar ya bahar le gaya. Isay pehle UI mein banayein (**Desk → search
"DocType" → New**), **Module** apni app par set kar ke aur `developer_mode`
on kar ke, taake JSON aap ki app mein save ho.

Fields — isi order mein:

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

Child table **Gate Pass Item** (apni DocType, "Is Child Table" mark ki hui):

| Fieldname | Label | Type | Notes |
|---|---|---|---|
| `item_name` | Item | Data | In List View |
| `qty` | Qty | Int | In List View |
| `direction` | Direction | Select | In / Out |

Naming: **Autoname** ko `naming_series` par set karein. Pehla pass
`GP-2026-0001` ban jata hai. Agar aap Autoname khali chhor dein, to Frappe
records ko aik hash se naam deta hai jise koi parh nahi sakta — hamesha isay
set karein.

UI mein banane ke baad, isay site par apply karein:

```bash
bench --site mysite.local migrate
```

Phir Desk mein **Gate Pass → New** kholein aur aik banayein. Aap ne abhi
zero code ke saath aik working app screen bana li hai.

## Field types jo aap sab se zyada use karein ge

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

Aam usool: agar value kisi master record se match honi chahiye, to **Link**
use karein, kabhi free text nahi. Company ke naam ke liye free text ka
matlab hai baad mein aik hi company ki das spellings.

## Layout rules — koi bhi field add karne se pehle yeh parhein

Kharab field layout sab se aam beginner ghalti hai. Yeh paanch rules asal
projects se aaye hain (dekhein `guides/common-mistakes.md`):

1. **Pehle form ko parhein.** Field add karne se pehle mojooda form kholein.
   Us flow mein add karein jo pehle se hai — fields ko end par bolt-on na
   karein.
2. **Position `insert_after` se dein.** Har naya field us field ka naam deta
   hai jis ke baad woh aata hai. Position ke baghair fields neeche aik dher
   mein aa jate hain.
3. **Har row mein do fields.** Aik row yeh hai: field, **Column Break**,
   field, phir aik **Section Break** agle row ko shuru karta hai. Kabhi aik
   column mein chhe fields stack na karein — form aik lambi, na parhne
   wali scroll ban jata hai.
4. **Child table ko apna section mile.** Us se pehle Section Break lagayein,
   saaf label ke saath ("Items"). Do data fields ke beech dabbi hui table
   tooti hui lagti hai aur aasani se miss ho jati hai.
5. **List View mein max 4–5 columns.** Sirf un fields par `In List View`
   tick karein jin ko user record dhoondne ke liye scan karta hai. Baaki sab
   form par hai.

Gate Pass par apply karein: Section 1 mein series, date, visitor, company,
purpose hain (har row mein do); Section 2 ("Items") mein sirf table hai;
remarks end par apni row mein hain.

## DocType kab use karein vs Custom Field

- **Naya record type** (Gate Pass, Sample Request, Service Ticket) → apni
  app mein naya DocType.
- **Kisi aur ke DocType par aik extra field** (Delivery Note par
  "Transporter" field) → Custom Field, fixture ke tor par export karein —
  doosri app ka DocType JSON kabhi edit na karein.
- **Apne DocType par aik-off field** → usay DocType mein add karein, sahi
  position par, upar wale paanch rules ko follow karte hue.

## Aam ghaltiyan

- **Koi Section / Column Breaks nahi.** 20 fields ka aik lamba column.
  Users ko is se nafrat hai, aur yeh pehli cheez hai jo aik reviewer flag
  karega.
- **Link ki jagah free text.** "Customer" Data ke tor par, Customer se Link
  ke bajaye — reports aur filters toot jate hain.
- **Apne section ke baghair child table.** Yeh cramped render hoti hai aur
  miss ho jati hai.
- **Sab kuch `In List View`.** List mein das columns, jin mein se aadhe
  khali hain. Isay 4–5 par rakhein.
- **Koi naming series nahi.** Hash se naam wale records phone par nahi
  milte.
- **DocType ko ghalat module mein banana.** Yeh ghalat app mein aa jata hai
  aur ship nahi ho sakta. Shuru karne se pehle Module set karein.
- **`migrate` skip karna.** DocType UI mein mojood hai lekin table tab tak
  nahi banti jab tak aap migrate nahi karte.

## Next

[04 — Desk, List View, Form View](04-desk-list-form.md) — users asal mein
un records ke saath kaise kaam karte hain jo aap ne abhi define kiye hain.
