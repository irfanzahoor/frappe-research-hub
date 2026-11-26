# Stock & Inventory — Warehouses, Batches, Serials, FEFO, Valuation

## Ye kya karta hai

Stock do sawalon ka jawab deta hai: **ye kahan hai?** aur **ye kis qeemat ka
hai?** Har movement — purchase receipt, delivery, transfer, manufacture —
ek **Stock Ledger Entry (SLE)** likhta hai. SLE stock ki yaad hai, bilkul
waisay hi jaisay GL Entry paisay ki yaad hai. Aur wahi rule lagta hai: isay
kabhi haath se na likhein.

## Core DocTypes

| DocType | Ye kya hai |
|---|---|
| Item | Master: code, name, group, UOM, valuation method, is-stock-item. |
| Warehouse | Ek tree (All Warehouses → Main Store → Cold Room). Stock hamesha ek warehouse mein hota hai. |
| Stock Entry | Manual movements. Types: Material Issue, Material Receipt, Material Transfer, Manufacture, Repack, Material Transfer for Manufacture. |
| Stock Ledger Entry (SLE) | Ek stock movement line. Submit par khud ban jati hai — **isay haath se kabhi insert na karein**. |
| Bin | Har Item + Warehouse ka balance: `actual_qty`, `projected_qty`, `reserved_qty`. |
| Batch | Expiry date wala ek production lot. Traceability aur FEFO mumkin banata hai. |
| Serial and Batch Bundle | Record karta hai ke transaction mein exactly kaun se serials / batches istemal hue. |
| Stock Reconciliation | Ghalat balance ko theek karne ka sahi tareeqa — posting date aur reason ke saath. |
| Delivery Note | Stock bahar bhejta hai (selling side). |
| Purchase Receipt | Stock andar lata hai (buying side) aur uski value book karta hai. |

## End-to-end flow

```text
Setup:   Item masters → Warehouses → opening Stock Reconciliation
In:      Purchase Receipt (submit) → SLE in, Bin up, value booked
Move:    Stock Entry — Material Transfer → SLE out of A, SLE in to B
Out:     Delivery Note (submit) → SLE out, Bin down
Make:    Stock Entry — Manufacture → raw materials out, finished goods in
Fix:     Stock Reconciliation (never edit Bin or SLE by hand)
Check:   Stock Balance, Stock Ledger, Stock Ageing reports
```

Quantities **Bin** se ya kisi stock report se parhein — apne code mein SLE
rows ko sum karke kabhi nahi. Aur paisa ledger reports se parhein, submit ke
baad kisi document ke totals se nahi.

## Batches, serials and FEFO

- **Batch** — ek production lot. Ek batch ki manufacturing date aur expiry
  date hoti hai, is liye recall mein exact lot ka naam liya ja sakta hai
  ("recall batch SP-104", "sab kuch recall karo" nahi).
- **FEFO (First Expiry, First Out)** — woh batch pehle pick karein jiski
  expiry sab se pehle hai. Food, pharma aur chemicals ke liye zaroori hai.
  ERPNext expiry ke hisaab se batches khud select kar sakta hai, is liye
  store team ko yaad rakhne ki zaroorat nahi.
- **Serials** — har unit ke liye ek unique number (ek phone, ek machine).
  Serial and Batch Bundle record karta hai ke kis delivery mein kaun se
  serials gaye.
- **Valuation** — har Item **FIFO** ya **Moving Average** istemal karta hai.
  FIFO issues ko sab se purani purchase cost par value karta hai; Moving
  Average har receipt par average dobaara calculate karta hai. Har item ke
  liye ek pick karein aur usay chhor dein — saal ke beech mein isay badalna
  history dobaara likh deta hai.

## Amli misaal — ek spice manufacturer, ek batch

NexTash ka food client (dekhein [fmc](https://github.com/irfanzahoor/fmc))
500 kg laal mirch **Batch CH-231** ke tor par receive karta hai, expiry
2027-06-30:

1. **Purchase Receipt** — 500 kg "Raw Material Store" mein. Bin: 500 kg.
2. Production ko 200 kg chahiye. **Stock Entry (Manufacture)** batch CH-231
   se 200 kg consume karta hai aur 190 kg mirch powder add karta hai (10 kg
   process loss).
3. Customer ka order 100 kg powder ship karta hai. **Delivery Note** sab se
   purana powder batch pehle pick karta hai — FEFO, is liye shelf par kuch
   expire nahi hota.
4. Ek quality complaint aati hai. Pack par batch number se pata chal jata hai
   ke ye CH-231 hai, supplier kaun tha, receipt date kya thi aur us lot ke
   har doosre pack ka kya hua.

## Asli use case

Ek pharma distributor expiry ki wajah se stock kho raha tha: store jo cheez
nazdeek hoti thi wohi pick karta tha, aur sab se purane batches shelf ke
peechay expire ho jate thay. Batches aur FEFO picking ke saath, sab se pehle
expire hone wala stock pehle ship hota hai, aur Stock Ageing report dikhata
hai ke agle 90 din mein kya expire hoga — write-off banne se pehle.

**Hum isay kaise istemal kar sakte hain:** batch + FEFO + Stock Ageing ko ek
package ke tor par har food aur pharma client ko offer karein. Ye wahi
pattern hai jo fmc ki batch traceability mein hai — aur demo (receive,
produce, ship, trace back) ek hi meeting mein sale close kar deta hai.

## Aam ghaltiyan

- **Bin ya SLE ko haath se edit karna.** Balance ghalat hai? Reason ke
  saath Stock Reconciliation karein. Haath se edit kiye gaye bins aur ledger
  hamesha ke liye alag ho jayenge.
- **Expirable goods ke liye batches nahi.** Batches ke baghair na FEFO hai
  na recall. Agar cheez expire hoti hai to usay batch chahiye.
- **Stock nikalne ke liye code mein SLE rows ko sum karna.** Bin ya Stock
  Balance report istemal karein. Rows ko sum karna slow hai aur usi waqt
  ghalat ho jata hai jab koi backdated entry aa jaye.
- **Saal ke beech mein valuation method badalna.** FIFO vs Moving Average ek
  policy decision hai, try karne wali setting nahi. Setup par decide karein.
- **Sab kuch ke liye ek warehouse.** Raw, finished, quarantine aur returns
  ke liye alag warehouses rakhein — warna "ye kahan hai?" ka koi jawab nahi.

## Agla

[03 — Selling](03-selling.md) — quotation se cash tak.
