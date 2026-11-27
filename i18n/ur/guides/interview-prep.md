---
description: "Frappe aur ERPNext developer interview ki tayyari — 36 sawal, model jawab, code spot-the-bug, scenarios aur aik haftay ka revision plan."
---

# Interview ki Tayyari — Frappe & ERPNext Developer Interviews

Interview se aik hafta pehle kholnay wala page. 36 sawal jo Frappe /
ERPNext developer se asal mein poochhay jatay hain, har aik ke saath
aik mukhtasar model jawab — itna lamba ke samajh aa jaye, itna chhota
ke bol kar sunaya ja sakay. Har section ke saath woh lesson linked hai
jo isay sikhata hai, aur end par [aik haftay ka plan](#aik-haftay-ka-plan-interview-se-pehle)
hai — roz kya revise karna hai.

Is guide ko aise use karein: sawal parhein, model jawab parhnay **se
pehle** khud zor se jawab dein. Agar apnay alfaz mein nahi bol saktay,
to linked lesson par wapas jayein. Code walay sawal junior aur
mid-level ka farq tay kartay hain — un ki practice do dafa karein.

---

## 1. Frappe Framework basics

Revise karein: [Lesson 01](../learn/framework/level-1/01-what-is-frappe.md),
[Lesson 02](../learn/framework/level-1/02-bench-sites-apps.md),
[Lesson 03](../learn/framework/level-1/03-first-doctype.md),
[Lesson 05](../learn/framework/level-2/05-server-scripts-events.md),
[Lesson 09](../learn/framework/level-2/09-permissions-roles.md),
[Lesson 11](../learn/framework/level-3/11-scheduler-jobs.md).

**Q1. Frappe Framework kya hai?**

Python aur JavaScript mein aik full-stack, metadata-driven web
framework, MariaDB (ya Postgres) ke saath. Aap aik DocType define
karein aur Frappe muft mein de deta hai — database table, form, list
view, permissions aur REST API. ERPNext Frappe par bani hui aik app
hai — framework platform hai, ERPNext us ke upar business logic hai.

**Q2. DocType kya hota hai?**

Aik definition jo aik hi waqt mein database table, form, list view,
permission set aur API endpoint hai. DocType ke fields hotay hain
(Data, Link, Select, Table…), aur ye standard (app ke saath aaya hua)
ya custom (aap ka banaya hua) ho sakta hai. Child DocTypes chhoti
DocTypes hain jo sirf parent ke andar rehti hain — masalan Sales
Order Item, Sales Order ke andar lines ki table hoti hai.

**Q3. Bench, site, app — in mein farq kya hai?**

Bench aik folder hai jis mein apps aur sites hoti hain. Site aik
database plus aik config hai — aik company, aik set of data. App aik
code package hai (DocTypes, scripts, reports) jo aik ya zyada sites
par install hoti hai. Aik bench mein kayi sites ho sakti hain, aur
aik site par kayi apps chal sakti hain.

**Q4. Hooks kya hotay hain, aur kahan rehtay hain?**

Hooks app ki `hooks.py` file hai jo Frappe ko batati hai ke aap ka
code kab chalay: `doc_events` (Sales Order submit honay par ye
function chalao), `scheduler_events` (roz subah 9 bajay ye chalao),
`fixtures` (ye records app ke saath ship karo),
`override_doctype_class`. Agar aap chahtay hain ke framework ke kisi
moment par aap ka code chalay, to taqreeban hamesha us ke liye koi
hook hota hai.

**Q5. Server Script vs Client Script — konsa kab use karna hai?**

Server Script server par Python hai: database parh aur likh sakta
hai, APIs call kar sakta hai, aur rules enforce kar sakta hai — ye
wahid jagah hai jahan business logic mehfooz hai. Client Script
browser mein JavaScript hai: form behaviour, fields dikhana ya
chhupana, fori feedback. Jo cheez user ko bypass nahi karni chahiye,
wo server par honi chahiye — Client Script ko hamesha skip kiya ja
sakta hai.

**Q6. Save aur submit par document events kis order mein chaltay hain?**

Pehli save par: `before_insert`, phir `validate`, phir `before_save`,
phir `after_insert`. Har agli save par: `validate`, `before_save`,
phir `on_update`. Submit par: `before_submit`, phir `on_submit`.
Cancel par: `on_cancel`. Yaad rakhnay wala rule: `validate` **har**
save par chalta hai, is liye woh checks jo hamesha lagoo honay
chahiye, wahin lagayein — sirf `before_insert` mein kabhi nahi, warna
aik edit usay bypass kar de gi.

**Q7. Submittable DocType kya hoti hai?**

Aik DocType jis ka `docstatus` hota hai: 0 = Draft, 1 = Submitted,
2 = Cancelled. Sales Invoice, Delivery Note aur Stock Entry
submittable hain — submit honay ke baad document lock ho jata hai aur
us ke stock aur ledger effects lag chukay hotay hain. Wapas janay ka
wahid tareeqa Cancel hai, jo un effects ko reverse kar deta hai.
Drafts ko azadi se edit kiya ja sakta hai; submitted documents ko
nahi.

**Q8. Frappe mein permissions kaise kaam karti hain?**

Permissions role-based hain, har DocType ke liye, Role Permission
Manager mein set hoti hain: har role ke liye Read, Write, Create,
Submit, Cancel aur Delete tick karein. Field-level control permlevel
se hota hai — permlevel 1 par aik field un roles ko nazar nahi aata
jin ke paas sirf permlevel 0 hai. User Permissions is se agay ja kar
ye restrict karti hain ke user *kon se records* dekh sakta hai,
masalan sirf apna warehouse ya territory.

**Q9. Scheduler kya hai, aur background jobs kaise kaam kartay hain?**

Scheduler aik timetable par jobs chalata hai jo `hooks.py` mein
`scheduler_events` se define hota hai — `all` (har minute), `hourly`,
`daily`, `weekly`, `monthly`, ya aik `cron` expression. Bhaari kaam
`frappe.enqueue` se background jobs mein jata hai, taake web request
foran wapas aa jaye aur aik worker slow kaam baad mein `short`,
`default` ya `long` queue mein karay. `bench enable-scheduler` se
site ke liye scheduler on hota hai.

**Q10. Child table, technically, kya hoti hai?**

Aik child DocType jis ka `istable` set ho — us ki koi list view nahi
hoti aur us ke standalone records nahi hotay. Us ki rows apni table
mein teen link columns ke saath store hoti hain: `parent` (parent
document ka name), `parenttype` (parent DocType) aur `parentfield`
(kon si table field mein hai). Isi liye child row hamesha parent ke
saath hi fetch aur save hoti hai.

---

## 2. ERPNext functional

Revise karein: [Accounting](../learn/erpnext/core/01-accounting.md),
[Stock](../learn/erpnext/core/02-stock-inventory.md),
[Selling](../learn/erpnext/core/03-selling.md),
[Buying](../learn/erpnext/core/04-buying.md),
[Manufacturing](../learn/erpnext/operations/05-manufacturing.md),
[Quality](../learn/erpnext/operations/06-quality.md),
[HR](../learn/erpnext/people/09-hr.md),
[CRM](../learn/erpnext/people/10-crm.md).

**Q11. Order-to-cash flow samjhayein.**

Quotation → Sales Order → Delivery Note → Sales Invoice → Payment
Entry. Quotation price ki offer hai. Sales Order commitment hai.
Delivery Note stock bahar bhejta hai aur cost of goods book karta
hai. Sales Invoice revenue aur receivable book karta hai. Payment
Entry receivable ko bank ke against band karta hai. Har step aik
alag submittable document hai, is liye har step auditable hai.

**Q12. Sales Invoice submit honay par General Ledger mein kya hota hai?**

Customer ko Debit (accounts receivable — customer ke zimme),
Income account ko Credit (sales), aur tax ke liye Tax account ko
Credit. Jab Payment Entry submit hoti hai, to Bank ko Debit aur
Customer ko Credit hota hai, jis se receivable band ho jata hai. Har
ERPNext transaction aik balanced double entry hai — isi liye reports
qabil-e-bharosa hoti hain.

**Q13. Buying / stock flow samjhayein.**

Purchase Requisition → Purchase Order → Purchase Receipt → Purchase
Invoice → Payment Entry. Purchase Receipt key step hai: ye stock
barhata hai aur post karta hai Debit Stock, Credit "Stock Received
But Not Billed". Purchase Invoice phir us account ko clear karti hai
— Debit "Stock Received But Not Billed", Credit Supplier. Ye
three-way match (order vs receipt vs invoice) hi hai jo over-billing
pakarta hai.

**Q14. Manufacturing flow samjhayein.**

BOM → Work Order → Stock Entry → Quality Inspection → Delivery. BOM
aik finished item ke raw materials aur operations ki list hai. Work
Order quantity plan karta hai. "Material Transfer for Manufacture"
type ki Stock Entry raw material ko work-in-progress warehouse mein
le jati hai, aur "Manufacture" type ki Stock Entry usay consume kar
ke finished item bana deti hai. Quality Inspection dispatch ko gate
karti hai — pass honay se pehle kuch ship nahi hota.

**Q15. BOM kya hai, aur is mein kya hota hai?**

Bill of Materials aik finished item ki recipe hai: raw materials
(quantities aur rates ke saath), operations (workstations aur times
ke saath), aur resulting cost. BOM single-level ho sakti hai (saaray
raw materials seedha listed) ya multi-level (aik raw material khud
kisi aur BOM se banta ho). BOM badlein to har future Work Order nayi
recipe use karta hai — purani orders wohi BOM rakhti hain jis se
banayi gayi thin.

**Q16. Batch vs Serial No — konsa kab use karna hai?**

Batch jab kayi identical units ko aik group ke tor par track karna
ho: aik hi manufacturing date, aik hi expiry, aik hi quality
result — medicines, masalay, khana. Serial jab har aik unit unique
ho aur usay alag se track karna ho — machines, phones, vehicles.
Batches mein FEFO (first-expiry-first-out) chalta hai; serials aik
aik kar ke pick hotay hain.

**Q17. ERPNext v16 mein HR flow kaisa hai?**

Employee → Leave (Leave Allocation, phir Leave Application) →
Attendance → Salary Structure → Payroll Entry. Leave, attendance,
shifts aur payroll Frappe HR app mein rehtay hain, jo v16 mein
ERPNext ke saath install hoti hai. Jo rule matter karta hai: payroll
sirf approved attendance aur approved leave par chalti hai —
unapproved records kabhi salary slip tak nahi pohunchtay.

**Q18. CRM flow kaisa hai, aur v16 mein kya badla?**

Lead → Opportunity / Deal → Quotation → Customer. v16 mein CRM
Frappe CRM app mein hai (leads, deals, web forms, communication),
ERPNext ke andar nahi. Legacy ERPNext CRM abhi bhi mojood hai lekin
v17 mein remove honay ka schedule hai — is liye naya kaam Frappe CRM
mein banana chahiye, aur purana data upgrade se pehle migrate kar
lena chahiye.

---

## 3. Code & debugging

Revise karein: [Lesson 05](../learn/framework/level-2/05-server-scripts-events.md),
[Lesson 06](../learn/framework/level-2/06-client-scripts.md),
[Lesson 07](../learn/framework/level-2/07-apis.md),
[Lesson 14](../learn/framework/level-3/14-performance.md),
[Lesson 15](../learn/framework/level-3/15-security.md),
[Lesson 16](../learn/framework/level-3/16-debugging.md),
[Cheat Sheets](cheat-sheets.md).

**Q19. Is code mein bug dhoondhein:**

```python
customer = frm.doc.customer  # JS side — is line ko ignore karein, bug neechay hai
frappe.db.sql(f"select name from `tabSales Order` where customer='{customer}'")
```

Ye f-string se SQL banata hai, is liye customer name mein aik quote
honay se query toot jati hai — aur aik malicious value koi bhi SQL
chala sakti hai. Ye SQL injection ka hole hai. Fix parameterised
query se karein:

```python
frappe.db.sql(
    "select name from `tabSales Order` where customer=%s", (customer,))
```

**Q20. Is Client Script mein bug dhoondhein:**

```javascript
frappe.ui.form.on("Employee", {
    refresh: function(frm) {
        frm.set_df_property("salary", "hidden", 1);  // salary sab se chhupao
    }
});
```

JavaScript mein field chhupana security nahi hai — koi bhi API ya
browser console se field parh sakta hai. Fix permlevel hai: `salary`
ko permlevel 1 par rakhein aur wo level sirf HR Manager role ko
dein. Client Scripts user experience ke liye hoti hain, access
control ke liye kabhi nahi.

**Q21. `before_insert` mein aik check edits par bypass ho raha hai. Kyun?**

`before_insert` sirf aik dafa chalta hai, pehli save par. Mojooda
document ki edit usay kabhi nahi chalati. Check ko `validate` mein
le jayein, jo har save par chalta hai — insert se pehle aur update
se pehle. Agar rule document ki poori zindagi ke liye lagoo hona
chahiye, to `validate` hi us ke liye sahi event hai.

**Q22. Is code mein bug dhoondhein:**

```python
rate = frappe.db.get_value("Item Price", {"item_code": item}, "price_list_rate")
total = rate * qty
```

`get_value` `None` return karta hai jab koi matching record na milay,
to `None * qty` se `TypeError` aata hai. Isay guard karein:
`rate = frappe.db.get_value(...) or 0`, ya aik saaf `frappe.throw`
karein ("Is item ki koi price nahi mili") taake user ko pata chalay
ke kya missing hai, bajaye traceback dekhne ke.

**Q23. Ye code kya karta hai, aur aap ye kyun likhein ge?**

```python
frappe.enqueue("my_app.tasks.send_daily_report", queue="long")
```

Ye `send_daily_report` ko web request ke andar chalanay ke bajaye aik
background queue par daal deta hai. User ko foran response mil jata
hai aur aik worker slow job baad mein chalata hai — `long` un jobs
ki queue hai jo minutes leti hain. Ye tab likhein jab request warna
email, bari report, ya external API ka intezar karti.

**Q24. Client Script mein `cur_frm` use karnay mein kya ghalat hai?**

`cur_frm` aik purana global hai jo us form ki taraf point karta hai
jo ittefaq se khula ho — list, dialog, ya doosri tab mein ye ghalat
form ho sakta hai. Function ko sahi form pehle se `frm` ke tor par
milta hai. Hamesha `frm` parameter use karein; `cur_frm` legacy hai
aur naye code mein nahi aana chahiye.

**Q25. `doc.save()` aur `doc.submit()` mein kya farq hai?**

`save()` document ko Draft (docstatus 0) ke tor par likhta hai —
editable, koi stock ya ledger effect nahi. `submit()` usay Submitted
(docstatus 1) mein le jata hai, `before_submit` aur `on_submit`
chalata hai, aur document ke asal effects post karta hai: stock
movements, GL entries, status changes. Submitted document edit nahi
ho sakta — sirf cancel ho sakta hai, jo un effects ko reverse kar
deta hai.

**Q26. Is code mein performance bug dhoondhein:**

```python
for row in sales_order.items:
    item = frappe.get_doc("Item", row.item_code)   # har line par aik query
    row.description = item.description
```

Har line par aik database query — 200 lines walay order mein 200
queries. Ye N+1 problem hai. Fix aik hi query se, shuru mein:

```python
items = {d.name: d.description for d in frappe.get_all(
    "Item", filters={"name": ["in", [r.item_code for r in sales_order.items]]},
    fields=["name", "description"])}
for row in sales_order.items:
    row.description = items.get(row.item_code)
```

Aik query, phir har line par dictionary lookup.

---

## 4. Scenario questions

Revise karein: [Lesson 08](../learn/framework/level-2/08-reports-print-formats.md),
[Lesson 10](../learn/framework/level-2/10-workflows-assignments.md),
[Lesson 12](../learn/framework/level-3/12-notifications-email.md),
[Practice Project](practice-project.md),
[Case Studies](case-studies.md).

**Q27. Client chahta hai ke 10% se zyada discount ke liye manager ki approval chahiye. Kaise banayein ge?**

Sales Order par Workflow se: states Draft → Pending Approval →
Approved, aur Approved ki taraf transition sirf Sales Manager role
kar sakay. Phir aik server-side `validate` backstop ke tor par lagayein
— agar discount 10% se zyada ho aur document Approved state mein na
ho, to `frappe.throw`. Workflow user ko nazar aanay wala process
deta hai; server check ye yakeeni banata hai ke API usay skip na kar
sakay.

**Q28. Client warehouse se bahar janay wali har cheez ke liye gate-pass register chahta hai. Kaise banayein ge?**

Aik custom DocType "Gate Pass" (naming series, date, visitor name,
company, purpose) jis ki child table "Gate Pass Item" ho (item, qty,
direction in/out), aur jahan lagoo ho wahan Delivery Note se linked
ho. Security desk ke liye approval Workflow lagayein, aur aik Script
Report jo khulay gate passes dikhaye — jo issue ho chukay hon lekin
wapas na aaye hon. Ye wohi register hai jo practice project aur
Lesson 03 mein banaya gaya hai.

**Q29. Client ko aik report chahiye jo standard reports se nahi ban sakti. Kya banayein ge?**

Script Report jab Python logic chahiye ho — grouping, DocTypes ke
beech calculations, ya custom columns — aur Query Report jab aik SQL
query kaafi ho. Pehle check karein ke standard report plus filter se
kaam ho jata hai ya nahi; sirf phir Script Report likhein, un filters
ke saath jo user ko asal mein chahiye hon, aur usay us module se link
karein jis se us ka talluq hai.

**Q30. Client ke paas Excel mein 5,000 products hain aur wo ERPNext mein chahiye. Data kaise migrate karein ge?**

Data Import tool use karein: template export karein, bhar dein,
pehle chhota batch (50 rows) staging site par import karein, Data
Import Log ki errors theek karein, phir baqi import karein. Asal
import se pehle mandatory fields (item code, item group, stock UOM)
aur duplicates validate karein, aur backup ke baghair production
mein kabhi seedha import na karein. Ganday data ke liye
`frappe.get_doc(...).insert()` wali chhoti import script tool se
zyada control deti hai.

**Q31. Aik report khulnay mein do minute leti hai. Problem kaise dhoondhein ge?**

Pehle reproduce karein aur slow-query log parhein — kya aik slow
query hai ya kayi chhoti queries? Loop mein kayi chhoti queries N+1
problem hai: aik dafa fetch karein, memory mein lookup karein. Aik
slow query ko aam tor par filtered column par index chahiye hota hai,
ya chhoti date range. Ye bhi check karein ke report woh rows to
nahi fetch kar rahi jo dikhati hi nahi. Query theek karein, dobara
measure karein, aur sirf phir caching ya baray server ke baaray mein
sochhein.

**Q32. Shaam 5 bajay production bug report hota hai. Kya karein ge?**

Live par hot-fix na karein. Pehle staging par reproduce karein, Error
Log aur traceback ki aakhri lines parhein, aur sab se chhoti change
dhoondhein jo isay theek karay. Fix ko staging par test karein,
production ka backup lein, normal path se deploy karein
(`bench update` / `bench migrate`), live par verify karein, aur users
ko batayein ke kya hua tha. Agar data ghalat hai, to pehle code theek
karein — phir client ke saath tay karein ke ghalat data kaise correct
ho ga.

---

## 5. HR / behavioural

**Q33. "Apnay kisi project ke baaray mein batayein."**

Feature list se nahi, shape se jawab dein: problem, kya banaya, kya
ghalat hua, aur result. Masalan: "Aik masala manufacturer dispatches
kagaz par track karta tha, to hum ne ERPNext mein gate-pass register
aur quality gate banaya — pehlay version mein aik kharab batch ship
ho gaya kyun ke gate dair se lagaya gaya tha, is liye hum ne
inspection ko dispatch se pehle blocking bana diya. Dispatch errors
kam ho gayein aur owner ko aakhirkaar nazar aanay laga ke warehouse
se kya nikla hai." Aik asal kahani paanch feature names se behtar
hai.

**Q34. "Aap naya ERPNext module kaise seekhtay hain?"**

"Pehle test site par module ko user ki tarah use karta hoon —
documents banata hoon, submit karta hoon, aur un ki ledger aur stock
entries parhta hoon. Phir DocTypes parhta hoon ke fields aur links
kya hain, aur sirf phir koi customisation likhta hoon. Agar kuch
samajh na aaye, to source code hi documentation hai."

**Q35. "User kehta hai 'system ghalat hai'. Kya karein ge?"**

Code ko chhoonay se pehle un ke data ke saath reproduce karein.
Aksar system sahi hota hai aur data ghalat hota hai — ghalat rate,
missing stock entry, cancelled document. Unhein ledger ya stock
ledger entry dikha kar sabit karein ke kya hua tha, un ke alfaz mein
samjhayein, aur data un ke saath theek karein. Agar code waqai ghalat
ho, to saaf saaf keh dein aur theek kar dein.

**Q36. "Doosray ERP ke bajaye Frappe / ERPNext kyun?"**

Open source, aik stack (Python + MariaDB + JavaScript), aur
metadata-driven — DocType se form, list, permissions aur API bina
boilerplate ke mil jatay hain, is liye customisation tez hoti hai aur
upgradeable rehti hai. Imaandaar trade-off: aap ko Python developers
chahiye hotay hain, aur upgrades mein ehtiyaat chahiye kyun ke custom
code toot sakta hai. Ye un businesses ke liye fit hai jo apnay
workflows chahtay hain; ye us company ke liye sahi choice nahi jo
zero customisation chahti hai.

---

## Aik haftay ka plan — interview se pehle

Roz aik block revise karein, aur aglay block par janay se pehle us
block ke sawalat zor se bol kar jawab dein. Day 7 code walay sawalat
aur mock run ke liye hai.

| Din | Revise karein | Phir ye jawab dein |
|---|---|---|
| 1 | [Lessons 01–04](../learn/framework/level-1/01-what-is-frappe.md) — Frappe kya hai, bench, DocTypes, Desk | Section 1, Q1–Q3, Q10 |
| 2 | [Lessons 05–07](../learn/framework/level-2/05-server-scripts-events.md) — server scripts, client scripts, APIs | Section 1, Q4–Q6; Section 3, Q19–Q25 |
| 3 | [Lessons 08–10](../learn/framework/level-2/08-reports-print-formats.md) — reports, permissions, workflows | Section 1, Q7–Q8; Section 4, Q27–Q29 |
| 4 | [ERPNext core](../learn/erpnext/core/01-accounting.md) — Accounting, Stock, Selling, Buying | Section 2, Q11–Q13, Q16 |
| 5 | [ERPNext operations & people](../learn/erpnext/operations/05-manufacturing.md) — Manufacturing, Quality, Projects, HR, CRM | Section 2, Q14–Q15, Q17–Q18; Section 4, Q30–Q32 |
| 6 | [Level 3](../learn/framework/level-3/11-scheduler-jobs.md) — scheduler, testing, performance, security, debugging + [Troubleshooting](troubleshooting.md) | Section 1, Q9; Section 3, Q26; Section 4, Q31–Q32 |
| 7 | [Practice Project](practice-project.md) — masala factory ka flow aik dafa shuru se end tak banayein | Section 3 poora + Section 5 zor se, mock interview ki tarah |

---

## Agay kahan jayein

- [Cheat Sheets](cheat-sheets.md) — in jawabon walay commands, hooks aur API calls, aik page par
- [Troubleshooting](troubleshooting.md) — tayyari ke doran milnay wali 22 errors
- [Practice Project](practice-project.md) — poora flow aik dafa banayein, taake Q33 mein is ke baaray mein bol sakein
- [Case Studies](case-studies.md) — scenario jawabon mein quote karnay ke liye asal production stories

---

**Hum isay kaise istemal kar sakte hain:** interview se pehle is guide
ko aik haftay ke plan ke saath parhein — har section ke sawalat zor se
bol kar jawab dein, aur jahan atkein wahan linked lesson par wapas
jayein. NexTash mein naye developers ki hiring ke liye yehi sawalat
screening ke tor par use ho saktay hain.
