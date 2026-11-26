# Selling — Quotations, Sales Orders, Delivery, Pricing

## What it does

Selling turns a customer's interest into money in the bank — and into stock
leaving the warehouse at the right time. Every step is a document, and every
document has one job. A Delivery Note moves stock; a Sales Invoice books the
sale. Mixing those two jobs up is where selling implementations go wrong.

## Core DocTypes

| DocType | What it is |
|---|---|
| Customer | The master: name, group, territory, default price list, credit limit. |
| Quotation | A priced offer. No stock moves, no money booked. |
| Sales Order | The confirmed order. Reserves stock, promises a delivery date. |
| Delivery Note | Ships the goods. On submit, stock moves out (SLE) and the order becomes "To Bill". |
| Sales Invoice | Books the sale. On submit, revenue + tax post to the ledger and the customer owes the money. |
| Payment Entry | Records the money received against the invoice. |
| Price List / Item Price | What an item costs for a customer group (Retail, Wholesale, Export). |
| Pricing Rule | Automatic discounts: "10% off for orders over Rs 100,000". |
| Sales Taxes and Charges Template | The tax applied to the invoice. |

## End-to-end flow

```text
Quotation → Sales Order → Delivery Note → Sales Invoice → Payment Entry
   (offer)     (promise)      (ship)          (bill)         (collect)
```

- A Quotation can become a Sales Order in one click. The prices carry over.
- A Delivery Note moves stock out; a Sales Invoice books the sale.
- An invoice can be created from the order **without** a delivery — for
  service sales, where nothing physical ships.
- Returns use a **Sales Invoice with `is_return = 1`** against the original
  invoice. Never a negative manual entry.
- A Sales Order can be partially delivered and partially billed. The status
  bar tells you what is left: "To Deliver", "To Bill", "Completed".

## Worked example — a distributor, one order

A retailer orders 200 cartons of cooking oil from Al-Noor Traders:

1. **Quotation** — Rs 2,500 per carton, valid 7 days. The retailer accepts.
2. **Sales Order** — 200 × 2,500 = Rs 500,000. Submit. The order reserves
   200 cartons in the warehouse, and the delivery date is promised.
3. **Delivery Note** — 200 cartons leave "Main Store". Submit. Stock drops
   by 200; the order status becomes "To Bill".
4. **Sales Invoice** — Rs 500,000 + 18% sales tax. Submit. Ledger: Dr
   Customer 590,000 — Cr Sales Income 500,000 — Cr Sales Tax Payable 90,000.
5. **Payment Entry** — the retailer pays by bank transfer. The invoice is
   closed; the order is "Completed".

The same flow works for a service company — skip the Delivery Note and
invoice straight from the order.

## A real use case

A packaging supplier took orders on WhatsApp and wrote deliveries in a
register. Orders were forgotten, deliveries were doubled, and nobody knew
which customer owed what. After moving to Sales Order → Delivery Note →
Sales Invoice, the "To Deliver" list became the morning's work list, and the
Accounts Receivable report showed exactly who owed what, with ageing.

**How we can use it:** make the "To Deliver / To Bill" lists the core of
every sales demo — a business owner sees their pending work in one screen,
and that is what sells the module. Add Pricing Rules for the client's real
discount policy (wholesale slabs, seasonal offers) in the first week, not as
an afterthought.

## Common mistakes

- **Invoicing before delivery (for goods).** The customer owes money for
  stock still in your warehouse. Invoice after the Delivery Note — unless
  the sale is a service.
- **Editing a submitted order to change the qty.** Cancel and amend. An
  edited submitted order and its stock/ledger postings will disagree.
- **One price list for everyone.** Retail, wholesale and export customers
  pay different prices. Set up Price Lists and Item Prices properly, or
  every invoice becomes a manual negotiation.
- **No credit limits.** A Customer with no credit limit can order
  indefinitely. Set limits — ERPNext blocks over-limit orders when
  configured.
- **Delivery Note as an invoice.** It moves stock, it does not book money.
  If the accountant only has the Delivery Note, the sale never happened in
  the books.

## Next

[04 — Buying](04-buying.md) — the mirror image: from need to payment.
