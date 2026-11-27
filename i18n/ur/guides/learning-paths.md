---
description: "Hub se guzarne ke do learning paths — Developer Mastery Track, Frappe ko bana kar master karne ke liye, aur Functional Guidance Track, non-developers ke liye."
---

# Learning Paths — Developer Mastery ya Functional Guidance

Yeh hub aik personal mastery path hai, reading list nahi. Yeh is
liye banaya gaya hai ke aik banda is se akela guzre, aur jab tak wo
kaam guide ke baghair na kar sake, tab tak rukay nahi. Is se guzarne
ke do tareeqe hain, is hisab se ke aap kaun hain — aik chunein, aur
us ko tartib se follow karein. Aage peeche mat kudain; har stage
pichli stage ko assume karti hai.

## Aap kaun sa track hain?

- **Developer Mastery Track** — aap code likhte hain, ya likhna
  chahte hain. Aap asal bench par asal cheezein banayenge, keyboard
  par haath rakh kar, aur har stage ko is tarah prove karenge ke
  guide dekhe baghair kar ke dikhayenge. Is track ko follow karein
  agar aap ka goal Frappe work ko *master* karna hai.
- **Functional Guidance Track** — aap code nahi likhte: ERP
  consultant, business user, manager, ya woh banda jo decide karta
  hai ke system ko kya karna hai. Aap samajhne, evaluate karne aur
  implementation ko guide karne ke liye parhenge — code ke baghair.

Aap kisi bhi waqt track badal sakte hain. Jo developer Mastery Track
khatam kar le, usay bhi Functional Track ki case studies parhni
chahiye; jo functional banda DocType kaise kaam karta hai, yeh jan'na
chahe, wo Level 1 mein jhank sakta hai. Yeh tracks raaste hain,
deewarein nahi.

---

## Track 1 — Developer Mastery: Noob se Pro tak

**Tareeqa yeh hai:** lessons parhein, phir checkpoint karein. Aik
checkpoint tab hi complete hota hai jab aap usay *hub khole baghair*
kar sakein — na guide, na notes, sirf aik khaali bench aur aap ki
yaad-dasht. Agar na kar sakein, to wapas ja kar dobara parhein; isi
mein asal seekh hai. Neeche diye gaye time estimates aik rough guide
hain, un ke liye jo haftay mein chand shaamein parhte hain.

### Stage 1 — Foundations (lag bhag 1 hafta)

Tartib se parhein:

- [Lesson 01 — What is Frappe](../learn/framework/level-1/01-what-is-frappe.md)
- [Lesson 02 — Bench, Sites & Apps](../learn/framework/level-1/02-bench-sites-apps.md)
- [Lesson 03 — Your First DocType](../learn/framework/level-1/03-first-doctype.md)
- [Lesson 04 — Desk, List & Form](../learn/framework/level-1/04-desk-list-form.md)

**Checkpoint:** aik fresh bench par, nayi app banayein aur Gate Pass
DocType shuru se banayein — fields `naming_series`,
`gate_pass_date`, `visitor_name`, `company`, `purpose`, plus Gate
Pass Item child table (`item_name`, `qty`, `direction`) — phir Desk
mein aik Gate Pass banayein aur submit karein. Guide khole baghair.

### Stage 2 — Build (lag bhag 2 haftay)

Tartib se parhein:

- [Lesson 05 — Server Scripts & Document Events](../learn/framework/level-2/05-server-scripts-events.md)
- [Lesson 06 — Client Scripts](../learn/framework/level-2/06-client-scripts.md)
- [Lesson 07 — APIs](../learn/framework/level-2/07-apis.md)
- [Lesson 08 — Reports & Print Formats](../learn/framework/level-2/08-reports-print-formats.md)
- [Lesson 09 — Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md)
- [Lesson 10 — Workflows & Assignments](../learn/framework/level-2/10-workflows-assignments.md)

Phir woh documents jin ko aap automate karenge — ERPNext Core modules:

