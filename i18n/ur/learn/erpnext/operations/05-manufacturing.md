# Manufacturing — BOM, Work Orders, Job Cards, Production, Subcontracting

## Ye kya karta hai

Manufacturing raw material ko finished goods mein badal deta hai — aur
ye saabit karta hai ke har unit ki cost kya aayi. Recipe hai **BOM** (Bill
of Materials), banane ka order hai **Work Order**, aur shop floor par hua
kaam **Job Cards** par track hota hai. Jab Work Order mukammal hota hai,
to ek Stock Entry raw material bahar nikaalti hai aur finished goods
andar laati hai, aur ledger production cost book kar leta hai.

Agar aap Manufacturing skip kar ke sirf Stock Entries karte hain, to aap
wo do cheezein kho dete hain jin ki factory owner ko parwah hoti hai:
**cost kya aayi** aur **kaam kahan atak gaya**.

## Core DocTypes

| DocType | Ye kya hai |
|---|---|
| BOM | Recipe: finished item + raw materials + operations + cost. Har item ke liye ek BOM (version ke hisaab se variants ke saath). |
| BOM Creator | Multi-level BOM banane ka tez tareeqa, finished item se neeche ki taraf. |
| Work Order | "Is ka 500 kg banao." Is mein BOM, qty, warehouse, planned dates aur status hota hai. |
| Job Card | Shop floor par ek operation (grinding, packing). Time, operator aur completed qty track karta hai. |
| Routing | Operations ki tarteeb wali list jin se product guzarta hai. |
| Operation | Ek step: naam, workstation, standard time. |
| Workstation | Ek machine ya work centre (grinder, packing line) jis ka hourly rate hota hai. |
| Production Plan | Planner: Sales Orders / forecasts ko Work Orders aur Material Requests mein badal deta hai. |
| Master Production Schedule | Kya banana hai, har period ke hisaab se, Production Plan chalne se pehle ka plan. |
| Sales Forecast | Har item ki expected demand, har period ke hisaab se — schedule ka input. |
| Stock Entry (Manufacture) | Movement: raw material bahar, finished goods andar. Work Order mukammal hone par post hoti hai. |
| Downtime Entry | Record karta hai ke workstation kab ruka, aur kyun. |
| Subcontracting Order | Raw material bahar ke vendor ko bhejo taake wo ek step kar de (masalan packing). |
| Subcontracting Receipt | Finished kaam vendor se wapas aata hai. |
| Subcontracting Inward Order | Ulta (v16): customer aap ko material bhejta hai aur aap kaam karte hain. |

## Shuru se akhir tak flow

```text
Setup:   Item masters → BOM → Routing + Workstations → Operations
Plan:    Sales Forecast → Master Production Schedule → Production Plan
Order:   Work Order (submit) → materials reserved / transferred to WIP
Make:    Job Card per operation → time logged → Stock Entry (Manufacture)
Cost:    finished goods valued at BOM cost + labour + overhead
Check:   Work Order Summary, Production Plan, Job Card, BOM Cost reports
```

- Work Order ek BOM se shuru hota hai. BOM badlo to har future Work
  Order us ke saath badal jata hai — isi liye BOM master hai, Work Order
  nahi.
- Material work-in-progress warehouse mein Stock Entry se jata hai jis ki
  type **Material Transfer for Manufacture** hoti hai; finished goods
  **Manufacture** ke saath wapas aate hain.
- Job Card shop-floor ki sachai hai: kis ne kiya, kitna time laga, kitna
  bana. Job Cards ke baghair aap labour ki cost nahi nikaal sakte aur na
  hi slow operation dhoond sakte hain.
- **Subcontracting** us step ke liye hai jo aap khud nahi karte:
  Subcontracting Order material bahar bhejta hai, Subcontracting Receipt
  finished kaam wapas lata hai, aur vendor ko service ki payment milti hai.

## Amli misaal — ek spice manufacturer, ek Work Order

fmc demo client ([fmc](https://github.com/irfanzahoor/fmc) — Food
Manufacturing for ERPNext) ko 500 kg red chilli powder chahiye:

1. **BOM** "Chilli Powder 500g pack" ke liye: 1 kg raw chilli, 0.02 kg
   packaging, operations: cleaning → grinding → packing.
2. **Work Order** 500 kg ke liye. Submit. 500 kg raw chilli (Batch CH-231)
   WIP warehouse mein chala jata hai.
3. **Job Cards**: cleaning (2 hrs), grinding (4 hrs grinder
   workstation par), packing (3 hrs). Har card time aur operator log
   karta hai.
4. **Stock Entry (Manufacture)**: 500 kg raw chilli consume hui, 490 kg
   powder bana (10 kg process loss), 500 g ke 980 packs mein pack hua.
5. Packs par production batch hota hai, is liye customer ki complaint
   CH-231, grinder, operator aur us din tak trace ho jati hai jis din ye
   bana tha.

## Asli use case

Lahore ki ek spice factory production notebook mein plan karti thi aur
cost andaze se nikaalti thi. Unhein kabhi pata nahi chalta tha ke asal
mein kaun sa product paisa bana raha hai — grinding losses aur packing
time nazar nahi aate thay. BOMs + Work Orders + Job Cards ke baad, BOM
cost report ne har pack ki asal cost dikha di, aur slow operation
(grinding) Job Card report par nazar aa gaya — dusre grinder ke liye
case, numbers ke saath.

**Hum isay kaise istemal kar sakte hain:** Manufacturing har food, pharma
aur textile client ko becho, wo module jo "cost kya aayi?" ka jawab deta
hai — aur isay fmc ke saath demo karo, jis mein food-manufacturing flow
(batches, FEFO, QC) pehle se bana hua hai. Subcontracting un clients ke
liye alag fixed-price add-on hai jo packing ya stitching outsource karte
hain.

## Aam ghaltiyan

- **BOM nahi, sirf Stock Entries.** BOM ke baghair production ki koi
  standard cost nahi hoti aur koi variance nahi — aap bata nahi sakte ke
  batch efficient tha ya wasteful.
- **Job Cards skip karna.** In ke baghair, labour cost aik andaza hai aur
  bottleneck operation chhupa rehta hai.
- **Raw, WIP aur finished ke liye ek warehouse.** Material mix ho jata hai
  aur "ye kahan hai?" ka koi jawab nahi hota. Inhein alag rakho.
- **Qty badalne ke liye submitted Work Order edit karna.** Cancel karo aur
  amend karo — Work Order pehle hi stock reserve kar ke move kar chuka
  hota hai.
- **Subcontracting receipts bhool jana.** Bahar bheja gaya material jo
  kabhi wapas nahi aaya, wo stock hai jo khamoshi se books se ghaib ho
  jata hai.

## Agla

[06 — Quality](06-quality.md) — inspections, quarantine, release aur
reject.
