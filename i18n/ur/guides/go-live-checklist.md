# Go-Live Checklist

Go-live aik project hai, aik din nahi. System tab ready hota hai jab
data theek ho, users apna kaam kar sakte hon, aur purana system ab bhi
aap ko bacha sakta ho. Aik distributor perfect code aur ghalat opening
stock ke saath live gaya — pehle mahine ki reports fiction thi. Ye
checklist is liye hai ke ye dobara na ho.

## 1. Data import order

Dependency ki tarteeb mein import karein — aik transaction us master ko
reference nahi kar sakti jo abhi maujood hi nahi hai:

```text
1. Company → Chart of Accounts → Cost Centers → Tax Templates
2. Masters: Item (+ Item Group, UOM, Warehouse), Customer, Supplier,
   Price List, BOM
3. Opening balances: stock + accounts (section 2)
4. Open transactions: open Sales Orders, Purchase Orders, open
   Sales/Purchase Invoices, open Payment Entries
```

Rules: **aik DocType ke liye aik file**, Data Import se import karein
(v16.50 mein step-based wizard hai — usi ko use karein). Pehle test
import par validate karein; kabhi seedha live mein import na karein.
Har import ko reconcile karein: file mein row counts vs system mein
rows, das records haath se khol kar dekhein. Ghalat data file mein fix
kiya jata hai aur dobara import kiya jata hai — file hi record hai.

## 2. Opening balances

**Stock** — Stock Reconciliation, posting date = cutover date, har line
par reason ke saath. Bin quantities physical count se match karni
chahiye. Agar warehouse count aur sheet mein farq ho, to count jeet ti
hai aur farq likh diya jata hai, chhupaya nahi jata.

**Accounts** — customer aur supplier ke opening balances Opening Invoice
Creation Tool se (har party ke liye aik opening invoice, cutover date
wali), bank aur cash ka opening Journal Entry se. Phir woh test jo matter
karta hai: **Trial Balance ko balance hona chahiye** (debits = credits)
go-live se pehle. Agar balance na ho, to go-live ruk jata hai.

**Users ke aane se pehle reconcile karein:** books mein stock value vs
stock report, Accounts Receivable vs customer ledger, Accounts Payable
vs supplier ledger. Teen numbers, teen matches, koi exception nahi.

## 3. Permissions & roles

- Role Permission Manager mein roles aur permissions set karein — har
  DocType, har role ke liye, har shakhs ke liye nahi. User Permissions
  (Company, Warehouse, Branch) un users ke liye jo sirf apni branch ya
  warehouse dekh sakte hon.
- **Asal user accounts se test karein.** Accountant, store keeper, sales
  rep ke tor par log in karein — aur un ka asal kaam karein: Sales
  Invoice banayein, Stock Entry submit karein, Purchase Order approve
  karein. Administrator ke tor par test karne se kuch sabit nahi hota;
  Administrator sab kuch kar sakta hai.
- Portal users (customers, suppliers) ko bhi test karein — woh portal
  se log in karte hain aur sirf apne documents dekhte hain.
- v16 par, `has_permission` hooks ko explicit `True` return karna lazmi
  hai (dekhein [Lesson 09](../learn/framework/level-2/09-permissions-roles.md)).
  `None` return karne wala hook sab ko lock kar deta hai.
- JS mein field chhupana security nahi hai — permlevel use karein.
  Validation server par karein, sirf JS mein nahi (dekhein
  [Common mistakes](common-mistakes.md)).

## 4. User training

- **NexTash client ke super users ko train karta hai; super users apni
  teams ko train karte hain.** Poore staff ko seedha train karna scale
  nahi karta aur yaad bhi nahi rehta.
- Har role ke liye material, har kaam ke liye aik page: "How to make a
  Sales Invoice", "How to receive stock", "How to approve a leave
  application". Chhoti SOPs, woh manual nahi jo koi parhta hi nahi.
- Training **sample data wali training site** par hoti hai, kabhi live
  par nahi. Users training mein cheezein tor kar seekhte hain; users
  live mein cheezein tor dein to business ruk jata hai.
- Har role training mein apna asal kaam aik dafa karta hai — pehla asal
  invoice pehla invoice nahi hona chahiye jo kabhi banaya gaya ho.

## 5. Cutover plan

- **Freeze date likh kar agree ki jati hai.** Friday close ke baad
  purane system mein koi nayi transaction nahi. Freeze ke baad ki har
  cheez ERPNext mein jati hai.
- **Final import Saturday ko:** masters delta (hafte ke dauraan add kiye
  gaye customers ya items), opening balances, open transactions.
- **Delta entries:** final import ke baad jo kuch reh gaya ho, woh Monday
  subah haath se enter kiya jata hai aur list se tick kar diya jata hai.