- [Module 01 — Accounting](../learn/erpnext/core/01-accounting.md)
- [Module 02 — Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md)
- [Module 03 — Selling](../learn/erpnext/core/03-selling.md)
- [Module 04 — Buying](../learn/erpnext/core/04-buying.md)

**Checkpoint:** apne Gate Pass mein server-side validation add
karein (future dates nahi, positive quantities) aur aik client script
jo date set kare aur direction par react kare — khud likhein,
yaad-dasht se. Apna kaam baad mein demo app se compare karein,
pehle nahi. Jab atak jayein, to [Cheat Sheets](cheat-sheets.md)
use karein — woh cheezein dekhne ke liye hain, poore solutions
copy karne ke liye nahi.

### Stage 3 — Ship (lag bhag 2 haftay)

Tartib se parhein:

- [Lesson 11 — Scheduler & Background Jobs](../learn/framework/level-3/11-scheduler-jobs.md)
- [Lesson 12 — Notifications, Email & Integrations](../learn/framework/level-3/12-notifications-email.md)
- [Lesson 13 — Testing](../learn/framework/level-3/13-testing.md)
- [Lesson 14 — Performance](../learn/framework/level-3/14-performance.md)
- [Lesson 15 — Security](../learn/framework/level-3/15-security.md)
- [Lesson 16 — Debugging](../learn/framework/level-3/16-debugging.md)

**Checkpoint:** apni app mein aik daily scheduler job add karein jo
stale draft Gate Passes dhoonde, aur aik Script Report likhein jo
Gate Passes ko din ke hisab se list kare. Phir jaan boojh kar kuch
tor dein — aik kharab migration, aik ghalat permission — aur usay
sirf traceback aur
[Lesson 16](../learn/framework/level-3/16-debugging.md) se theek
karein. Debugging kaam ka hissa hai, is mein rukawat nahi.

### Stage 4 — Operations (lag bhag 2 haftay)

Woh ERPNext modules jo asal business chalate hain. Manufacturing
aur Quality practice project ke stock phases *se pehle* parhein —
wahan aap ko in ki zaroorat paregi:

- [Module 05 — Manufacturing](../learn/erpnext/operations/05-manufacturing.md)
- [Module 06 — Quality](../learn/erpnext/operations/06-quality.md)
- [Module 07 — Projects](../learn/erpnext/operations/07-projects.md)
- [Module 08 — Assets](../learn/erpnext/operations/08-assets.md)
- [Module 09 — HR](../learn/erpnext/people/09-hr.md)
- [Module 10 — CRM](../learn/erpnext/people/10-crm.md)
- [Module 11 — Helpdesk](../learn/erpnext/people/11-helpdesk.md)
- [Module 12 — Support & Portal](../learn/erpnext/people/12-support-portal.md)

**Checkpoint:** order-to-cash flow (Sales Order → Delivery Note →
Sales Invoice → Payment Entry) aur buy-to-pay flow (Purchase Order
→ Purchase Receipt → Purchase Invoice → Payment Entry) kisi aur ko
samjhayein, notes ke baghair, har step par DocType ka naam le kar
aur yeh bata kar ke stock aur ledger mein kya badalta hai. Agar
samjha nahi sakte, to abhi seekha nahi.

### Stage 5 — Advanced (lag bhag 2 haftay)

Tartib se parhein:

- [Module 13 — Studio, Flow & Insights](../learn/erpnext/v16/13-studio-flow-insights.md)
- [Module 14 — Cross-Module Flows](../learn/erpnext/v16/14-cross-module-flows.md)
- [Lesson 17 — Studio & Flow](../learn/framework/level-4/17-studio-flow.md)
- [Lesson 18 — Insights](../learn/framework/level-4/18-insights.md)
- [Lesson 19 — Website & Portal](../learn/framework/level-4/19-website-portal.md)
- [Lesson 20 — Upgrades](../learn/framework/level-4/20-upgrades.md)
- [Lesson 21 — Ops](../learn/framework/level-4/21-ops.md)

