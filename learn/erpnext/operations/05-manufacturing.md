# Manufacturing — BOM, Work Orders, Job Cards, Production, Subcontracting

## What it does

Manufacturing turns raw material into finished goods — and proves the cost
of every unit that comes out. The recipe is the **BOM** (Bill of Materials),
the order to make something is the **Work Order**, and the work done on the
shop floor is tracked on **Job Cards**. When the Work Order finishes, a
Stock Entry moves raw materials out and finished goods in, and the ledger
books the production cost.

If you skip Manufacturing and just do Stock Entries, you lose the two
things a factory owner cares about: **what it cost** and **where it got
stuck**.

## Core DocTypes

| DocType | What it is |
|---|---|
| BOM | The recipe: finished item + raw materials + operations + cost. One BOM per item (with variants by version). |
| BOM Creator | A faster way to build a multi-level BOM from a finished item downwards. |
| Work Order | "Make 500 kg of this." Carries the BOM, qty, warehouse, planned dates, and status. |
| Job Card | One operation on the shop floor (grinding, packing). Tracks time, operator, and completed qty. |
| Routing | The ordered list of operations a product goes through. |
| Operation | One step: name, workstation, standard time. |
| Workstation | A machine or work centre (grinder, packing line) with an hourly rate. |
| Production Plan | The planner: turns Sales Orders / forecasts into Work Orders and Material Requests. |
| Master Production Schedule | The plan for what to make, by period, before the Production Plan runs. |
| Sales Forecast | Expected demand per item, per period — the input to the schedule. |
| Stock Entry (Manufacture) | The movement: raw materials out, finished goods in. Posted when the Work Order completes. |
| Downtime Entry | Records when a workstation stopped, and why. |
| Subcontracting Order | Send raw material to an outside vendor to do one step (e.g. packing). |
| Subcontracting Receipt | The finished work comes back from the vendor. |
| Subcontracting Inward Order | The reverse (v16): a customer sends you material and you do the work. |

## End-to-end flow

```text
Setup:   Item masters → BOM → Routing + Workstations → Operations
Plan:    Sales Forecast → Master Production Schedule → Production Plan
Order:   Work Order (submit) → materials reserved / transferred to WIP
Make:    Job Card per operation → time logged → Stock Entry (Manufacture)
Cost:    finished goods valued at BOM cost + labour + overhead
Check:   Work Order Summary, Production Plan, Job Card, BOM Cost reports
```

- A Work Order starts from a BOM. Change the BOM and every future Work
  Order changes with it — that is why the BOM, not the Work Order, is the
  master.
- Materials move to the work-in-progress warehouse with a Stock Entry of
  type **Material Transfer for Manufacture**; the finished goods come back
  with **Manufacture**.
- A Job Card is the shop-floor truth: who did it, how long it took, how
  much was made. Without Job Cards you cannot cost labour or find the slow
  operation.
- **Subcontracting** is for the step you do not do yourself: the
  Subcontracting Order sends the material out, the Subcontracting Receipt
  brings the finished work back, and the vendor is paid for the service.

## Worked example — a spice manufacturer, one Work Order

The fmc demo client ([fmc](https://github.com/irfanzahoor/fmc) — Food
Manufacturing for ERPNext) needs 500 kg of red chilli powder:

1. **BOM** for "Chilli Powder 500g pack": 1 kg raw chilli, 0.02 kg
   packaging, operations: cleaning → grinding → packing.
2. **Work Order** for 500 kg. Submit. 500 kg of raw chilli (Batch CH-231)
   moves to the WIP warehouse.
3. **Job Cards**: cleaning (2 hrs), grinding (4 hrs on the grinder
   workstation), packing (3 hrs). Each card logs time and operator.
4. **Stock Entry (Manufacture)**: 500 kg raw chilli consumed, 490 kg powder
   produced (10 kg process loss), packed into 980 packs of 500 g.
5. The packs carry the production batch, so a customer complaint traces
   back to CH-231, the grinder, the operator and the day it was made.

## A real use case

A Lahore spice factory planned production in a notebook and costed it by
feel. They never knew which product actually made money — grinding losses
and packing time were invisible. After BOMs + Work Orders + Job Cards, the
BOM cost report showed the real cost per pack, and the slow operation
(grinding) was visible on the Job Card report — the case for a second
grinder, with numbers.

**How we can use it:** sell Manufacturing to every food, pharma and
textile client as the module that answers "what does it cost?" — and demo
it with fmc, which already has the food-manufacturing flow (batches, FEFO,
QC) built in. Subcontracting is a separate fixed-price add-on for clients
who outsource packing or stitching.

## Common mistakes

- **No BOM, just Stock Entries.** Production without a BOM has no standard
  cost and no variance — you cannot tell if a batch was efficient or
  wasteful.
- **Skipping Job Cards.** Without them, labour cost is a guess and the
  bottleneck operation stays hidden.
- **One warehouse for raw, WIP and finished.** Materials get mixed up and
  "where is it?" has no answer. Separate them.
- **Editing a submitted Work Order to change the qty.** Cancel and amend —
  the Work Order has already reserved and moved stock.
- **Forgetting subcontracting receipts.** Material sent out and never
  received back is stock that quietly disappears from the books.

## Next

[06 — Quality](06-quality.md) — inspections, quarantine, release and
reject.
