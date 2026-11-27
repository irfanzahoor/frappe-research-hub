---
description: "Frappe aur ERPNext glossary — 56 terms saada zuban mein, har aik ke saath woh lesson jis se yeh seekha jata hai."
---

# Glossary — Frappe & ERPNext ke Alfaz, Saada Zuban Mein

Is hub ka har mushkil lafz, aik ya do lines mein samjhaya hua. Terms
English mein rehte hain (yeh woh alfaz hain jo aap ko screen par
dikhen ge); definition saada meaning hai. Jahan aik term sikhaya jata
hai, wahan woh lesson linked hai jo isay sikhata hai.

Dono tracks ke liye: developers in terms se lessons mein milte hain,
functional log in se meetings mein milte hain. Agar koi lafz missing
hai, to issue kholein — request template repo mein hai.

**Kisi letter par jayein:** [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [L](#l) · [M](#m) · [N](#n) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w)

K, O, X, Y, Z ke neeche koi term nahi — abhi tak.

---

## A

**API** — Aik system doosre system se data ya kaam mangne ka tareeqa,
aik tay shuda address (URL) aur format se. Frappe mein aik whitelisted
server method API ban jata hai, jise browser, doosri app ya
`bench execute` se call kar sakte hain. Sikhaya jata hai:
[Lesson 07](../learn/framework/level-2/07-apis.md).

**App** — DocTypes, code aur reports ka aik package jo bench mein aik
feature set add karta hai. ERPNext khud Frappe par bani hui aik app
hai, aur aap ka custom code aap ki apni app mein rehta hai. Sikhaya
jata hai:
[Lesson 02](../learn/framework/level-1/02-bench-sites-apps.md).

## B

**Background Job** — Aik kaam jo user ke click ke baad peeche chalta
hai — masalan bulk email bhejna ya bari report banana — taake screen
us ke kaam karte waqt freeze na ho. Sikhaya jata hai:
[Lesson 11](../learn/framework/level-3/11-scheduler-jobs.md).

**Batch** — Aik saath receive ya banaya gaya stock ka aik lot, apne
batch number ke saath — taake pata chale kharab item kis batch ka tha,
aur sab se purana batch pehle use ho (FEFO). Sikhaya jata hai:
[Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md).

**Bench** — Command-line tool (`bench`) jo Frappe installation manage
karta hai: sites banata hai, apps install karta hai, migrations
chalata hai aur server start karta hai. Jis folder mein yeh banata
hai, usay bhi bench kehte hain. Sikhaya jata hai:
[Lesson 02](../learn/framework/level-1/02-bench-sites-apps.md).

**BOM** — Bill of Materials: aik item banane ki recipe — aik finished
unit mein kaun se raw materials, kitni quantity mein, lagte hain. Work
Order BOM se banta hai. Sikhaya jata hai:
[Manufacturing](../learn/erpnext/operations/05-manufacturing.md).

## C

**Child Table** — Form ke andar aik table: rows ki list (jaise invoice
lines ya gate-pass items) jo parent document se judi hoti hain aur us
ke saath save hoti hain. Sikhaya jata hai:
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**Client Script** — JavaScript jo user ke browser mein chalti hai aur
form ka behaviour badalti hai — field show ya hide karna, default
bharna, ya save se pehle value check karna. Is par security ke liye
bharosa nahi kar sakte, kyun ke yeh server par nahi chalti. Sikhaya
jata hai:
[Lesson 06](../learn/framework/level-2/06-client-scripts.md).

**Controller** — DocType ke peeche Python class (app ke
`doctype/<name>/<name>.py` mein) jahan document ki server-side logic
rehti hai: `validate`, `before_save`, `on_submit` aur aise methods.
Sikhaya jata hai:
[Lesson 05](../learn/framework/level-2/05-server-scripts-events.md).

**Currency** — Field type jo paisay store karta hai, company ki
currency ke symbol aur decimals ke saath. Sikhaya jata hai:
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

## D

**Dashboard** — Charts aur number cards ka aik page jo aik nazar mein
business ki haalat dikhata hai — is mahine ki sales, khule orders,
kam stock. Desk ya Insights mein banta hai. Sikhaya jata hai:
[Lesson 04](../learn/framework/level-1/04-desk-list-form.md).

**Data** — Field type jo aik chhoti line text store karta hai, jaise
naam ya code. Sikhaya jata hai:
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**Date** — Field type jo calendar date store karta hai, time ke
baghair. Sikhaya jata hai:
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**Desk** — Frappe ki main work screen: sidebar, workspaces, list views
aur forms, jahan users roz ka kaam karte hain. Sikhaya jata hai:
[Lesson 04](../learn/framework/level-1/04-desk-list-form.md).

**DocStatus** — Document ki state aik number mein: 0 = Draft,
1 = Submitted, 2 = Cancelled. Workflows aur permissions aksar is par
depend karte hain. Sikhaya jata hai:
[Lesson 10](../learn/framework/level-2/10-workflows-assignments.md).

**DocType** — Aik kisam ke document ki definition: us ke fields, us
ka behaviour, aur us ki permissions. Frappe aik DocType ko database
table, form, list view aur API mein badal deta hai. Sikhaya jata hai:
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

## E

**ERPNext** — Frappe par bana hua open-source ERP app: accounting,
stock, selling, buying, manufacturing, HR, CRM aur bohat kuch, aik hi
system mein. Sikhaya jata hai:
[Lesson 01](../learn/framework/level-1/01-what-is-frappe.md).

## F

**Field** — Form par maloomat ka aik box — naam, date, doosre document
ka link. Har field ki aik type hoti hai (Data, Link, Currency…) jo tay
karti hai ke is mein kya aa sakta hai. Sikhaya jata hai:
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**Fixture** — Data jo aik app apne saath le kar aati hai aur har
migrate par dobara install karti hai — masalan aik standard Role,
Workflow ya Print Format jo app ko kaam karne ke liye chahiye. List
hai:
[Cheat Sheets](cheat-sheets.md) mein.

**Frappe Framework** — Open-source Python-aur-JavaScript web framework
jis par ERPNext bana hai: yeh DocTypes, permissions, reports, APIs aur
Desk interface deta hai, is liye aik app zyada tar definitions hoti
hai, plumbing nahi. Sikhaya jata hai:
[Lesson 01](../learn/framework/level-1/01-what-is-frappe.md).

## G

**GL Entry** — General Ledger Entry: accounts mein aik line. Har
invoice, payment aur stock movement GL Entries likhta hai, aur trial
balance in ka total hota hai. Sikhaya jata hai:
[Accounting](../learn/erpnext/core/01-accounting.md).

## H

**Hook** — App ki `hooks.py` mein aik line jo app ke code ko Frappe se
jorti hai — masalan "jab Sales Order submit ho, yeh function chalao",
ya "yeh job har raat barah baje chalao". Sikhaya jata hai:
[Lesson 05](../learn/framework/level-2/05-server-scripts-events.md).

**HTML** — Field type jo form par fixed text, instructions ya
formatted note dikhata hai. Yeh koi data store nahi karta, sirf
dikhata hai. Sikhaya jata hai:
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

## I

**Insights** — Frappe ka dashboard tool (v16): query se Workbook
banayein, us se charts banayein, aur charts ko Dashboard par lagayein
— baghair code ke. Sikhaya jata hai:
[Lesson 18](../learn/framework/level-4/18-insights.md).

## J

**Jinja** — Print Formats aur notifications mein use hone wali template
language: `{{ doc.customer }}` field ki value print karta hai, aur
`{% if %}` / `{% for %}` conditions aur loops add karte hain. Sikhaya
jata hai:
[Lesson 08](../learn/framework/level-2/08-reports-print-formats.md).

## L

**Link** — Field type jo doosre document ki taraf ishara karta hai,
jaise Customer ya Item. User list se chunta hai, aur Frappe check
karta hai ke linked document mojood hai. Sikhaya jata hai:
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**List View** — Aik table jo aik saath bohat se documents dikhati hai
— tamam Sales Orders, tamam Items — filters, sorting aur columns ke
saath. Sikhaya jata hai:
[Lesson 04](../learn/framework/level-1/04-desk-list-form.md).

## M

**MariaDB** — Database jis mein Frappe sab kuch store karta hai
(Postgres bhi supported hai): har DocType aik table banta hai, har
document aik row. Sikhaya jata hai:
[Lesson 01](../learn/framework/level-1/01-what-is-frappe.md).

**Migration** — Code changes ke baad `bench migrate` chalana: yeh
database tables ko DocTypes ke mutabiq update karta hai, patches
chalata hai, aur fixtures dobara load karta hai. Sikhaya jata hai:
[Lesson 02](../learn/framework/level-1/02-bench-sites-apps.md).

**Module** — App ke andar aik folder jo mutaliq DocTypes ko group
karta hai — masalan Selling module mein Sales Order, Delivery Note aur
Customer hain. Sikhaya jata hai:
[Lesson 02](../learn/framework/level-1/02-bench-sites-apps.md).

## N

**Naming Series** — Pattern jo document numbers banata hai, jaise
`SO-2026-0001`: aik prefix aur running number, har DocType ke liye set
hota hai. Sikhaya jata hai:
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**Notification** — Khud bakhud bheja gaya message — email, Desk alert
ya dono — jab kuch hota hai, jaise approval ke liye ruka hua order ya
leave request jise decision chahiye. Sikhaya jata hai:
[Lesson 12](../learn/framework/level-3/12-notifications-email.md).

## P

**Payment Entry** — Document jo asal mein di gayi ya mili hui raqam
record karta hai — invoices ke against, ya advance ke tor par — aur
mutabiq GL Entries likhta hai. Sikhaya jata hai:
[Accounting](../learn/erpnext/core/01-accounting.md).

**Permission** — Rule jo tay karta hai ke kaun aik DocType ko read,
write, create, submit ya delete kar sakta hai: har Role, har DocType
ke liye, Role Permission Manager mein set hota hai. Sikhaya jata hai:
[Lesson 09](../learn/framework/level-2/09-permissions-roles.md).

**Print Format** — Layout jo document print karte ya PDF banate waqt
use hota hai — document ke fields par Jinja templates se banta hai.
Sikhaya jata hai:
[Lesson 08](../learn/framework/level-2/08-reports-print-formats.md).

## Q

**Quality Inspection** — Document jo goods ki checking ka result
record karta hai — accepted ya rejected, readings ke saath — aur
delivery ya receipt ko pass hone tak rok sakta hai. Sikhaya jata hai:
[Quality](../learn/erpnext/operations/06-quality.md).

**Query Report** — Report jo aik SQL query (aur columns aur filters ke
liye aik chhoti Python file) se likhi jati hai: list-style report
banane ka sab se tez tareeqa. Sikhaya jata hai:
[Lesson 08](../learn/framework/level-2/08-reports-print-formats.md).

## R

**Redis** — In-memory store jo Frappe caching aur job queue ke liye use
karta hai: background jobs Redis mein wait karte hain jab tak worker
unhein utha na le. Sikhaya jata hai:
[Lesson 11](../learn/framework/level-3/11-scheduler-jobs.md).

**Role** — Users ko diya gaya label — Sales User, Stock Manager,
System Manager — jo tay karta hai ke woh kaun se DocTypes dekh sakte
hain aur un ke saath kya kar sakte hain. Sikhaya jata hai:
[Lesson 09](../learn/framework/level-2/09-permissions-roles.md).

## S

**Sales Order** — Customer ka confirmed order: woh kya khareede ga,
kis price par, aur kab. Selling flow ka pehla document. Sikhaya jata
hai: [Selling](../learn/erpnext/core/03-selling.md).

**Scheduler** — Frappe ki ghari: yeh har minute jaagta hai aur due
jobs chalata hai — hourly, daily, ya `hooks.py` mein likhi cron
schedule par. Sikhaya jata hai:
[Lesson 11](../learn/framework/level-3/11-scheduler-jobs.md).

**Script Report** — Report jo Python mein likhi jati hai: query,
columns aur logic par poora control, un reports ke liye jo aik SQL
query se nahi ban sakteen. Sikhaya jata hai:
[Lesson 08](../learn/framework/level-2/08-reports-print-formats.md).

**Section Break** — Layout field jo form par naya section shuru karta
hai, optional heading ke saath — mutaliq fields ko group karne ke liye
use hota hai. Sikhaya jata hai:
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**Server Script** — Python code jo server par chalta hai jab document
event fire hota hai (`validate`, `before_save`, `on_submit`…) — asal
rules yahan rehte hain, kyun ke browser par bharosa nahi kar sakte.
Sikhaya jata hai:
[Lesson 05](../learn/framework/level-2/05-server-scripts-events.md).

**Site** — Aik Frappe installation ka data: aik site ka apna database,
apne users aur apni installed apps hoti hain. Aik bench par bohat si
sites ho sakti hain. Sikhaya jata hai:
[Lesson 02](../learn/framework/level-1/02-bench-sites-apps.md).

**Stock Entry** — Document jo stock ko move karta hai: receive karna,
warehouses ke darmiyan move karna, production mein consume karna, ya
write off karna. Sikhaya jata hai:
[Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md).

**Submit** — Action jo draft document ko final banata hai: DocStatus 0
se 1 ho jata hai, `on_submit` code chalta hai, aur ledger aur stock
effects post hote hain. Submitted documents cancel ho sakte hain, edit
nahi. Sikhaya jata hai:
[Lesson 05](../learn/framework/level-2/05-server-scripts-events.md).

## T

**Tab Break** — Layout field jo form par naya tab shuru karta hai —
lambi forms ko tabs mein baant kar tidy rakhne ke liye use hota hai.
Sikhaya jata hai:
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

**Table** — Field type jo child table hold karta hai: form ke andar
rows ki list, har row child DocType ka aik document. Sikhaya jata hai:
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

## U

**User** — Login account: aik shakhs, email, password, roles aur
permissions ke saath. Sikhaya jata hai:
[Lesson 09](../learn/framework/level-2/09-permissions-roles.md).

## V

**Validation** — Check jo document save hone se pehle chalta hai
(`validate`): agar fail ho, Frappe error dikhata hai aur save karne
se mana kar deta hai — masalan "qty must be positive". Sikhaya jata
hai:
[Lesson 05](../learn/framework/level-2/05-server-scripts-events.md).

## W

**Website** — Frappe ki built-in website: public pages, web forms aur
customer portal pages, Desk wali site se hi serve hote hain. Sikhaya
jata hai:
[Lesson 19](../learn/framework/level-4/19-website-portal.md).

**Work Order** — Production order: is item ki itni quantity, is BOM
se, is date tak banani hai. Yeh material issue, job cards aur
finished-goods receipt ko chalata hai. Sikhaya jata hai:
[Manufacturing](../learn/erpnext/operations/05-manufacturing.md).

**Workflow** — States aur un ke darmiyan transitions ka set — Draft →
Pending Approval → Approved — rules ke saath ke kaun document ko aik
state se doosri mein le ja sakta hai. Sikhaya jata hai:
[Lesson 10](../learn/framework/level-2/10-workflows-assignments.md).

**Workspace** — Desk ka home page: aik job ke liye shortcuts, charts
aur links ka set — Sales, Stock, ya aap ki team ke liye custom
workspace. Sikhaya jata hai:
[Lesson 04](../learn/framework/level-1/04-desk-list-form.md).
