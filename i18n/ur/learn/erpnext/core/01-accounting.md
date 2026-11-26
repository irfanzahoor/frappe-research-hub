# Accounting — Chart of Accounts, GL, Invoicing, Payments, Tax

## Ye kya karta hai

Accounting woh module hai jis mein har doosra module post karta hai. Selling
revenue book karta hai, Buying cost book karta hai, Stock value book karta hai
— aur ye sab ek hi **General Ledger** mein aata hai. Agar ledger ghalat hai to
business ke numbers ghalat hain, chahe baaki ERP kitna hi acha kyun na ho.

## Core DocTypes

| DocType | Ye kya hai |
|---|---|
| Company | Legal entity. Har transaction ek Company aur ek Cost Center mein post hota hai. |
| Chart of Accounts / Account | Accounts ka tree: Asset, Liability, Equity, Income, Expense. |
| Sales Invoice | Customer ko bill karta hai. Submit par ye revenue + tax book karta hai aur receivable banata hai. |
| Purchase Invoice | Supplier ka bill book karta hai. Submit par ye payable banata hai. |
| Payment Entry | Paisa andar ya bahar record karta hai, invoices ke against (ya advance ke tor par). |
| Journal Entry | Accounts ke darmiyan manual adjustments — corrections, opening balances, accruals. |
| GL Entry | Ek ledger line. Submit par khud ban jati hai — **isay haath se kabhi insert na karein**. |
| Cost Center | Paisa kis ka hai (branch, department, project). Har transaction ko ek Cost Center chahiye hota hai. |
| Sales Taxes and Charges Template | Sales invoice par lagne wale tax rules (masalan Sales Tax 18%). |
| Purchase Taxes and Charges Template | Purchase invoices ke liye yehi cheez. |
| Mode of Payment | Cash, bank, cheque, card — paisa kaise move hua. |

## End-to-end flow

```text
Setup:  Company → Chart of Accounts → Tax Templates → Cost Centers
Sell:   Sales Invoice (submit) → GL Entry: Dr Customer, Cr Income + Tax
Pay:    Payment Entry against the invoice → GL Entry: Dr Bank, Cr Customer
Buy:    Purchase Invoice (submit) → GL Entry: Dr Expense/Stock, Cr Supplier
Pay:    Payment Entry against the invoice → GL Entry: Dr Supplier, Cr Bank
Fix:    Journal Entry for anything that is not an invoice or a payment
Check:  General Ledger, Trial Balance, Balance Sheet, Profit & Loss reports
```

Do rules poora module chalatay hain:

1. **Business state sirf submit / cancel se badalti hai.** Submit ki hui
   invoice ko theek karne ke liye usay cancel karein aur amend karein. Uske
   fields kabhi edit na karein, aur GL Entry rows kabhi seedha na likhein.
2. **Balances ledger reports se aate hain**, code mein GL Entry ko sum karke
   nahi, aur submit ke baad kisi document ke apne totals se bhi nahi.

## Amli misaal — ek trading company, ek din

Al-Noor Traders ek retailer ko cooking oil ke 100 cartons bechta hai:

1. **Sales Invoice** Rs 500,000 + 18% sales tax (Rs 90,000) ke liye. Submit.
   Ledger: Dr Customer 590,000 — Cr Sales Income 500,000 — Cr Sales Tax
   Payable 90,000. Ab customer par 590,000 baaqi hai.
2. Retailer bank transfer se Rs 300,000 deta hai. Invoice ke against
   **Payment Entry**. Ledger: Dr Bank 300,000 — Cr Customer 300,000. Baaki
   balance: 290,000.
3. Company apne supplier se 200 cartons khareedti hai: **Purchase Invoice**
   Rs 400,000 + tax ke liye. Ledger: Dr Stock/Expense 400,000 — Cr Supplier.
4. Month end: accountant **Trial Balance** kholta hai (debits = credits),
   **Profit & Loss** (income − expense), aur **Balance Sheet** — ye sab ek hi
   ledger se parhe jate hain, is liye ye apas mein khud hi milte hain.

## Asli use case

Lahore ka ek distributor Excel mein invoicing karta tha aur bank ek alag
register mein rakhta tha. Month-end mein ek hafta lagta tha aur tax return
hamesha andaza hota tha. Invoicing aur payments ERPNext mein le jaane ke
baad, Sales Tax Payable account kisi bhi waqt exact liability dikhata tha,
aur return General Ledger report se file ho gayi.

**Hum isay kaise istemal kar sakte hain:** Accounting ko har implementation
mein pehla module bana kar bechein — aik client jo "sirf stock chahta hai"
usay bhi ledger chahiye hota hai, aur tax template setup (Sales Tax,
withholding) ek fixed-price service hai jo hum har Pakistani client ke liye
dobaara de sakte hain.

## Aam ghaltiyan

- **Ghalat Company ya Cost Center mein posting.** Jo document sahi company
  ke baghair hai, woh ghalat books mein post hota hai. Har user ke liye
  default Company set karein aur har implementation ki pehli invoice par
  isay check karein.
- **Submit ki hui invoice ko edit karna.** Cancel karein aur amend karein.
  Edit ki hui submitted document aur uska ledger hamesha ke liye alag ho
  jayenge.
- **Code mein GL Entry rows insert karna.** Ledger system ki yaad hai. Agar
  koi posting missing hai to woh document ghalat hai jis ne usay banana tha
  — document ko theek karein, ledger ko nahi.
- **Sab kuch ke liye ek bank account.** Har bank (aur har currency) ke liye
  alag accounts rakhein warna reconciliation andaza ban jata hai.
- **Tax ek manual line ke tor par.** Tax templates istemal karein. Likha hua
  tax amount usi waqt ghalat ho jata hai jab rate badalta hai.

## Agla

[02 — Stock & Inventory](02-stock-inventory.md) — samaan kahan hai, aur
uski qeemat kya hai.
