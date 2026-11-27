---
description: "Frappe aur ERPNext mein masala factory end to end banayein — Gate Pass, stock, sales, quality gate, invoicing — 8 guided phases mein."
---

# Practice Project — Masala Factory

Lessons parhne se aap ko pieces samajh aate hain. Yeh project aap ko
sikhata hai ke woh pieces aik saath kaise fit hote hain. Aap aik chhoti
masala manufacturer — **Lal Mirch Foods** — ke liye aik working ERP
banayenge: khaali bench se live order-to-cash flow tak, apni app mein,
apni site par.

Factory kachchi mirch khareedti hai, use pees kar 1 kg ke pack mein Red
Chilli Powder banati hai, distributors ko bechti hai, dispatch se pehle
quality check karti hai, invoice banati hai, aur payment leti hai. Har
step mein aik real ERPNext document use hota hai — wohi jo lessons
sikhate hain — plus aik custom DocType aap ka apna (Lesson 03 wala Gate
Pass).

**Waqt:** taqreeban 3–4 shaamein, har phase taqreeban aik ghanta.
**Nateeja:** aik site jo aap client ko demo kar sakte hain, aur yeh
confidence ke agla project aap scratch se bana sakte hain.

## Shuru karne se pehle

**Aap ko chahiye:** ERPNext v16 ke saath aik working bench (dekhein
[Lesson 02 — Bench, Sites & Apps](../learn/framework/level-1/02-bench-sites-apps.md)).
Phase 2 se pehle [Lesson 03 — Your First DocType](../learn/framework/level-1/03-first-doctype.md)
parh lein — wahan wala Gate Pass hi woh hai jis par aap kaam karenge.

**Demo data** — yeh names har jagah exactly aise hi use karein, taa ke
har phase agle se mil jaye:

| Master | Values |
|---|---|
| Company | Lal Mirch Foods |
| Items | `RAW-CHILLI` — Raw Chilli (Whole), Kg, valuation rate 400 |
| | `RCP-1KG` — Red Chilli Powder 1 Kg Pack, Nos, standard rate 650 |
| Warehouses | Stores, Work In Progress, Finished Goods |
| Customer | Karachi Spice Traders |
| Price List | Standard Selling (default) |

**Flow jo aap bana rahe hain:**

```text
Gate Pass → BOM → Work Order → Stock Entry (Manufacture)
    → Sales Order → Delivery Note → Quality Inspection
    → Sales Invoice → Payment Entry → Report + Print Format
```

Har phase ke end par aik **checkpoint** hai — kuch aisa jo aap ko aage
barhne se pehle karna aana chahiye. Checkpoints skip na karein; agar
Phase 3 ka stock ghalat hai to Phase 4 chup chaap toot jayega.

---

## Phase 1 — Bench, site, app aur masters

**Uses:** [Lesson 02 — Bench, Sites & Apps](../learn/framework/level-1/02-bench-sites-apps.md)

### Steps

1. App aur site banayein:

   ```bash
   cd ~/frappe-bench
   bench new-app spice_factory
   bench new-site spice.local --install-app erpnext
   bench --site spice.local install-app spice_factory
   ```

2. Is site ke liye developer mode on karein, taa ke Desk mein banaye
   gaye DocTypes aap ki app mein save hon:

   ```bash
   bench --site spice.local set-config developer_mode 1
   bench --site spice.local migrate
   bench start
   ```

3. Desk mein upar wali table ke masters banayein:
   **Company** (Lal Mirch Foods), **Item** `RAW-CHILLI` (Item Group
   Raw Material, UOM Kg) aur `RCP-1KG` (Item Group Products, UOM Nos,
   Standard Selling Rate 650), **Warehouses** (Stores, Work In
   Progress, Finished Goods), **Customer** (Karachi Spice Traders).

4. Aik **Stock Entry**, purpose **Material Receipt**, `t_warehouse`
   Stores, valuation rate 400 se 200 kg `RAW-CHILLI` Stores mein
   daal dein. Submit karein. Yeh aap ka opening stock hai — is ke
   baghair Phase 3 ke paas consume karne ko kuch nahi hoga.

### Checkpoint

Ab aap ko browser mein `spice.local` khol kar apni app installed nazar
aani chahiye, aur Stock Balance report mein Stores mein 200 kg
`RAW-CHILLI` milna chahiye.

### Common mistakes

