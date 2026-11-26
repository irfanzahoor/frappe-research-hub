# Case Studies — ERPNext Production Mein

Lessons aap ko pieces sikhati hain. Yeh case studies dikhati hain ke
jab woh pieces aik asal business se milte hain to kya hota hai — kya
decisions liye gaye, kya ghaltiyan hui, aur kya result nikla. Yeh
production ERPNext kaam se liye gaye anonymised patterns hain:
company ki type aur size asal hai, naam badle hue hain, aur har number
approximate hai — "taqreeban" aur "roughly" ka matlab yahi hai, koi
measured benchmark nahi.

Har case aik hi shape mein hai: background, problem, solution, kya
ghalat hua, results, aur aap ko is se kya seekhna chahiye. Har case
ke aakhri do sections hi asal point hain: solution se ideas lein,
ghaltiyan parhein taake woh aap se na hon.

---

## Case 1 — Lahore mein aik masala manufacturer

### Background

Aik chhoti spice manufacturer — taqreeban 20–30 log, aik factory,
aik warehouse — laal mirch powder, haldi aur spice mixes pees kar
pack karti hai, aur Punjab bhar ke distributors ko bechti hai.
Business is point se aagay barh gaya tha jahan spreadsheet aur paper
register kaam aate: mahine mein taqreeban 40–60 sales orders, 3–4 raw
materials bulk mein khareede jate, aur har dispatch 1 kg aur 5 kg
packs mein jati.

Yeh wohi tarah ka business hai jo
[Practice Project](practice-project.md) ki factory hai — wohi flow,
wohi documents, demo scale ki bajaye asal scale par.

### Problem

Har haftay teen cheezein takleef deti thin:

1. **Kisi ko nahi pata tha ke stock mein asal mein kya hai.**
   Storekeeper paper register rakhta tha; sales team spreadsheet
   rakhti thi. Dono aksar dinon mein alag hote, aur farq tab pata
   chalta jab customer ka order poora nahi ho pata. Distributor
   200 packs mangwata, spreadsheet kehta ke stock mein hain, aur
   warehouse mein 140 milte.
2. **Quality dispatch ke baad check hoti thi, pehle nahi.** Kharab
   batch factory ko nahi, customer ko milta tha. Aik wapas aayi
   hui consignment ka matlab tha aik distributor ka nuksan — aur
   distributors aapas mein baat karte hain.
3. **Kisi ko nahi pata tha ke aik pack ki asal cost kya hai.** Kachchi
   mirch ki qeemat season ke saath badalti hai. Selling price
   andazay se tay hoti thi, aur koi nahi bata sakta tha ke aik
   mahine mein 1 kg pack par faida hua ya nuksan.

### Solution

Core standard ERPNext tha, aur aik chhoti custom app sirf us aik
cheez ke liye jo ERPNext out of the box nahi karta:

- **BOMs aur batch-wise stock ke saath manufacturing.** Har finished
  product ka BOM bana (kachchi mirch → pisi hui powder → packed
  product), aur raw material aur finished goods ka har batch
  batch-wise track hua, taake quality problem poori mahine ki
  production ki bajaye aik batch tak trace ho sake. Dekhein
  [Lesson 05 — Manufacturing](../learn/erpnext/operations/05-manufacturing.md)
  aur [Lesson 02 — Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md).
- **Dispatch se pehle Quality Inspection gate.** Koi Delivery Note
  submit nahi ho sakta tha jab tak batch ki inspection pass na ho —
  Server Script mein aik validation jo linked Quality Inspection
  check karti hai, aur submit rok deti hai agar inspection missing
  ho ya fail ho. Gate sirf aik `validate` hook hai; jo discipline
  woh lagata hai, wohi asal point hai. Dekhein
  [Lesson 06 — Quality](../learn/erpnext/operations/06-quality.md)
  aur [Lesson 05 — Server Scripts](../learn/framework/level-2/05-server-scripts-events.md).
