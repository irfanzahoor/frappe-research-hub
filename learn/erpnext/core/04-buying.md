# Buying — Purchase Orders, Receipts, Supplier Workflow

## What it does

Buying turns a need into stock on the shelf and a bill you can pay. It is the
mirror image of Selling: Material Request → Purchase Order → Purchase Receipt
→ Purchase Invoice → Payment Entry. The same discipline applies — one
document, one job. A Purchase Receipt moves stock in; a Purchase Invoice
books the liability.

## Core DocTypes

| DocType | What it is |
|---|---|
| Supplier | The master: name, group, default currency, payment terms, tax details. |
| Material Request | "We need this." Can be raised by any department; type Purchase, Transfer or Manufacture. |
| Request for Quotation | Ask several suppliers for a price on the same items. |
| Supplier Quotation | One supplier's priced reply. |
| Purchase Order | The confirmed order to one supplier: items, qty, rate, delivery date. |
| Purchase Receipt | Goods arrive. On submit, stock moves in and the stock value is booked. |
| Purchase Invoice | The supplier's bill. On submit, the liability is booked. |
| Payment Entry | Records the money paid against the invoice. |
| Purchase Taxes and Charges Template | The tax applied to the purchase invoice. |

## End-to-end flow

```text
Material Request → Purchase Order → Purchase Receipt → Purchase Invoice → Payment Entry
   (we need it)     (we order it)     (it arrived)      (we owe for it)   (we pay)
```

- A Purchase Receipt moves stock in and books the stock value. A Purchase
  Invoice books the supplier liability. **They are separate documents.**
- The invoice can arrive **before or after** the receipt — a supplier may
  bill first, or deliver first. ERPNext matches them by item and qty, not
  by date.
- Returns use a **Purchase Invoice with `is_return = 1`** against the
  original invoice.
- The three-way match is the control: Purchase Order (what we ordered) vs
  Purchase Receipt (what arrived) vs Purchase Invoice (what we are billed).
  If the three disagree, something is wrong — find it before paying.

## Worked example — a manufacturer buys raw material

A spice factory needs 500 kg of red chilli:

1. **Material Request** — production raises it: 500 kg red chilli, required
   by Friday.
2. **Request for Quotation** — sent to three suppliers. Two reply.
3. **Purchase Order** — to the cheaper supplier: 500 kg at Rs 800/kg,
   delivery Friday. Submit.
4. **Purchase Receipt** — Friday, 500 kg arrive and are weighed: 495 kg
   accepted, 5 kg rejected (damaged). Submit for 495 kg. Stock goes up by
   495 kg; the rejected 5 kg never enter stock.
5. **Purchase Invoice** — the supplier bills for 500 kg. The invoice is
   matched against the receipt: only 495 kg are accepted, so the payable is
   for 495 kg. The 5 kg difference is caught **before** payment.
6. **Payment Entry** — paid on the agreed terms (30 days). Ledger: Dr
   Supplier — Cr Bank.

## A real use case

A food manufacturer paid suppliers from the invoice alone, without matching
receipts. Short deliveries were paid in full for months. After the
three-way match, the Accounts Payable report showed the exact outstanding
per supplier, and one supplier's repeated short-shipments were visible in
the Purchase Receipt history — the evidence for a renegotiation.

**How we can use it:** demo the three-way match (order vs receipt vs
invoice) in every buying pitch — it is the one screen that makes a finance
head trust the system. For manufacturing clients, start the flow at
Material Request from production, not at the Purchase Order, so the need is
visible before the money is committed.

## Common mistakes

- **Paying from the invoice without the receipt.** If the goods never
  arrived, you just paid for air. Always match receipt first.
- **One supplier, one price, forever.** No Supplier Quotation comparison
  means no leverage. Get two quotes on anything recurring.
- **Booking the invoice for the ordered qty, not the received qty.** The
  payable must match what arrived. Short-shipments are the classic leak.
- **No Material Request.** Orders raised directly by purchasing hide the
  real need. The request is the audit trail — who asked, for what, and why.
- **Editing a submitted receipt to fix a qty.** Cancel and amend. A receipt
  posts stock; editing it leaves the stock ledger wrong.

## Next

You have finished the Core modules: Accounting, Stock, Selling, Buying.
Next in the ERPNext path: **Operations** — Manufacturing, Quality, Projects
and Assets (Beta).