- **App install karne ke baad `migrate` skip karna.** App listed to
  ho jati hai, lekin us ki tables tab tak nahi banti jab tak aap
  migrate na karein.
- **Masters ghalat site par banana.** URL bar mein site ka naam check
  karein — `spice.local`, koi doosri dev site nahi.
- **Developer mode bhool jana.** Is ke baghair Phase 2 ka Gate Pass
  sirf database mein save hota hai, app mein nahi, aur aap use ship
  nahi kar sakte.

---

## Phase 2 — Gate Pass register

**Uses:** [Lesson 03 — Your First DocType](../learn/framework/level-1/03-first-doctype.md),
[Lesson 04 — Desk, List View, Form View](../learn/framework/level-1/04-desk-list-form.md),
[Lesson 06 — Client Scripts](../learn/framework/level-2/06-client-scripts.md)

### Steps

1. **Gate Pass** DocType bilkul Lesson 03 jaisa banayein — wohi fields,
   wohi order:

   | Fieldname | Label | Type | Notes |
   |---|---|---|---|
   | `naming_series` | Series | Select | Options: `GP-.YYYY.-.####` |
   | `gate_pass_date` | Date | Date | Default: Today |
   | `visitor_name` | Visitor | Data | Required |
   | `company` | Company | Link | Options: Company |
   | `purpose` | Purpose | Select | Visit / Delivery / Pickup |
   | `items` | Items | Table | Options: Gate Pass Item |
   | `remarks` | Remarks | Small Text | |

   Child table **Gate Pass Item**: `item_name` (Data, In List View),
   `qty` (Int, In List View), `direction` (Select: In / Out).
   Autoname ko `naming_series` par set karein.

2. Aik Client Script add karein — date khud bhar jaye, aur Delivery
   ya Pickup pass baghair items ke refuse ho jaye:

   ```js
   // spice_factory/spice_factory/doctype/gate_pass/gate_pass.js
   frappe.ui.form.on("Gate Pass", {
       refresh(frm) {
           // New passes always start with today — the guard should not type it.
           if (frm.is_new()) {
               frm.set_value("gate_pass_date", frappe.datetime.nowdate());
           }
       },
       validate(frm) {
           if (
               (frm.doc.purpose === "Delivery" || frm.doc.purpose === "Pickup") &&
               !frm.doc.items.length
           ) {
               frappe.throw(__("Add at least one item for a Delivery or Pickup pass."));
           }
       },
   });
   ```

   `bench --site spice.local migrate` chalakar Desk reload karein.

3. Do passes banayein: aik **Delivery** (supplier 50 kg `RAW-CHILLI`
   lata hai, direction In) aur aik **Visit** (aik buyer, koi items
   nahi). Dono submit karein.

### Checkpoint

Ab aap ko aik minute se kam mein Gate Pass banana aana chahiye, list
mein woh `GP-2026-0001` nazar aana chahiye, aur agar aap baghair items
ke Delivery pass save karne ki koshish karein to saaf error milna
chahiye.

### Common mistakes

- **Client Script ghalat file mein daalna.** Form behaviour
   `gate_pass.js` mein rehta hai, DocType folder ke andar — Server
   Script mein nahi, hooks.py mein nahi.
- **Script add karne ke baad `migrate` bhool jana.** `.js` file tab
   hi pick hoti hai jab DocType app se dobara load ho.
- **`refresh` mein validate karna, `validate` mein nahi.** `refresh`
   har dafa chalta hai jab form khulta hai; wahan check lagane se
   error tab bhi aata hai jab user sirf dekh raha ho.

---

## Phase 3 — Banayein: BOM, Work Order, Stock Entry

**Uses:** [Manufacturing](../learn/erpnext/operations/05-manufacturing.md),
[Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md)

### Steps

1. `RCP-1KG` ke liye aik **BOM** banayein, quantity 1:

   | Item | Qty | UOM |
   |---|---|---|
   | `RAW-CHILLI` | 1.05 | Kg |

   (1 kg powder ke liye 1.05 kg kachchi mirch chahiye — peesne mein
   taqreeban 5% waste hota hai. BOM submit karein.)

2. Aik **Work Order** banayein: `production_item` `RCP-1KG`, qty
   **100**, `bom_no` (BOM se fetch hoga), `fg_warehouse` Finished
   Goods, `wip_warehouse` Work In Progress. Submit karein. Ab Work
   Order plan reserve kar chuka hai: 105 kg kachchi mirch andar, 100
   pack bahar.