- **Communication:** har user ko freeze date, go-live date, aur ye pata
  ho ke stuck hone par kis ko call karna hai. Client ka manager is ka
  elaan karta hai.

## 6. Backups & restore test

```bash
bench --site <site> backup --with-files
```

- Scheduled backups go-live se pehle on hon (v16 par, offsite backups
  aik alag app hai — use install karein, ye na maan lein ke ye built in
  hai).
- **Go-live se pehle spare site par restore test kiya gaya ho.** Jo
  backup kabhi restore nahi kiya gaya, woh backup nahi hai.
- Backup files server se bahar rakhi jayein — database wali disk par
  backup aik copy hai, backup nahi.

## 7. Monitoring

Pehle hafte mein, koi rozana check karta hai: **Scheduler chal raha hai**
— `bench doctor` aur Desk mein Background Jobs list. Ruka hua scheduler
matlab no emails, no notifications, no auto-reposts — khamoshi se.
**Email Queue drain ho rahi hai** — emails bheji ja rahi hain, stuck
nahi hain. **Error Log saaf hai** — har error parha gaya, sirf gina nahi
gaya; aik error jo 200 dafa repeat ho, woh aik bug hai, use fix karein.
**Disk space** — bhari hui disk database ko rok deti hai. **Integrations
end-to-end** — payment gateway, WhatsApp, webhooks: go-live wale din har
aik ki aik asal transaction.

## 8. Rollback / Plan B

- **Purana system aik hafte tak chalane ke qabil rehta hai.** Excel,
  purana ERP, paper register — jo bhi tha, woh go-live wale din delete
  nahi kiya jata.
- **Rollback trigger pehle se agree kiya jata hai:** masalan "agar
  invoicing do ghante ke liye down ho, to hum purane system par wapas
  chale jate hain aur dobara plan karte hain." Ye ab sukoon se tay kiya
  jata hai, Monday ko panic mein nahi.
- Rollback se pehle ERPNext mein enter kiya gaya data exportable hona
  chahiye — use bahar kaise nikalna hai (report export), ye pehle se
  pata ho, zaroorat parne se pehle.

## 9. Go-live day runbook

| Waqt | Kaam | Zimmedar |
|---|---|---|
| 08:00 | Scheduler, Email Queue, Error Log, disk check ki gayi; backup liya gaya | NexTash |
| 08:30 | Users log in karte hain; har role apna workspace kholta hai | Super users |
| 09:00 | Pehla asal Sales Invoice sales team ke saath mil kar banaya gaya | Sales super user |
| 10:00 | Pehli stock movement Bin se check ki gayi | Store keeper |
| 12:00 | Pehli Payment Entry, bank balance check kiya gaya | Accountant |
| 14:00 | Error Log review kiya gaya; har error fix kiya gaya ya owner ke saath log kiya gaya | NexTash |
| 16:00 | Day-1 sign-off call: kya kaam kiya, kya blocked hai, kal ki list | Client manager + NexTash |
| 17:00 | Backup liya gaya; day-1 notes likh diye gaye | NexTash |

## Go-live checklist

**Data**
- [ ] Masters tarteeb se import kiye gaye, row counts reconcile kiye gaye
- [ ] Opening stock physical count se reconcile kiya gaya
- [ ] Opening balances import kiye gaye; Trial Balance balance hai
- [ ] AR / AP / stock value ledgers se reconcile kiye gaye
- [ ] Open transactions import ki gayi hain (orders, open invoices)

**Permissions**
- [ ] Roles har DocType ke liye set hain; User Permissions har branch/warehouse ke liye
- [ ] Asal user accounts se test kiya gaya, Administrator se nahi
- [ ] Portal users test kiye gaye

**Training**
- [ ] Super users train kiye gaye; har role ke liye SOPs likhi gayi hain
- [ ] Har role ne training site par apna asal kaam aik dafa kiya

**Cutover**
- [ ] Freeze date likh kar agree ki gayi; final import ho gaya
- [ ] Monday subah ke liye delta list tayyar hai

**Backups & monitoring**
- [ ] Scheduled backups on hain; spare site par restore test kiya gaya
- [ ] Scheduler, Email Queue, Error Log check kiye gaye; integrations end-to-end test ki gayi hain

**Rollback**
- [ ] Purana system aik hafte tak chalane ke qabil hai
- [ ] Rollback trigger client se agree kiya gaya

## Sources

Lesson cross-references: [01 — Accounting](../learn/erpnext/core/01-accounting.md)
(opening balances, Trial Balance),
[02 — Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md)
(Stock Reconciliation, Bin),
[09 — Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md),
[11 — Scheduler & Background Jobs](../learn/framework/level-3/11-scheduler-jobs.md),
[12 — Notifications & Email](../learn/framework/level-3/12-notifications-email.md),
and [Common mistakes](common-mistakes.md) (permissions, ledger rules).