- **Har truck ke andar aur bahar ke liye Gate Pass.** Raw material
  ki arrivals aur finished goods ki dispatches dono custom Gate
  Pass DocType se guzarti thin, jo
  [Lesson 03](../learn/framework/level-1/03-first-doctype.md) se hai,
  taake guard ka register aur stock ledger aakhir mein aik dosre se
  mil jayein.
- **Costing BOM se, andazay se nahi.** BOM ki valuation rate se pack
  ki asal cost milti thi, aur aik simple script report har mahine
  use selling price se compare karti thi — pehli dafa owner dekh
  saka ke kis product par faida hota hai aur kis par nahi. Dekhein
  [Lesson 08 — Reports & Print Formats](../learn/framework/level-2/08-reports-print-formats.md).
- **Roles ne factory floor ko imandar rakha.** Storekeepers Stock
  Entries bana sakte the lekin submit nahi kar sakte the; submit
  sirf production manager kar sakta tha. Dekhein
  [Lesson 09 — Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md).

### Kya ghalat hua

1. **Quality gate bahut der se lagaya gaya.** Pehla version
   inspection ke baghair Delivery Notes submit hone deta tha,
   kyunke "gate go-live ke baad laga dein ge". Us gap mein aik
   kharab batch bahar chala gaya — wohi failure jise rokne ke
   liye gate bana tha. Fix yeh tha ke gate pehle din se mandatory
   ho, aur "baad mein laga dein ge" wala control kabhi na ho.
   Jo control pehle din enforce nahi hota, woh control hi nahi hai.
2. **Batch numbers haath se type hote the.** Do storekeepers batch
   codes alag tareeqay se type karte the (`BATCH-12` vs
   `batch 12`), to wohi batch reports mein do batches nazar aata
   tha. Fix naming series thi — code system generate karta hai,
   insaan kabhi type nahi karta. Field-layout rules
   [Common Mistakes](common-mistakes.md) guide mein dekhein.

### Results

Taqreeban, pehle teen mahino mein: register aur system ke beech
stock ke disagreements haftay ki behes se nikal kar aik rare
exception ban gaye; gate enforce hone ke baad koi batch passed
inspection ke baghair bahar nahi gaya; aur monthly costing report
ne dikhaya ke aik spice mix cost se kam par bik raha tha — us ki
price usi haftay theek kar di gayi. Is mein koi jaadu nahi tha.
Stock is liye theek tha kyunke har movement aik hi system se
guzarti thi; quality gate is liye kaam karta tha kyunke woh submit
rokta tha, sirf request nahi karta tha.

### Hum isay kaise istemal kar sakte hain

Agar aap kisi manufacturer ke liye bana rahe hain, to wohi teen
cheezon se shuru karein: batch-wise stock, submit rokne wala quality
gate, aur costing report. Gate pehle banayein, go-live se pehle, baad
mein nahi. Aur insaan ko kabhi woh identifier type na karne dein jo
system generate kar sakta hai — naming series isi liye hain.

---

## Case 2 — Aik trading aur distribution business

### Background

Aik distributor — taqreeban 10–15 log, aik warehouse, do delivery
vans — manufacturers se packaged goods khareed kar sheher bhar ki
dukanein supply karta hai. Mahine mein taqreeban 150–200 deliveries,
zyada tar chhoti, zyada tar udhaar par. Business do cheezon par
chalata tha: yeh janna ke har dukaan par kitna udhaar hai, aur yeh
janna ke har van kahan hai.

### Problem

1. **Udhaar yaad-dasht se diya jata tha.** Owner ko pata tha ke
   kaun si dukaan waqt par deti hai aur kaun si nahi — jab tak woh
   chhutti par na jaye, aur kisi aur ko pata na ho. Samaan un
   dukaanon ko bhi chala jata tha jo mahino se peechay thin.
2. **Deliveries phone call se track hoti thin.** Office driver ko
   call karta, driver dukaan ko call karta, dukaan kehti "abhi nahi
   aayi". Aik delivery jo waqai ho chuki hoti, dinon tak "pending"
   rehti, aur us par invoice nahi ban sakta tha.