3. Work Order ke against aik **Stock Entry**, purpose
   **Manufacture**, post karein:

   | Row | Item | Qty | Source | Target |
   |---|---|---|---|---|
   | 1 | `RAW-CHILLI` | 105 | Stores | — |
   | 2 | `RCP-1KG` | 100 | — | Finished Goods |

   Submit karein. Stock Balance mein ab Stores mein 95 kg
   `RAW-CHILLI` aur Finished Goods mein 100 pack `RCP-1KG` hone
   chahiye.

### Checkpoint

Ab aap ko Stock Ledger se bata sakhna chahiye ke har kilo kahan gaya:
200 andar, 105 consume, 100 pack produce. Agar numbers match nahi kar
rahe to aage na barhein — Phase 4 wohi stock bechta hai jo Phase 3 ne
banaya hai.

### Common mistakes

- **Work Order submit karne se pehle Stock Entry post karna.**
   Manufacture entry ko link karne ke liye submitted Work Order
   chahiye.
- **Ghalat purpose.** Purpose Material Receipt wali Manufacture entry
   stock to move kar deti hai, lekin raw material kabhi consume nahi
   karti — ledger balance nahi karega.
- **Submitted Work Order ko qty badalne ke liye edit karna.** Cancel
   karke amend karein — woh pehle hi stock reserve aur move kar chuka
   hai.

---

## Phase 4 — Bechna: Sales Order → Delivery Note → Sales Invoice

**Uses:** [Selling](../learn/erpnext/core/03-selling.md),
[Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md),
[Accounting](../learn/erpnext/core/01-accounting.md),
[Lesson 05 — Server Scripts & Document Events](../learn/framework/level-2/05-server-scripts-events.md)

### Steps

1. Karachi Spice Traders ke liye aik **Sales Order** banayein: item
   `RCP-1KG`, qty **50**, rate 650, `delivery_date` agle hafte,
   warehouse Finished Goods. Submit karein. (Order-to-cash hamesha
   Quotation → Sales Order → Delivery Note → Sales Invoice →
   Payment Entry hota hai.)

2. Sales Order se **Create → Delivery Note** banayein. Item row check
   karein: us mein `against_sales_order` wapas order ki taraf point
   karta hai, aur warehouse Finished Goods hai. Submit karein — stock
   50 pack reh jayega.

3. Delivery Note se **Create → Sales Invoice** banayein. Totals check
   karein (50 × 650 = 32,500), phir submit karein.

4. Aik guard lagayein taa ke yeh kabhi oversell na ho. `validate` hook
   drafts ko bhi block kar dega, is liye `on_submit` hook karein:

   ```python
   # spice_factory/hooks.py
   doc_events = {
       "Sales Order": {
           "on_submit": "spice_factory.api.check_stock_before_submit",
       },
   }
   ```

   ```python
   # spice_factory/api.py
   import frappe
   from frappe import _


   def check_stock_before_submit(doc, method):
       """Block submitting a Sales Order we cannot fulfil from stock."""
       for row in doc.items:
           if not row.warehouse:
               continue
           available = frappe.db.get_value(
               "Bin",
               {"item_code": row.item_code, "warehouse": row.warehouse},
               "actual_qty",
           ) or 0
           if row.qty > available:
               frappe.throw(
                   _("Not enough stock for {0} in {1}: need {2}, have {3}").format(
                       row.item_code, row.warehouse, row.qty, available
                   )
               )
   ```

   `bench --site spice.local migrate` chalakar test karein: 60 pack ka
   doosra Sales Order (sirf 50 bache hain) submit hone se refuse hona
   chahiye; 40 pack wala pass hona chahiye.

### Checkpoint

Ab aap aik sale ko end to end trace kar sakhte hain: Sales Order
`SO-0001` → Delivery Note → Sales Invoice `SINV-0001`, aur dikha
sakhte hain ke invoice ka `outstanding_amount` payment tak 32,500 hai.

### Common mistakes

- **Delivery se pehle invoice banana.** Invoice money document hai;
   Delivery Note stock document hai. Delivery Note skip karein to stock
   kabhi move nahi hoga.
- **Submit-only rule ke liye `validate` hook karna.** `validate` har
   save par chalta hai, is liye drafts bhi block ho jate hain.
   "Commit karne se mana karna" ke liye `on_submit` sahi event hai.