**Checkpoint:** apni site ka backup lein, usay doosri site par
restore karein, aur
[Upgrade guide](upgrade-v14-v15-v16.md) ke mutabiq upgrade karein.
Jo developer backup restore nahi kar sakta, us ne yeh stage
khatam nahi ki.

### Stage 6 — Capstone: practice project (lag bhag 1 hafta)

[Practice Project — masala factory, shuru se end
tak](practice-project.md) banayein, saari 8 phases, apni bench par.
Yeh poora track aik project mein hai: Gate Pass, BOM aur Work Order,
stock, sales, Quality Inspection gate, invoicing, payment, report
aur print format, phir permissions, backup aur go-live.

[Demo app code](https://github.com/irfanzahoor/frappe-research-hub/tree/main/demo-app)
aik **reference hai, shortcut nahi**: pehle Gate Pass khud banayein,
phir apna code shipped app se line by line compare karein. Agar aap
ka code aur demo app aik jaise hain, to aap ne theek banaya. Agar
farq hai, to pata lagayein ke kyun — woh farq hi asal lesson hai.

### Stage 7 — Aakhri check: interview ki tayyari

[Interview Prep guide](interview-prep.md) se guzrein — 36 sawal,
model jawab ke saath, jin mein spot-the-bug code sawal bhi hain.
Agar aap code aur scenario sawalon ka jawab bina hichkichahat ke
de sakte hain, to aap tayyar hain ke koi aur aap ko test kare.

### "Master" ka matlab kya hai

Aap master tab hain jab aap aik khaali bench par baith kar Gate Pass
app plus practice-project flow — DocTypes, validation, client script,
workflow, report, print format, permissions, backup — **hub khole
baghair** bana sakein. Lafzon ki yaad-dasht se nahi, balkay is
samajh se ke pieces aik doosre se kaise jurrte hain.

Yahi woh bar hai jis ke around yeh track banaya gaya hai. Is ke baad
sirf sharp rehna hai: [Troubleshooting guide](troubleshooting.md)
jab kuch toot jaye, [Cheat Sheets](cheat-sheets.md) jab koi command
chahiye, [Case Studies](case-studies.md) is liye ke asal
implementations kaise gayi, aur har go-live se pehle
[Common Mistakes](common-mistakes.md) ki list.

---

## Track 2 — Functional Guidance: ERPNext samjhein, implementation ko guide karein

**Tareeqa yeh hai:** samajhne ke liye parhein, banane ke liye nahi.
Koi code nahi, koi bench nahi, koi commands nahi. Har stage ke end
par aap ko yeh pata hona chahiye ke aap kya *decide* ya *explain*
kar sakte hain.

### Stage 1 — Frappe aur ERPNext kya hain (chand shaamein)

- [Lesson 01 — What is Frappe](../learn/framework/level-1/01-what-is-frappe.md) — Framework kya hai, ERPNext kya hai, Frappe Cloud kya hai
- [Module 01 — Accounting](../learn/erpnext/core/01-accounting.md)
- [Module 02 — Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md)
- [Module 03 — Selling](../learn/erpnext/core/03-selling.md)
- [Module 04 — Buying](../learn/erpnext/core/04-buying.md)

**Ab aap yeh kar sakein ge:** kisi colleague ko saada alfaaz mein
samjha sakein ke ERPNext business ke liye kya karta hai, aur kaun sa
module paise, stock, sales aur purchasing ka malik hai.

### Stage 2 — Woh flows jo business chalate hain

- [Module 14 — Cross-Module Flows](../learn/erpnext/v16/14-cross-module-flows.md) — order-to-cash, buy-to-pay, forecast → production → sales
- [Module 05 — Manufacturing](../learn/erpnext/operations/05-manufacturing.md)
- [Module 06 — Quality](../learn/erpnext/operations/06-quality.md)
- [Module 07 — Projects](../learn/erpnext/operations/07-projects.md)
- [Module 09 — HR](../learn/erpnext/people/09-hr.md)
- [Module 10 — CRM](../learn/erpnext/people/10-crm.md)

**Ab aap yeh kar sakein ge:** aik sales order ko quotation se
payment tak trace karein aur har step par batayein ke kaun sa
document banta hai aur stock aur accounts mein kya badalta hai.

### Stage 3 — Sahi tools chunein

- [Choosing Apps](choosing-apps.md) — kab app install karni hai aur
  kab khud banana hai, aur har app aap ko baad mein kya cost deti hai
- [Apps Catalog](../research/apps-catalog.md) — kya pehle se mojood
  hai, taake aap woh banane ke paise na dein jo muft mein mil raha hai
- [Go-Live Checklist](go-live-checklist.md) — aik asal go-live ko
  kya chahiye: data, permissions, training, cutover

**Ab aap yeh kar sakein ge:** judge kar sakein ke aik requirement
ke liye nayi app chahiye, chhoti customisation, ya sirf process
mein tabdeeli — aur bata sakein ke us ko maintain karne ki kya
cost hogi.

### Stage 4 — Asal implementations se seekhein

- [Case Studies](case-studies.md) — aik masala manufacturer, aik
  trading/distribution business, aik services company: kya banaya
  gaya, kya ghalat hua, aur is se kya seekhna hai
- [Common Mistakes](common-mistakes.md) — woh ghaltiyan jo teams
  sab se zyada karti hain, taake aap unhein apne project mein
  pehle se pehchan sakein

**Ab aap yeh kar sakein ge:** teen cheezein bata sakein jo ERPNext
implementation mein aam tor par ghalat hoti hain, aur aap kya
mukhtalif karenge.

### Stage 5 — Developers ke saath kaam karein

Code likhne ke liye aap ko code likhna nahi aana chahiye. Inhein
concepts ke tor par parhein, chalane ki instructions ke tor par nahi:

- [Lesson 04 — Desk, List & Form](../learn/framework/level-1/04-desk-list-form.md) — users asal mein system mein kaise kaam karte hain, taake aap apni baat un ki zuban mein keh sakein
- [Lesson 10 — Workflows & Assignments](../learn/framework/level-2/10-workflows-assignments.md) — approvals kaise chalti hain, taake aap aik design kar sakein
- [Lesson 09 — Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md) — kaun kya dekh sakta hai aur kya kar sakta hai, taake aap sahi access maang sakein
- [Lesson 13 — Testing](../learn/framework/level-3/13-testing.md) — quality kaise check karte hain, taake aap delivery ko theek se test kar sakein

**Ab aap yeh kar sakein ge:** aik requirement is tarah likh sakein
ke developer bina guess kiye bana sake — "jab X ho, to system ko Y
karna chahiye, aur Z ko yeh karne ki ijazat nahi honi chahiye" — aur
check kar sakein ke jo deliver hua, kya woh is se match karta hai.

### Stage 6 — Jab cheezein ghalat ho jayein

- [Troubleshooting](troubleshooting.md) — is ko "kya ghalat ho
  sakta hai" ke tor par parhein, khud fix karne ke liye nahi. Aap
  ko yeh jan'na hai ke kaun se masle chhote hain (atki hui email
  queue) aur kaun se serious hain (fail hui migration), taake aap
  urgency judge kar sakein.
- [Upgrade guide](upgrade-v14-v15-v16.md) — upgrade mein kya
  hota hai, taake aap is ke liye plan kar sakein, is se hairan
  hone ke bajaye.

### Is track ko asal implementation mein kaise use karein

Implementation mein Stage 2 apne zehen mein le kar jayein: flows.
Jab developer koi solution propose kare, to teen sawal poochein —
yeh kaun se documents banata hai, stock aur ledger mein kya
badalta hai, aur hum is ko kaise test karenge. Jab vendor koi app
propose kare, to pehle [Choosing Apps](choosing-apps.md) ke sawal
aur [Apps Catalog](../research/apps-catalog.md) check karein. Aur
go-live se pehle, [Go-Live Checklist](go-live-checklist.md) team
ke saath chalayein — yeh is liye mojood hai ke asal go-lives is ke
baghair fail hue hain.
