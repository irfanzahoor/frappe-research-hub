# 04 — Desk, List View, Form View

## Yeh kya hai

**Desk** woh web UI hai jis mein har Frappe user rehta hai. Is ke teen hisse
hain jin ko aap ko samajhna hai: **Workspace** (home screen), **List View**
(records dhoondein), aur **Form View** (aik record par kaam karein). Aap ka
DocType automatically teeno le leta hai — aap ka kaam hai in ko usable
banana.

## Desk shell

- **Sidebar** — modules aur workspaces. Workspaces un DocTypes, reports aur
  dashboards ko group karte hain jo aik role ko chahiye. Aik workspace jis
  ka Module set nahi hai, woh har Desk user ko nazar aata hai — module set
  karein, aur finance/HR workspaces ko role se restrict karein.
- **Search bar (Awesomebar)** — DocType, document ka naam, ya report type
  karein aur seedha wahan pahunch jayein. Isi tarah experienced users
  navigate karte hain; sidebar discovery ke liye hai.
- **Notifications aur assignments** — ghanti, aur forms par "Assigned To"
  list. Kaam user ke paas aata hai, user ko usay dhoondna nahi parta.
- **User menu (upar right)** — "About" batata hai ke site par kaun se
  versions chal rahe hain.

## List View — dhoondna aur triage karna

List View aik sawal ka jawab deti hai: *kin records par tawajju chahiye?*

- **Columns** un fields se aate hain jo `In List View` mark kiye gaye hain
  (max 4–5 — dekhein Lesson 03). Yahi woh hain jin ko user scan karta hai.
  Woh fields chunein jo record ko pehchanti hain: naam, date, party, status,
  amount.
- **Filters** — status, date, company, owner se filter karein. Aik filter ko
  named view ke tor par save karein ("My open orders", "Overdue invoices")
  taake team usay share kare.
- **Sort** — transactions ke liye default newest first hai; jab kaam ko
  oldest-first chahiye to isay badlein (misal ke tor par, sab se purana
  unpaid invoice).
- **Views** — List, Report, Kanban (status ke hisab se), Calendar, Gantt,
  Tree. Kanban pipeline ke liye sahi view hai (leads, support tickets);
  plain list triage ke liye sahi hai.
- **Bulk actions** — rows select karein aur bulk mein Assign, print, export
  ya delete karein.
- **List Settings** (gear icon) — baghair code ke chunein ke kaun se columns
  nazar aayein.

Aik achhi list user ko record seconds mein dhoondne deti hai aur us ki state
aik nazar mein dikhati hai. Aik buri list 12 columns chauri, unfiltered, aur
ghalat sort ke saath hoti hai.

## Form View — aik record par kaam karna

Form View jawab deti hai: *yeh record kya hai, aur is ke saath mujhe kya
karna hai?*

- **Sections aur tabs** — woh layout jo aap ne DocType mein define kiya tha.
  Sections mutaliqa fields ko group karte hain; tabs lambi form ko split
  karte hain (Details / Items / Terms).
- **Child tables** — form ke andar rows (items, taxes). In ka apna section
  aur apne columns hote hain.
- **Status bar** — Draft / Submitted / Cancelled (docstatus), plus workflow
  state jab Workflow active ho.
- **Save / Submit / Cancel / Amend** — Save Draft ko editable rakhta hai.
  Submit isay lock kar deta hai aur us ke effects post karta hai (stock
  moves, GL entries). Cancel un ko reverse karta hai. Amend cancelled wale
  se linked naya Draft banata hai. Submitted document ke fields ko kabhi
  seedha edit na karein.
- **Timeline** — har comment, assignment, attachment aur version change,
  order mein. Yeh audit trail hai — isi liye "bas mujhe call kar lein"
  koi process nahi hai.
- **Actions menu** — Print, Email, Share, Duplicate, aur linked document
  ke liye "New" (misal ke tor par, Sales Order se Sales Invoice).
- **Customize (developer mode mein)** — form se hi field add karein ya label
  change karein. Jaldi fix ke liye handy hai; baad mein isay fixture ke
  tor par ship karein.

## Chhoti si misaal — Desk mein aik subah ka kaam

Aap sales user hain. Subah 9 baje hain.

1. **Selling** workspace kholein — aap ki quotations aur orders wahan hain.
2. **Sales Order → List** kholein, Status = "To Deliver" filter karein,
   Delivery Date se sort karein. Overdue wale upar hain.
3. Pehla order kholein. Form customer, items, taxes, aur status bar ("To
   Deliver and Bill") dikhata hai.
4. Actions menu se **Delivery Note** banayein. Submit karein — stock bahar
   move ho jata hai. Timeline record karta hai ke kis ne kiya aur kab.
5. List mein wapas jayein, order ab "To Bill" parhta hai. **Sales Invoice**
   usi tarah banayein. Ho gaya — order "Completed" hai.

Koi code nahi likha gaya. Yeh pura flow DocTypes, lists aur forms ka apna
kaam karna hai.

## Kis view ko kab use karein

| Job | View |
|---|---|
| Record dhoondna | List, filter ke saath |
| Dekhna ke kya overdue / pending hai | List, sorted aur filtered |
| Pipeline par kaam karna (leads, tickets) | Kanban |
| Aik record enter ya check karna | Form |
| Dekhna ke record ke saath kya kuch hua | Form → Timeline |
| Meeting ke liye export karna | List → Report view ya Export |

## Aam ghaltiyan

- **List ko edit karne ki jagah samajhna.** List dhoondne ke liye hai. Form
  par edit karein — validation, permissions aur timeline wahin hain.
- **List mein zyada columns.** 4–5 se zyada hon to koi list ko scan nahi
  kar sakta.
- **Koi saved filters nahi.** Har user roz "my open orders" dobara banata
  hai. Filter aik dafa save karein, role ke saath share karein.
- **Field ko JS mein chhupa kar "secure" karna.** Chhupana security nahi
  hai — koi bhi field ko API se parh sakta hai. Is ke bajaye permlevel
  (field-level permission) use karein.
- **Timeline ke bajaye memory se kaam karna.** Agar yeh timeline mein nahi
  hai, to yeh hua hi nahi. Comments aur assignments document par hone
  chahiye.
- **Sab ke liye aik workspace.** Aik sales user ko payroll workspace nahi
  chahiye. Workspaces per role hote hain, per site nahi.

## Next

Aap ne Level 1 mukammal kar liya hai. Aap Frappe ko explain kar sakte hain,
bench chala sakte hain, saaf layout ke saath DocType define kar sakte hain,
aur Desk mein kaam kar sakte hain. Level 2 Server Scripts aur Document
Events se shuru hota hai — jahan logic hoti hai.