- **Stock check `frappe.db.sql` se karna.** Bin par
   `frappe.db.get_value` use karein — raw SQL yahan kuch bypass nahi
   karta, lekin yeh aik aadat hai jo doosri jagah permissions torti
   hai. (Lesson 08 dekhein.)

---

## Phase 5 — Dispatch se pehle quality gate

**Uses:** [Quality](../learn/erpnext/operations/06-quality.md)

### Steps

1. `RCP-1KG` ke liye aik **Quality Inspection Template** banayein,
   do parameters ke saath:

   | Parameter | Type | Acceptance |
   |---|---|---|
   | Moisture % | Numeric | Minimum 0, Maximum 10 |
   | Colour | Value-based | Accepted value: Red |

2. `RCP-1KG` **Item** par **Inspection Required before Delivery**
   tick karein aur Quality Inspection Template set karein. Ab se
   ERPNext khud gate enforce karta hai: is item ka Delivery Note tab
   tak submit nahi ho sakta jab tak passing inspection mojood na ho —
   aur rejected inspection use poori tarah block kar deti hai.

3. Doosra Delivery Note banayein (Phase 4 wale 40-pack Sales Order
   se). Item row mein **Quality Inspection** field par click karke aik
   inspection banayein: `inspection_type` **Outgoing**,
   `reference_type` Delivery Note, `sample_size` 5. Readings daalein —
   Moisture 8%, Colour Red — aur submit karein. `status`
   **Accepted** ho jayega.

4. Delivery Note submit karein. Yeh pass ho jayega, kyun ke gate pass
   ho chuka hai.

### Checkpoint

Ab aap aik Delivery Note dikha sakhte hain jo apni inspection pass
hone tak blocked tha, aur bata sakhte hain ke kyun: inspection
transaction ki precondition hai, parallel activity nahi.

### Common mistakes

- **Inspection ghalat type ki banana.** Outgoing dispatch ke liye hai;
   Incoming purchases ke liye; In Process Job Cards ke liye. Ghalat
   type ghalat gate pass karta hai.
- **Template set karna lekin Item checkbox tick na karna.** Template
   akele kuch nahi karta — Item ka inspection flag hi gate on karta
   hai.
- **Dispatch ke baad inspect karna.** Agar maal ja chuka hai to
   inspection sirf paperwork hai. Check Delivery Note submit hone se
   pehle hona chahiye.

---

## Phase 6 — Payment lein, aur gate pass approve karwayein

**Uses:** [Accounting](../learn/erpnext/core/01-accounting.md),
[Lesson 10 — Workflows & Assignments](../learn/framework/level-2/10-workflows-assignments.md)

### Steps

1. Sales Invoice `SINV-0001` khol kar **Create → Payment Entry**
   banayein. Fields check karein: `payment_type` **Receive**,
   `party_type` **Customer**, `party` Karachi Spice Traders,
   `paid_amount` 32,500. **Get Outstanding Invoices** par click
   karein, poori amount `SINV-0001` ke against allocate karein
   (`references` table: `reference_doctype` Sales Invoice,
   `reference_name` invoice, `allocated_amount` 32,500), aur submit
   karein. Invoice ka `outstanding_amount` ab 0 hai aur us ka `status`
   Paid hai.

2. Ab Gate Pass ko approval dein. Aik **Workflow** banayein,
   Document Type **Gate Pass**, Is Active tick karein:

   | State | Docstatus |
   |---|---|
   | Draft | 0 |
   | Pending Approval | 0 |
   | Approved | 1 |
   | Rejected | 0 |

   Transitions: Draft → Pending Approval ("Send for Approval",
   allowed role Gatekeeper), Pending Approval → Approved ("Approve",
   allowed role Manufacturing Manager), Pending Approval → Rejected
   ("Reject", allowed role Manufacturing Manager).

3. Gatekeeper ke tor par aik Gate Pass banakar approval ke liye
   bhejein. Manufacturing Manager user se log in karke use approve
   karein. Dekhein ke Submit button gayab ho gaya hai — ab document
   ko workflow chalata hai.

### Checkpoint

Ab aap aik Paid invoice dikha sakhte hain jis ka outstanding amount
zero hai, aur aik Gate Pass dikha sakhte hain jisay aik hi shakhs bana
aur approve nahi kar sakta.

### Common mistakes

- **Get Outstanding Invoices par click kiye baghair payment allocate
   karna.** `references` table khaali rehti hai, paisa unallocated
   advance ban kar gir jata hai, aur invoice Unpaid rehti hai.
