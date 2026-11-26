# Selling — Quotations, Sales Orders, Delivery, Pricing

## Ye kya karta hai

Selling customer ki dilchaspi ko bank mein paisa bana deta hai — aur stock ko
sahi waqt par warehouse se bahar bhejta hai. Har step ek document hai, aur har
document ka ek kaam hai. Delivery Note stock move karta hai; Sales Invoice
sale book karta hai. In do kaamon ko mix karna hi woh jagah hai jahan selling
implementations ghalat ho jati hain.

## Core DocTypes

| DocType | Ye kya hai |
|---|---|
| Customer | Master: name, group, territory, default price list, credit limit. |
| Quotation | Ek priced offer. Na stock move hota hai, na paisa book hota hai. |
| Sales Order | Confirmed order. Stock reserve karta hai, delivery date promise karta hai. |
| Delivery Note | Samaan ship karta hai. Submit par stock bahar move hota hai (SLE) aur order "To Bill" ban jata hai. |
| Sales Invoice | Sale book karta hai. Submit par revenue + tax ledger mein post hote hain aur customer par paisa baaqi ho jata hai. |
| Payment Entry | Invoice ke against milne wala paisa record karta hai. |
| Price List / Item Price | Kisi customer group ke liye item ki qeemat kya hai (Retail, Wholesale, Export). |
| Pricing Rule | Automatic discounts: "Rs 100,000 se zyada ke orders par 10% off". |
| Sales Taxes and Charges Template | Invoice par lagne wala tax. |

## End-to-end flow

```text
Quotation → Sales Order → Delivery Note → Sales Invoice → Payment Entry
   (offer)     (promise)      (ship)          (bill)         (collect)
```

- Quotation ek click mein Sales Order ban sakta hai. Prices saath chali
  jati hain.
- Delivery Note stock bahar bhejta hai; Sales Invoice sale book karta hai.
- Invoice order se delivery ke **baghair** bhi ban sakta hai — service sales
  ke liye, jahan kuch physical ship nahi hota.
- Returns mein original invoice ke against **`is_return = 1` wali Sales
  Invoice** istemal hoti hai. Kabhi negative manual entry nahi.
- Sales Order partially delivered aur partially billed ho sakta hai. Status
  bar batata hai ke kya baaqi hai: "To Deliver", "To Bill", "Completed".

## Amli misaal — ek distributor, ek order

Ek retailer Al-Noor Traders se cooking oil ke 200 cartons order karta hai:

1. **Quotation** — Rs 2,500 per carton, 7 din ke liye valid. Retailer maan
   jata hai.
2. **Sales Order** — 200 × 2,500 = Rs 500,000. Submit. Order warehouse mein
   200 cartons reserve kar deta hai, aur delivery date promise ho jati hai.
3. **Delivery Note** — 200 cartons "Main Store" se nikalte hain. Submit.
   Stock 200 kam ho jata hai; order status "To Bill" ban jata hai.
4. **Sales Invoice** — Rs 500,000 + 18% sales tax. Submit. Ledger: Dr
   Customer 590,000 — Cr Sales Income 500,000 — Cr Sales Tax Payable 90,000.
5. **Payment Entry** — retailer bank transfer se pay karta hai. Invoice
   close ho jati hai; order "Completed" hai.

Yehi flow service company ke liye bhi kaam karta hai — Delivery Note skip
karein aur order se seedha invoice karein.

## Asli use case

Ek packaging supplier WhatsApp par orders leta tha aur deliveries ek register
mein likhta tha. Orders bhool jate thay, deliveries double ho jati thin, aur
kisi ko nahi pata hota tha ke kaun sa customer kitna dena hai. Sales Order →
Delivery Note → Sales Invoice par aane ke baad, "To Deliver" list subah ki
work list ban gayi, aur Accounts Receivable report exactly dikhati thi ke
kaun kitna dena hai, ageing ke saath.

**Hum isay kaise istemal kar sakte hain:** har sales demo mein "To Deliver /
To Bill" lists ko core banayein — business owner apna pending kaam ek screen
par dekhta hai, aur yehi cheez module bechti hai. Client ki asli discount
policy (wholesale slabs, seasonal offers) ke liye Pricing Rules pehle hafte
mein add karein, baad ki soch ke tor par nahi.

## Aam ghaltiyan

- **Goods ke liye delivery se pehle invoicing.** Customer us stock ke liye
  paisa dena hai jo abhi aapke warehouse mein hai. Delivery Note ke baad
  invoice karein — jab tak sale service ki na ho.
- **Qty badalne ke liye submitted order ko edit karna.** Cancel karein aur
  amend karein. Edit kiya hua submitted order aur uski stock/ledger postings
  alag ho jayengi.
- **Sab ke liye ek price list.** Retail, wholesale aur export customers
  alag prices dete hain. Price Lists aur Item Prices sahi se set karein,
  warna har invoice ek manual negotiation ban jata hai.
- **Credit limits nahi.** Bina credit limit ke Customer hamesha order kar
  sakta hai. Limits set karein — configure karne par ERPNext over-limit
  orders ko block karta hai.
- **Delivery Note ko invoice samajhna.** Ye stock move karta hai, paisa book
  nahi karta. Agar accountant ke paas sirf Delivery Note hai to books mein
  sale kabhi hui hi nahi.

## Agla

[04 — Buying](04-buying.md) — mirror image: zaroorat se payment tak.
