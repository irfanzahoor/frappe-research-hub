# Cross-Module Flows — Forecast → MPS → MRP, Sales → Stock → Accounts

## Ye kya karta hai

Koi module akela kaam nahi karta. Aik sale stock istemal karti hai, stock purchase trigger karta hai, purchase ledger mein post hoti hai, aur forecast production plan chalata hai. Ye lesson us naqshe ka hai ke modules kaise jurtay hain — woh teen flows jo har asli implementation mein chalte hain. Agar aap inhein samajhte hain, to aap system mein kisi bhi number ko us document tak trace kar sakte hain jis ne isay banaya tha, aur aap client ko samjha sakte hain ke aik ghalat entry teen modules mein kyun goonjti hai.

## Core DocTypes

| DocType | Ye kya hai |
|---|---|
| Sales Forecast | Har item, har period ke liye expected demand — shuruati andaza. |
| Master Production Schedule | Har period mein kya banana hai, is ka plan, forecast aur asli orders se. |
| Production Plan | Planner: schedule aur Sales Orders ko Work Orders aur Material Requests mein badalta hai. |
| Material Request (Manufacture) | "Humein produce karne ke liye ye raw materials chahiye." Production Plan se raise hota hai. |
| Work Order | Plan se banaya gaya production order. |
| Purchase Order | Woh kami khareedta hai jo plan ne payi. |
| Stock Entry | Materials ko move karta hai aur finished goods ko post karta hai. |
| Sales Order | Confirm shuda customer order — plan ka doosra input. |
| Delivery Note | Goods ship karta hai, stock bahar move karta hai. |
| Sales Invoice | Revenue book karta hai; customer ko paisay dene hain. |
| Payment Entry | Isay collect karta hai. |

## Flow 1 — forecast → MPS → MRP (planning)

```text
Sales Forecast → Master Production Schedule → Production Plan
   (what we expect to sell)   (what we plan to make)   (what to order + make)
        → Material Request (Manufacture) → Purchase Order → Purchase Receipt
        → Work Order → Job Cards → Stock Entry (Manufacture) → finished stock
```

- **Sales Forecast** aik andaza hai; **Master Production Schedule** isay har period ke liye make-plan mein badal deta hai; **Production Plan** isay asli documents mein explode kar deta hai — jo banana hai us ke liye Work Orders, jo chahiye us ke liye Material Requests.
- Plan pehle **available stock check** karta hai. Ye sirf wohi order karta hai jo kam hai. Aik plan jo ghalat stock ke saath chalaya jaye, woh plan hai jo woh order karta hai jo aap ke paas pehle se hai.
- **MRP** (Material Requirements Planning) yehi explosion hai: demand minus stock minus on-order, har item, har date ke liye. Production Plan woh jagah hai jahan ERPNext ye karta hai.

## Flow 2 — sales → stock → accounts (rozana ka loop)

```text
Sales Order → Delivery Note (stock out) → Sales Invoice (revenue) → Payment Entry (cash)
     ↑                ↓
  reserves stock   Bin down, SLE written, ledger posted — one submit, three effects
```

- Aik submit teen jagah post karta hai: **Delivery Note** stock move karta hai, **Sales Invoice** revenue aur receivable book karta hai, **Payment Entry** isay clear karta hai. Isi liye submitted document ko edit karna mana hai — teenon records mein ikhtilaf ho jayega.
- Wohi loop ulta: Purchase Order → Purchase Receipt (stock in, value booked) → Purchase Invoice (liability) → Payment Entry.

## Flow 3 — production → QC → sales (factory ka loop)

```text
Work Order → Job Cards → Quality Inspection → finished stock → Delivery Note → invoice
   (make it)    (track it)   (prove it)        (sell it)
```

- Production Quality ko feed karta hai (lesson 06) aur Quality Sales ko gate karti hai: aik batch jo inspection mein fail ho jaye, woh kabhi Delivery Note tak nahi pahunchta.
- Batch traceability loop ko jor kar rakhti hai: woh pack jo customer ke paas hai, wo Work Order, raw-material batch, supplier aur us inspection tak trace hota hai jis ne isay pass kiya tha.

## Amli misaal — aik spice manufacturer, aik mahina

fmc demo client ([fmc](https://github.com/irfanzahoor/fmc)) October ki planning karta hai:

1. **Sales Forecast**: October ke liye 2,000 kg chilli powder, pichlay saal ki sales aur naye distributor ke order se.
2. **Master Production Schedule**: 2,000 kg banana hai, har hafte 500 kg.
3. **Production Plan** chalta hai: haath mein stock 300 kg hai, is liye ye 1,700 kg ke liye **Work Orders** aur 1,800 kg raw chilli ke liye **Material Requests** banata hai (process loss ki gunjaish rakh kar). Requests **Purchase Orders** ban jati hain.
4. Raw chilli aa jati hai (**Purchase Receipt** → **Quality Inspection** → raw store mein accept). **Work Orders** haftawar chalte hain; **Job Cards** grinding aur packing log karte hain; **Stock Entry (Manufacture)** har 500 kg batch par 490 kg book karta hai.
5. Distributor ke orders ship hote hain: **Delivery Note** (FEFO — sab se purana batch pehle) → **Sales Invoice** → **Payment Entry**. Ledger revenue dikhata hai; stock report dikhati hai ke kya bacha hai; November ka plan asli numbers se shuru hota hai, andaze se nahi.

## Asli use case

Aik manufacturer Excel mein planning karta tha: planner demand ka andaza lagata, purchasing andaze se khareedti, aur production aik raw material se khali ho jati jab ke doosra dher ho jata. ERPNext mein forecast → MPS → MRP ke baad, plan asli orders aur asli stock se chala — aik material store mein expire hona band ho gaya, aur "humare paas chilli khatam ho gayi" wali emergency haftawar meeting se ghaib ho gayi.

**Hum isay kaise istemal kar sakte hain:** planning chain (forecast → MPS → MRP) har us textile, food aur spare-parts manufacturer ko pitch karo jo ab bhi Excel mein plan karta hai — ye woh v16 feature hai jo upgrade ko justify karta hai, aur demo (forecast andar, Work Orders aur Purchase Orders bahar) sale close kar deta hai. Sales → stock → accounts loop woh pehla flow hai jo har naye user ko sikhana hai: aik submit, teen effects.

## Aam ghaltiyan

- **Purane forecast se planning karna.** Aik forecast jo kabhi update na ho, woh plan hai jo pichlay quarter ke andaze par bana hai. Isay mahana refresh karo.
- **Ghalat stock ke saath plan chalana.** Plan Bin par bharosa karta hai. Agar stock ghalat hai, to plan ghalat order karta hai — pehle stock theek karo (Stock Reconciliation).
- **Modules ko alag systems samajhna.** Aik "stock problem" aksar sales problem hota hai (koi Sales Order nahi) ya buying problem (koi Purchase Receipt nahi). Flow ko trace karo, symptom ko patch na karo.
- **Factory loop mein QC chhor dena.** Aik batch jo delivery ke baad inspection mein fail ho, woh recall hai; delivery se pehle ye rework hai.
- **Bhool jana ke loop hi audit trail hai.** Report mein har number aik document se aata hai. Agar aik number ghalat hai, to document dhoondo — report ko kabhi edit na karo.

## Agla

Aap ne ERPNext path mukammal kar liya hai: Core, Operations, People & Customers, aur v16. Poora map [learn/erpnext/README.md](../README.md) mein hai.