- **Approver role sab ko de dena.** Aik workflow jis mein creator
   apna pass khud approve kar sake, woh control nahi, decoration hai.
- **Workflow inactive chhor dena.** Inactive Workflow kuch nahi
   badalta — purana Submit button rehta hai, aur approval kabhi hoti
   hi nahi.

---

## Phase 7 — Dekhein: Order-to-Cash report + invoice print format

**Uses:** [Lesson 08 — Reports & Print Formats](../learn/framework/level-2/08-reports-print-formats.md)

### Steps

1. Aik **Script Report** "Order to Cash" banayein (Report Type: Script
   Report, Reference DocType: Sales Invoice, Module: aap ki app), is
   code ke saath:

   ```python
   # spice_factory/spice_factory/report/order_to_cash/order_to_cash.py
   import frappe
   from frappe import _


   def execute(filters=None):
       filters = frappe._dict(filters or {})
       return get_columns(), get_data(filters)


   def get_columns():
       return [
           {"label": _("Invoice"), "fieldname": "name", "fieldtype": "Link", "options": "Sales Invoice", "width": 130},
           {"label": _("Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
           {"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 180},
           {"label": _("Grand Total"), "fieldname": "grand_total", "fieldtype": "Currency", "width": 120},
           {"label": _("Outstanding"), "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 120},
           {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
       ]


   def get_data(filters):
       query_filters = {"docstatus": 1}
       if filters.get("customer"):
           query_filters["customer"] = filters.customer
       if filters.get("from_date") and filters.get("to_date"):
           query_filters["posting_date"] = ("between", [filters.from_date, filters.to_date])
       return frappe.get_list(
           "Sales Invoice",
           filters=query_filters,
           fields=["name", "posting_date", "customer", "grand_total", "outstanding_amount", "status"],
           order_by="posting_date desc",
       )
   ```

   ```js
   // spice_factory/spice_factory/report/order_to_cash/order_to_cash.js
   frappe.query_reports["Order to Cash"] = {
       filters: [
           { fieldname: "from_date", label: __("From Date"), fieldtype: "Date", default: frappe.datetime.month_start() },
           { fieldname: "to_date", label: __("To Date"), fieldtype: "Date", default: frappe.datetime.month_end() },
           { fieldname: "customer", label: __("Customer"), fieldtype: "Link", options: "Customer" },
       ],
   };
   ```

   Ise chalakar dekhein: `SINV-0001` mein Grand Total 32,500,
   Outstanding 0, Status Paid nazar aana chahiye.

2. Sales Invoice ke liye aik **Print Format** banayein (Print Format
   Type: Jinja), apni factory ke header aur items table ke saath:

   ```jinja
   <div style="text-align: center;">
     <h2>{{ doc.company }}</h2>
     <p>Tax Invoice — {{ doc.name }}</p>
   </div>
   <p><strong>Customer:</strong> {{ doc.customer_name }}<br>
   <strong>Date:</strong> {{ frappe.utils.formatdate(doc.posting_date) }}<br>
   <strong>Due Date:</strong> {{ frappe.utils.formatdate(doc.due_date) }}</p>
   <table style="width: 100%; border-collapse: collapse;">
     <tr><th style="text-align: left;">Item</th><th>Qty</th><th>Rate</th><th>Amount</th></tr>
     {% for row in doc.items %}
     <tr>
       <td>{{ row.item_name }}</td>
       <td>{{ row.qty }}</td>
       <td>{{ row.get_formatted("rate") }}</td>
       <td>{{ row.get_formatted("amount") }}</td>
     </tr>
     {% endfor %}
   </table>
   <p style="text-align: right;"><strong>Grand Total: {{ doc.get_formatted("grand_total") }}</strong></p>
   ```

   `SINV-0001` ko is se print karke check karein ke totals Desk se
   match karte hain.

### Checkpoint

Ab aap apni report se jawab de sakhte hain ke "kis se kitne paise
lene hain" — aur customer ko aik printed invoice de sakhte hain jo aap
ki factory ki lagti hai, default template ki nahi.

### Common mistakes

- **Query mein filter karne ke bajaye Python mein filter karna.**
   Filters `query_filters` mein rehte hain — har invoice fetch karke
   loop mein filter karna N+1 ghalti hai, report ki shakal mein
   (Lesson 14 dekhein).