3. **Warehouse ke andar-bahar ka koi paper trail nahi tha.** Samaan
   warehouse se baghair document ke nikal jata tha, to jab stock
   ghayab hota, to koi tareeqa nahi tha yeh kehne ka ke kab, ya kis
   ki duty par.

### Solution

Taqreeban poora standard ERPNext — yeh case zyada tar standard flow
ko theek tareeqay se use karne ke baare mein hai, us ke aas paas kaam
karne ki bajaye:

- **Standard order-to-cash flow, shuru se end tak enforce.**
  Sales Order → Delivery Note → Sales Invoice → Payment Entry,
  koi step skip nahi. Invoice sirf submitted Delivery Note se ban
  sakti thi, to "delivered lekin invoice nahi bani" aik category hi
  khatam ho gayi. Dekhein
  [Lesson 03 — Selling](../learn/erpnext/core/03-selling.md) aur
  [Lesson 01 — Accounting](../learn/erpnext/core/01-accounting.md).
- **Har Customer par credit limits.** Har dukaan ko us ki payment
  history ke mutabiq credit limit mili, aur system limit se zyada
  ke naye Sales Orders rok deta tha — rule ab aik shakhs ke
  dimaagh mein nahi rehta tha. Overdue invoices ki daily email
  owner ko scheduled report se jati thi. Dekhein
  [Lesson 11 — Scheduler & Background Jobs](../learn/framework/level-3/11-scheduler-jobs.md).
- **Delivery tracking khud Delivery Note se.** Driver ka naam aur
  van Delivery Note par hoti, aur submitted Delivery Note hi
  delivery ka saboot tha — dukaan print format par sign karti, aur
  signed copy office wapas aati. Dekhein
  [Lesson 08 — Reports & Print Formats](../learn/framework/level-2/08-reports-print-formats.md).
- **Warehouse movements ke liye Gate Pass.** Warehouse se nikalne
  wali har load ko us ki Delivery Notes se linked Gate Pass milta
  tha, taake guard ka register din ke end par stock ledger se mil
  jaye. Yeh wohi Gate Pass hai jo
  [Lesson 03](../learn/framework/level-1/03-first-doctype.md) se hai,
  bilkul alag business mein reuse hua.
- **Aik simple dashboard.** Accounts Receivable ageing, aaj ki
  deliveries, aur overdue customers — aik Insights dashboard par,
  jo owner har subah check karta tha. Dekhein
  [Lesson 18 — Insights](../learn/framework/level-4/18-insights.md).

### Kya ghalat hua

1. **Credit limit pehle bahut zyada set ki gayi thi.** Limits purani
   "gut feeling" numbers se copy ki gayi thin, jo generous thin.
   System ne unhein perfectly enforce kiya — aur perfectly aik
   ghalat policy enforce ki. Fix yeh tha ke limits asal payment
   history se set ki jayein (average monthly payment, sab se bara
   mahina nahi), aur har quarter review ki jayein. Automation woh
   rule enforce karti hai jo aap likhte hain, woh nahi jo aap ka
   matlab tha.
2. **Drivers ne signed Delivery Note ki mukhalfat ki.** Paper copy
   extra kaam lagti thi, aur do haftay tak vans baghair us ke
   nikaltay rahe. Fix technical nahi thi: owner ne signed copy ko
   driver ki daily allowance count hone ki shart bana diya. Us ke
   baad process chal pada. Aik system change jise koi follow na
   kare, woh system change hi nahi hai — insaan wala hissa plan
   karein, sirf DocType nahi.

### Results

Taqreeban: kuch mahino mein overdue receivables numayan tor par kam
ho gaye, kyunke late payers ko naye orders banana hi band ho gaye;
"delivered lekin invoice nahi bani" wali list, jo pehle darjanon
entries ki hoti thi, taqreeban zero ho gayi — invoice ab delivery
ke usi din banti hai; aur din ke end par stock reconciliation, jo
pehle storekeeper ko phone calls mein aik ghanta lagta tha, paanch
minute ka kaam ban gaya — do lists ka comparison jo pehle se hi mil
rahi thin.

### Hum isay kaise istemal kar sakte hain

