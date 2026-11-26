# Stock & Inventory — Warehouses, Batches, Serials, FEFO, Valuation

## What it does

Stock answers two questions: **where is it?** and **what is it worth?**
Every movement — a purchase receipt, a delivery, a transfer, a manufacture —
writes a **Stock Ledger Entry (SLE)**. The SLE is the memory of stock, the
same way the GL Entry is the memory of money. And the same rule applies:
never write it by hand.

## Core DocTypes

| DocType | What it is |
|---|---|
| Item | The master: code, name, group, UOM, valuation method, is-stock-item. |
| Warehouse | A tree (All Warehouses → Main Store → Cold Room). Stock always sits in one warehouse. |
| Stock Entry | Manual movements. Types: Material Issue, Material Receipt, Material Transfer, Manufacture, Repack, Material Transfer for Manufacture. |
| Stock Ledger Entry (SLE) | One stock movement line. Created automatically on submit — **never insert it by hand**. |
| Bin | The balance per Item + Warehouse: `actual_qty`, `projected_qty`, `reserved_qty`. |
| Batch | A production lot with an expiry date. Enables traceability and FEFO. |
| Serial and Batch Bundle | Records exactly which serials / batches a transaction used. |
| Stock Reconciliation | The correct way to fix a wrong balance — with a posting date and a reason. |
| Delivery Note | Moves stock out (selling side). |
| Purchase Receipt | Moves stock in (buying side) and books its value. |

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

Read quantities from **Bin** or from a stock report — never by summing SLE
rows in your own code. And read money from the ledger reports, not from a
document's totals after submit.

## Batches, serials and FEFO

- **Batch** — one production lot. A batch has a manufacturing date and an
  expiry date, so a recall can name the exact lot ("recall batch SP-104",
  not "recall everything").
- **FEFO (First Expiry, First Out)** — pick the batch that expires first.
  Critical for food, pharma and chemicals. ERPNext can auto-select batches
  by expiry, so the store team does not have to remember.
- **Serials** — one unique number per unit (a phone, a machine). The Serial
  and Batch Bundle records which serials left in which delivery.
- **Valuation** — each Item uses **FIFO** or **Moving Average**. FIFO values
  issues at the oldest purchase cost; Moving Average re-computes the average
  on every receipt. Pick per item and leave it alone — changing it mid-year
  rewrites history.

## Worked example — a spice manufacturer, one batch

NexTash's food client (see [fmc](https://github.com/irfanzahoor/fmc))
receives 500 kg of red chilli as **Batch CH-231**, expiry 2027-06-30:

1. **Purchase Receipt** — 500 kg into "Raw Material Store". Bin: 500 kg.
2. Production needs 200 kg. The **Stock Entry (Manufacture)** consumes 200 kg
   from batch CH-231 and adds 190 kg of chilli powder (10 kg process loss).
3. A customer order ships 100 kg of powder. The **Delivery Note** picks the
   oldest powder batch first — FEFO, so nothing expires on the shelf.
4. A quality complaint arrives. The batch number on the pack traces back to
   CH-231, the supplier, the receipt date and every other pack from that lot.

## A real use case

A pharma distributor was losing stock to expiry: the store picked whatever
was nearest, and the oldest batches expired at the back of the shelf. With
batches and FEFO picking, the oldest-expiring stock ships first, and the
Stock Ageing report shows what will expire in the next 90 days — before it
becomes a write-off.

**How we can use it:** offer batch + FEFO + Stock Ageing as a package to
every food and pharma client. It is the same pattern as fmc's batch
traceability — and the demo (receive, produce, ship, trace back) closes the
sale in one meeting.

## Common mistakes

- **Editing Bin or SLE by hand.** Wrong balance? Stock Reconciliation with a
  reason. Hand-edited bins and the ledger disagree forever.
- **No batches for expirable goods.** Without batches there is no FEFO and no
  recall. If it expires, it needs a batch.
- **Summing SLE rows in code to get stock.** Use Bin or the Stock Balance
  report. Summing rows is slow and wrong the moment a backdated entry lands.
- **Changing the valuation method mid-year.** FIFO vs Moving Average is a
  policy decision, not a setting to try. Decide at setup.
- **One warehouse for everything.** Separate raw, finished, quarantine and
  returns warehouses — or "where is it?" has no answer.

## Next

[03 — Selling](03-selling.md) — from quotation to cash.