- **User-facing read ke liye `frappe.db.sql` use karna.** Yeh tamam
   permission checks bypass kar deta hai. `frappe.get_list` un ka
   ehtram karta hai — wohi use karein.
- **Print format mein company ka naam hard-code karna.**
   `{{ doc.company }}` use karein — format har company par reuse hota
   hai.

---

## Phase 8 — Lock karein: permissions, backup, go-live

**Uses:** [Lesson 09 — Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md),
[Lesson 21 — Ops](../learn/framework/level-4/21-ops.md),
[Go-Live Checklist](go-live-checklist.md)

### Steps

1. Aik **Role** "Gatekeeper" banayein aur use sirf Gate Pass ki
   permissions dein: read, write, create — submit nahi, delete nahi,
   Sales Invoice ya Payment Entry tak access nahi. Ise guard ke user
   ko assign karein. Us user se log in karke confirm karein: Gate Pass
   chalta hai, Sales Invoice nahi khulti.

2. Done kehne se pehle backup lein:

   ```bash
   bench --site spice.local backup
   ```

   Check karein ke file `sites/spice.local/private/backups/` mein
   mojood hai.

3. Is site ke liye [Go-Live Checklist](go-live-checklist.md) par
   chalein: opening balances (aap ki 200 kg receipt), permissions
   (step 1), training (guard ko Gate Pass dikhayein, manager ko
   approval dikhayein), aur rollback plan (step 2 wale backup se
   restore).

### Checkpoint

Ab aap site kisi aur ko de sakhte hain: woh apne role se log in karega,
sirf apna kaam karega, aur agar bench mar jaye to sab kuch backup se
restore ho sakta hai.

### Common mistakes

- **Permissions ko Administrator ke tor par test karna.**
   Administrator ko sab kuch nazar aata hai. Asli user accounts se test
   karein, warna aap ne kuch test hi nahi kiya.
- **Har kaam ke liye aik role.** "Sab kuch karne wala" role hi woh
   tareeqa hai jis se guard invoices cancel karne ke qabil ho jata hai.
- **Go-live se pehle backup na lena.** Pehla backup hamesha disaster
   ke agle din liya jata hai. Abhi lein.

---

## Aage kya banayein

Aap ki factory chal rahi hai. Yeh agle real features hain, usi order
mein jis mein client inhein mangega:

1. **Production Plan** — open Sales Orders se Work Orders khud ba khud
   banayein, haath se banane ke bajaye. Dekhein
   [Manufacturing](../learn/erpnext/operations/05-manufacturing.md).
2. **Batch tracking** — har `RAW-CHILLI` receipt ko Batch No dein aur
   sab se pehle purana stock bechein (FEFO). Dekhein
   [Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md).
3. **Low-stock alert** — aik nightly Scheduler job jo email kare jab
   `RAW-CHILLI` 50 kg se neeche jaye. Dekhein
   [Lesson 11 — Scheduler & Background Jobs](../learn/framework/level-3/11-scheduler-jobs.md).
4. **Distributor portal** — Karachi Spice Traders ko un ke apne orders
   aur invoices dekhne dein, aur kuch nahi. Dekhein
   [Lesson 19 — Website & Portal](../learn/framework/level-4/19-website-portal.md).
5. **Insights dashboard** — monthly sales, outstanding amounts, aur
   stock value aik page par. Dekhein
   [Lesson 18 — Insights](../learn/framework/level-4/18-insights.md).

## Hum isay kaise istemal kar sakte hain

Yeh project woh demo hai jo NexTash pehli meeting mein aik
manufacturing client ko dikhata hai: wohi Gate Pass, wohi masala flow,
wohi quality gate — laptop par chal raha hai, client ke apne numbers
daal kar. Aik prospect jo apna order das minute mein Sales Order se
Paid invoice tak jata dekh le, woh "ERPNext yeh karta hai?" poochna
band karke "hum kab shuru kar sakte hain?" poochne lagta hai.

## Sources

DocType fields ERPNext v16 source (Sales Order, Delivery Note Item,
Stock Entry, Quality Inspection, Payment Entry) aur ERPNext docs
(order-to-cash flow, Quality Inspection enforcement, Payment Entry
references) se verify kiye gaye. Lesson links is hub ki apni lessons ki
taraf point karte hain; Gate Pass fields bilkul
[Lesson 03](../learn/framework/level-1/03-first-doctype.md) jaisi hain.