Kisi bhi trading business ke liye, standard flow hi product hai —
aik mahina use as designed chalane se pehle customise na karein.
Credit limits system mein honi chahiye, aik shakhs ki yaad mein
nahi, aur woh payment history se aani chahiye, optimism se nahi.
Aur jab aik naya step mukhalfat ka samna kare, to incentive theek
karein, form nahi.

---

## Case 3 — Aik services company

### Background

Aik chhoti services company — taqreeban 8–12 log — client projects
karti hai: implementation kaam, support contracts, aur kabhi kabhi
fixed-price jobs. Kaam spreadsheet mein track hota tha, hours chat
group mein track hote the, aur invoices mahine ke end par yaad se
likhe jate the. Kisi bhi waqt taqreeban 6–8 active projects, har aik
ka client alag, rate alag, aur "done" ka matlab alag.

### Problem

1. **Kisi ko nahi pata tha ke aik project par faida hota hai ya
   nuksan.** Hours der se ya bilkul record nahi hote the, to project
   ki cost aik andaza thi — aur invoice us se bhi bara andaza tha.
2. **Approvals chat mein hoti thin.** Aik discount, aik free extra,
   scope ki tabdeeli — sab aik message mein agree hota, sab invoice
   ke waqt bhool jata. Client ko promise yaad rehta; company use
   dhoond nahi sakti thi.
3. **Clients kuch dekh nahi sakte the.** Har status ka sawal phone
   call ya message se aata: "mera project kahan hai?", "agli invoice
   kab hai?" Team wohi sawal har haftay jawab deti thi.

### Solution

ERPNext Projects, jis mein Timesheets sab se zyada kaam karti thin:

- **Har engagement ke liye aik Project, us ke neechay Tasks.** Har
  kaam aik Task tha — owner aur due date ke saath — aur har ghanta
  Task se linked Timesheet entry tha. Project ki cost us ki
  Timesheet entries ka sum ban gayi — andaza khatam. Dekhein
  [Lesson 07 — Projects](../learn/erpnext/operations/07-projects.md).
- **Timesheets se Sales Invoices.** Billable hours approved
  Timesheets se seedha invoice mein aate the, taake invoice us
  kaam se milta jo waqai hua. Fixed-price projects milestones ke
  khilaf invoice hote the. Dekhein
  [Lesson 01 — Accounting](../learn/erpnext/core/01-accounting.md).
- **Har cheez ke liye approval Workflow jo paisa kharch karti hai.**
  Discounts, scope changes aur free kaam Sales Order par Workflow
  se guzarte — project lead request karta, owner approve karta —
  taake har promise aik document ki shakal mein ho, chat message
  ki nahi. Dekhein
  [Lesson 10 — Workflows & Assignments](../learn/framework/level-2/10-workflows-assignments.md).
- **Status aur tickets ke liye client portal.** Clients portal mein
  login kar ke apne project ki progress dekhte aur support tickets
  raise karte, call karne ki bajaye. Tickets Helpdesk se guzarte,
  to kuch bhi chat thread mein nahi kho sakta tha. Dekhein
  [Lesson 12 — Support & Portal](../learn/erpnext/people/12-support-portal.md)
  aur [Lesson 19 — Website & Portal](../learn/framework/level-4/19-website-portal.md).
- **Haftay ki project report.** Logged hours, billed hours, aur
  har client par project margin — har Monday subah owner ko
  scheduled job se email hoti. Dekhein
  [Lesson 11 — Scheduler & Background Jobs](../learn/framework/level-3/11-scheduler-jobs.md).

### Kya ghalat hua

1. **Timesheets Friday ko, yaad se bharay jate the.** Team aik
   haftay ke hours aik baar mein log karti thi, matlab hours
   approximate hote — aur "approximate" hamesha upar ki taraf round
   hota tha. Fix 5 baje ki daily reminder aur aik rule tha: do din
   se zyada purani Timesheet bill hone se pehle project lead ki
   approval mangti hai. Hours tab accurate hue jab woh daily hue.
