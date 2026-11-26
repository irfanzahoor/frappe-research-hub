# Accounting — Chart of Accounts, GL, Invoicing, Payments, Tax

## What it does

Accounting is the module every other module posts into. Selling books
revenue, Buying books cost, Stock books value — and all of it lands in the
same **General Ledger**. If the ledger is wrong, the business's numbers are
wrong, no matter how good the rest of the ERP looks.

## Core DocTypes

| DocType | What it is |
|---|---|
| Company | The legal entity. Every transaction posts to one Company and one Cost Center. |
| Chart of Accounts / Account | The tree of accounts: Asset, Liability, Equity, Income, Expense. |
| Sales Invoice | Bills a customer. On submit it books revenue + tax and creates the receivable. |
| Purchase Invoice | Books a supplier bill. On submit it creates the payable. |
| Payment Entry | Records money in or out, against invoices (or as an advance). |
| Journal Entry | Manual adjustments between accounts — corrections, opening balances, accruals. |
| GL Entry | One ledger line. Created automatically on submit — **never insert it by hand**. |
| Cost Center | Where money belongs (branch, department, project). Every transaction needs one. |
| Sales Taxes and Charges Template | The tax rules applied to a sales invoice (e.g. Sales Tax 18%). |
| Purchase Taxes and Charges Template | The same for purchase invoices. |
| Mode of Payment | Cash, bank, cheque, card — how the money moved. |

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

Two rules run the whole module:

1. **Business state changes only through submit / cancel.** To correct a
   submitted invoice, cancel it and amend it. Never edit its fields, and
   never write GL Entry rows directly.
2. **Balances come from the ledger reports**, not from summing GL Entry in
   code and never from a document's own totals after submit.

## Worked example — a trading company, one day

Al-Noor Traders sells 100 cartons of cooking oil to a retailer:

1. **Sales Invoice** for Rs 500,000 + 18% sales tax (Rs 90,000). Submit.
   Ledger: Dr Customer 590,000 — Cr Sales Income 500,000 — Cr Sales Tax
   Payable 90,000. The customer now owes 590,000.
2. The retailer pays Rs 300,000 by bank transfer. **Payment Entry** against
   the invoice. Ledger: Dr Bank 300,000 — Cr Customer 300,000. Balance
   outstanding: 290,000.
3. The company buys 200 cartons from its supplier: **Purchase Invoice** for
   Rs 400,000 + tax. Ledger: Dr Stock/Expense 400,000 — Cr Supplier.
4. Month end: the accountant opens **Trial Balance** (debits = credits),
   **Profit & Loss** (income − expense), and **Balance Sheet** — all read
   from the same ledger, so they agree with each other by construction.

## A real use case

A Lahore distributor was invoicing in Excel and keeping the bank in a
separate register. Month-end took a week and the tax return was always an
estimate. After moving invoicing and payments into ERPNext, the Sales Tax
Payable account showed the exact liability at any moment, and the return was
filed from the General Ledger report.

**How we can use it:** sell Accounting as the first module in every
implementation — even a client who "only wants stock" needs the ledger, and
the tax template setup (Sales Tax, withholding) is a fixed-price service we
can repeat for every Pakistani client.

## Common mistakes

- **Posting to the wrong Company or Cost Center.** A document without the
  right company posts to the wrong books. Set the default Company per user
  and check it on the first invoice of every implementation.
- **Editing a submitted invoice.** Cancel and amend. An edited submitted
  document and its ledger will disagree forever.
- **Inserting GL Entry rows in code.** The ledger is the system's memory. If
  a posting is missing, the document that should have created it is wrong —
  fix the document, not the ledger.
- **One bank account for everything.** Separate accounts per bank (and per
  currency) or reconciliation becomes guesswork.
- **Tax as a manual line.** Use the tax templates. A typed tax amount is
  wrong the first time the rate changes.

## Next

[02 — Stock & Inventory](02-stock-inventory.md) — where the goods are, and
what they are worth.
