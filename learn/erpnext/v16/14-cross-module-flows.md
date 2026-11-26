# Cross-Module Flows — Forecast → MPS → MRP, Sales → Stock → Accounts

## What it does

No module works alone. A sale consumes stock, stock triggers a purchase,
a purchase posts to the ledger, and a forecast drives a production plan.
This lesson is the map of how the modules connect — the three flows that
run every real implementation. If you understand these, you can trace any
number in the system back to the document that created it, and you can
explain to a client why one wrong entry echoes through three modules.

## Core DocTypes

| DocType | What it is |
|---|---|
| Sales Forecast | Expected demand per item, per period — the starting guess. |
| Master Production Schedule | The plan for what to make, by period, from the forecast and real orders. |
| Production Plan | The planner: turns the schedule and Sales Orders into Work Orders and Material Requests. |
| Material Request (Manufacture) | "We need these raw materials to produce." Raised by the Production Plan. |
| Work Order | The production order created from the plan. |
| Purchase Order | Buys the shortfall the plan found. |
| Stock Entry | Moves the materials and posts the finished goods. |
| Sales Order | The confirmed customer order — the other input to the plan. |
| Delivery Note | Ships the goods, moves stock out. |
| Sales Invoice | Books the revenue; the customer owes the money. |
| Payment Entry | Collects it. |

## Flow 1 — forecast → MPS → MRP (planning)

```text
Sales Forecast → Master Production Schedule → Production Plan
   (what we expect to sell)   (what we plan to make)   (what to order + make)
        → Material Request (Manufacture) → Purchase Order → Purchase Receipt
        → Work Order → Job Cards → Stock Entry (Manufacture) → finished stock
```

- The **Sales Forecast** is a guess; the **Master Production Schedule**
  turns it into a make-plan by period; the **Production Plan** explodes
  it into real documents — Work Orders for what you make, Material
  Requests for what you need.
- The plan checks **available stock first**. It only orders what is
  short. A plan run without accurate stock is a plan that orders what you
  already own.
- **MRP** (Material Requirements Planning) is this explosion: demand minus
  stock minus on-order, per item, per date. The Production Plan is where
  ERPNext does it.

## Flow 2 — sales → stock → accounts (the daily loop)

```text
Sales Order → Delivery Note (stock out) → Sales Invoice (revenue) → Payment Entry (cash)
     ↑                ↓
  reserves stock   Bin down, SLE written, ledger posted — one submit, three effects
```

- One submit posts in three places: the **Delivery Note** moves stock,
  the **Sales Invoice** books revenue and the receivable, the **Payment
  Entry** clears it. That is why editing a submitted document is
  forbidden — the three records would disagree.
- The same loop in reverse: Purchase Order → Purchase Receipt (stock in,
  value booked) → Purchase Invoice (liability) → Payment Entry.

## Flow 3 — production → QC → sales (the factory loop)

```text
Work Order → Job Cards → Quality Inspection → finished stock → Delivery Note → invoice
   (make it)    (track it)   (prove it)        (sell it)
```

- Production feeds Quality (lesson 06) and Quality gates Sales: a batch
  that fails inspection never reaches a Delivery Note.
- Batch traceability ties the loop together: the pack a customer holds
  traces to the Work Order, the raw-material batch, the supplier and the
  inspection that passed it.

## Worked example — a spice manufacturer, one month

The fmc demo client ([fmc](https://github.com/irfanzahoor/fmc)) plans
October:

1. **Sales Forecast**: 2,000 kg chilli powder for October, from last
   year's sales plus the new distributor's order.
2. **Master Production Schedule**: make 2,000 kg, 500 kg per week.
3. **Production Plan** runs: stock on hand is 300 kg, so it creates
   **Work Orders** for 1,700 kg and **Material Requests** for 1,800 kg raw
   chilli (allowing process loss). The requests become **Purchase Orders**.
4. Raw chilli arrives (**Purchase Receipt** → **Quality Inspection** →
   accepted into the raw store). **Work Orders** run weekly; **Job Cards**
   log grinding and packing; **Stock Entry (Manufacture)** books 490 kg
   per 500 kg batch.
5. Distributor orders ship: **Delivery Note** (FEFO — oldest batch
   first) → **Sales Invoice** → **Payment Entry**. The ledger shows
   revenue; the stock report shows what is left; the plan for November
   starts from the real numbers, not a guess.

## A real use case

A manufacturer planned in Excel: the planner guessed demand, purchasing
bought from the guess, and production ran out of one raw material while
another piled up. After forecast → MPS → MRP in ERPNext, the plan ran
from real orders and real stock — one material stopped expiring in the
store, and the "we are out of chilli" emergency disappeared from the
weekly meeting.

**How we can use it:** pitch the planning chain (forecast → MPS → MRP)
to every textile, food and spare-parts manufacturer who still plans in
Excel — it is the v16 feature that justifies the upgrade, and the demo
(forecast in, Work Orders and Purchase Orders out) closes the sale. The
sales → stock → accounts loop is the first flow to teach every new user:
one submit, three effects.

## Common mistakes

- **Planning from a stale forecast.** A forecast never updated is a plan
  built on last quarter's guess. Refresh it monthly.
- **Running the plan with wrong stock.** The plan trusts Bin. If stock is
  wrong, the plan orders wrong — fix stock first (Stock Reconciliation).
- **Treating modules as separate systems.** A "stock problem" is often a
  sales problem (no Sales Order) or a buying problem (no Purchase Receipt).
  Trace the flow, don't patch the symptom.
- **Skipping QC in the factory loop.** A batch that fails inspection after
  delivery is a recall; before delivery it is a rework.
- **Forgetting the loop is the audit trail.** Every number in a report
  comes from a document. If a number is wrong, find the document — never
  edit the report.

## Next

You have finished the ERPNext path: Core, Operations, People & Customers,
and v16. The full map is in [learn/erpnext/README.md](../README.md).