2. **Portal launch hua, lekin kisi client ko bataya hi nahi gaya.**
   Portal aik mahina live raha aur taqreeban kisi ne use nahi kiya,
   kyunke kisi client ko bataya hi nahi gaya tha ke woh hai ya
   login kya hai. Fix har active client ko aik chhoti email thi —
   un ka login aur aik line — "aap ke project ka status ab yahan
   hai" — aur aik haftay mein phone calls kam ho gayi. Aik feature
   jise kisi ko bataya hi na jaye, woh feature hai hi nahi.

### Results

Taqreeban: monthly invoice negotiation khatam ho gaya, kyunke us ki
har line aik approved Timesheet ya milestone ki taraf ishara karti
thi; aik project aadha guzarne par nuksan mein paya gaya, aur us ka
scope end par discover karne ki bajaye usi waqt dobara negotiate
hua; aur haftay ki "mera project kahan hai?" wali calls khatam ho
gayi jab clients khud status dekh sakne lage. Margin report ne sab
se zyada kaam kiya — us ne "kya hum faida kama rahe hain?" ko aik
ehsaas se aik number mein badal diya, jise owner har Monday check
karta tha.

### Hum isay kaise istemal kar sakte hain

Kisi bhi services business ke liye, Timesheet source of truth hai —
baaki sab kuch (invoice, margin, project status) us se derived hai,
to us ki accuracy pehle protect karein. Har paisay ke decision ko
Workflow se guzarein, kyunke chat mein kiya gaya promise aik dispute
hai jo abhi hua nahi. Aur jab portal banayein, to launch karna aadha
kaam hai; clients ko batana dosra aadha hai.

---

## Teenon cases mein kya common hai

1. **Standard flow ne zyada tar kaam kiya.** In mein se kisi
   business ko bari custom app nahi chahiye thi. Manufacturing case
   ko aik gate aur aik custom DocType chahiye thi; trading case ko
   taqreeban kuch custom nahi chahiye tha; services case ko aik
   Workflow aur aik portal chahiye tha. Pehle standard flow use
   karein, customise baad mein.
2. **Har control jo matter karta tha, kuch rokta tha.** Quality
   gate ne submit roka, credit limit ne order roka, approval
   Workflow ne discount roka. Jo control sirf warn karta hai, woh
   control ignore ho jata hai.
3. **Insaan wala hissa hi tay karta tha ke woh kaam kare ga ya
   nahi.** Drivers ko signed copy le jane ke liye incentive chahiye
   tha; timesheets ko daily reminder chahiye thi; clients ko portal
   use karne ke liye email chahiye thi. DocType implementation ka
   aadha hissa hai — dosra aadha woh log hain jo use karte hain.
4. **Ghaltiyan sab avoid ho sakti thin — aur sab pehchani hui thin.**
   Aik gate jo der se laga, limits jo gut feeling se copy ki gayi,
   hours jo yaad se log hue, aik portal jise kisi ko bataya hi nahi
   gaya. Agar aap yeh cases parh kar sochein "hum aisa kabhi nahi
   karein ge", to apne pehle go-live ke baad dobara parhein.

## Apna case study contribute karein

Yeh teen cases shuruat hain, catalogue nahi. Agar aap ne ERPNext
kisi asal business mein ship kiya hai — factory, dukaan, school,
clinic, farm — to use isi shape mein likh kar bhej dein. Naam
anonymise karein, numbers approximate aur imandari se rakhein, aur
batayein ke kya ghalat hua: ghaltiyan hi sab se zyada faide mand
hissa hain. Submit karne ka tareeqa
[CONTRIBUTING.md](../CONTRIBUTING.md) mein dekhein.

## Sources

NexTash mein production ERPNext kaam aur hub ki apni examples se
liye gaye anonymised patterns — [Practice Project](practice-project.md)
ki spice factory, [Lesson 03](../learn/framework/level-1/03-first-doctype.md)
ka Gate Pass, aur
[Food Manufacturing app (fmc)](https://github.com/irfanzahoor/fmc).
Lesson links hub ki apni lessons ki taraf ishara karte hain. Yahan
koi client naam, company naam, quote ya measured metric nahi hai:
har number design se approximate hai.
