# Buying — Purchase Orders, Receipts, Supplier Workflow

## Ye kya karta hai

Buying zaroorat ko shelf par stock aur ek aisa bill bana deta hai jo aap pay
kar sakte hain. Ye Selling ka mirror image hai: Material Request → Purchase
Order → Purchase Receipt → Purchase Invoice → Payment Entry. Wahi discipline
lagti hai — ek document, ek kaam. Purchase Receipt stock andar lata hai;
Purchase Invoice liability book karta hai.

## Core DocTypes

| DocType | Ye kya hai |
|---|---|
| Supplier | Master: name, group, default currency, payment terms, tax details. |
| Material Request | "Humein ye chahiye." Koi bhi department raise kar sakta hai; type Purchase, Transfer ya Manufacture. |
| Request for Quotation | Ek hi items par kai suppliers se price maangein. |
| Supplier Quotation | Ek supplier ka priced jawab. |
| Purchase Order | Ek supplier ko confirmed order: items, qty, rate, delivery date. |
| Purchase Receipt | Samaan aa gaya. Submit par stock andar move hota hai aur stock value book ho jati hai. |
| Purchase Invoice | Supplier ka bill. Submit par liability book ho jati hai. |
| Payment Entry | Invoice ke against diya gaya paisa record karta hai. |
| Purchase Taxes and Charges Template | Purchase invoice par lagne wala tax. |

## End-to-end flow

```text
Material Request → Purchase Order → Purchase Receipt → Purchase Invoice → Payment Entry
   (we need it)     (we order it)     (it arrived)      (we owe for it)   (we pay)
```

- Purchase Receipt stock andar lata hai aur stock value book karta hai.
  Purchase Invoice supplier liability book karta hai. **Ye alag documents
  hain.**
- Invoice receipt se **pehle ya baad** mein aa sakta hai — supplier pehle
  bill bhej sakta hai, ya pehle deliver kar sakta hai. ERPNext inhein item
  aur qty se match karta hai, date se nahi.
- Returns mein original invoice ke against **`is_return = 1` wali Purchase
  Invoice** istemal hoti hai.
- Three-way match hi control hai: Purchase Order (hum ne kya order kiya) vs
  Purchase Receipt (kya aaya) vs Purchase Invoice (humein kis ka bill mila).
  Agar teeno mein farq hai to kuch ghalat hai — pay karne se pehle usay
  dhoondein.

## Amli misaal — ek manufacturer raw material khareedta hai

Ek spice factory ko 500 kg laal mirch chahiye:

1. **Material Request** — production raise karta hai: 500 kg laal mirch,
   Friday tak chahiye.
2. **Request for Quotation** — teen suppliers ko bheja gaya. Do ne jawab
   diya.
3. **Purchase Order** — saste supplier ko: 500 kg at Rs 800/kg, delivery
   Friday. Submit.
4. **Purchase Receipt** — Friday, 500 kg aaye aur tole gaye: 495 kg accept
   hue, 5 kg reject hue (damaged). 495 kg ke liye submit karein. Stock 495
   kg barh gaya; reject kiye gaye 5 kg kabhi stock mein nahi aaye.
5. **Purchase Invoice** — supplier 500 kg ka bill bhejta hai. Invoice
   receipt se match hoti hai: sirf 495 kg accept hue, is liye payable 495
   kg ka hai. 5 kg ka farq payment se **pehle** pakra gaya.
6. **Payment Entry** — agreed terms (30 days) par pay kiya gaya. Ledger: Dr
   Supplier — Cr Bank.

## Asli use case

Ek food manufacturer suppliers ko sirf invoice dekh kar pay karta tha, receipts
match kiye baghair. Kam deliveries ki poori payment mahino tak hoti rahi.
Three-way match ke baad, Accounts Payable report har supplier ke against exact
outstanding dikhati thi, aur ek supplier ki baar baar kam shipments Purchase
Receipt history mein nazar aati thin — renegotiation ke liye saboot.

**Hum isay kaise istemal kar sakte hain:** har buying pitch mein three-way
match (order vs receipt vs invoice) demo karein — ye woh ek screen hai jis se
finance head ko system par bharosa ho jata hai. Manufacturing clients ke liye
flow ko Purchase Order se nahi, production se Material Request se shuru karein,
taake paisa commit hone se pehle zaroorat nazar aaye.

## Aam ghaltiyan

- **Receipt ke baghair invoice se pay karna.** Agar samaan kabhi aaya hi
  nahi to aap ne hawa ke liye pay kar diya. Hamesha pehle receipt match
  karein.
- **Ek supplier, ek price, hamesha ke liye.** Supplier Quotation comparison
  ke baghair koi leverage nahi. Har recurring cheez par do quotes lein.
- **Received qty ke bajaye ordered qty ke liye invoice book karna.** Payable
  us se match karna chahiye jo aaya hai. Short-shipments classic leak hain.
- **Material Request nahi.** Purchasing se seedha uthaye gaye orders asli
  zaroorat ko chhupa dete hain. Request hi audit trail hai — kis ne maanga,
  kya maanga, aur kyun.
- **Qty theek karne ke liye submitted receipt ko edit karna.** Cancel karein
  aur amend karein. Receipt stock post karti hai; usay edit karne se stock
  ledger ghalat ho jata hai.

## Agla

Aap ne Core modules mukammal kar liye: Accounting, Stock, Selling, Buying.
ERPNext path mein agla: **Operations** — Manufacturing, Quality, Projects
aur Assets (Beta).
