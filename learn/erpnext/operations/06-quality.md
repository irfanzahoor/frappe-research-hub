# Quality — Inspections, QC Quarantine / Release / Hold / Reject

## What it does

Quality decides whether goods are good enough to use, sell or ship — and
keeps the bad ones out of stock. A **Quality Inspection** checks a receipt,
a production batch or a delivery against a **Quality Inspection Template**
(a list of parameters with acceptance values). Goods that fail go to a
quarantine warehouse, not back into sellable stock. **Quality Goals**,
**Procedures** and **Reviews** are the management side: the targets, the
written process, and the regular check that the process is working.

## Core DocTypes

| DocType | What it is |
|---|---|
| Quality Inspection | One inspection: what was checked, against which template, pass or fail. |
| Quality Inspection Template | The checklist: parameters, acceptance values, per item or item group. |
| Quality Inspection Parameter | One measurable check (moisture %, colour, weight) with a value or range. |
| Quality Inspection Reading | One measured value recorded during an inspection. |
| Quality Goal | A measurable target (e.g. "rejection rate under 2%") with an owner. |
| Quality Procedure | The written process for a quality activity. |
| Quality Action | A corrective or preventive action raised from a failure. |
| Quality Review | A periodic review of goals, actions and inspection results. |
| Quality Feedback | Feedback from a customer or internal team about quality. |
| Quality Meeting | The meeting record: agenda, minutes, actions. |

Inspections live in the Stock module (they attach to receipts, deliveries
and production), while goals, procedures and reviews are the quality
management system around them.

## End-to-end flow

```text
Setup:   Quality Inspection Templates per item → quarantine warehouse
In:      Purchase Receipt → Quality Inspection → Accepted / Rejected
Fail:    rejected qty → quarantine warehouse (never into sellable stock)
Fix:     Quality Action (return to supplier, rework, or scrap)
Make:    in-process inspection on the Work Order → out-going inspection
Check:   Quality Inspection report, rejection rate vs Quality Goal
```

- An inspection is linked to a **reference document** — usually a Purchase
  Receipt, a Delivery Note or a Stock Entry. The inspected qty is accepted
  or rejected on that document.
- **Accepted** stock goes to the normal warehouse. **Rejected** stock goes
  to the quarantine warehouse (or is returned). It is never silently added
  to sellable stock.
- A **Quality Goal** turns inspection results into a number the owner
  watches — rejection rate, on-time inspections, complaints per month.
- A **Quality Action** is what happens after a failure: return the lot,
  rework it, change the supplier, or change the process. Without the
  action, the same failure repeats next month.

## Worked example — a spice manufacturer, one rejected lot

The fmc demo client ([fmc](https://github.com/irfanzahoor/fmc)) receives
500 kg of red chilli:

1. **Purchase Receipt** — 500 kg arrive. The item has a Quality Inspection
   Template (moisture ≤ 10%, colour grade A, no stones).
2. **Quality Inspection** — the lab measures moisture 13%. The lot fails.
3. 500 kg go to the **quarantine warehouse**. The 5 kg sample is kept for
   the supplier dispute; the rest is not usable.
4. **Quality Action** — return to supplier, and add a pre-shipment moisture
   check to the supplier's terms. The rejected lot never reaches production,
   so no finished batch is contaminated.
5. The **Quality Goal** "rejection rate under 2%" shows this supplier at
   8% over the quarter — the evidence for switching suppliers.

## A real use case

A food exporter shipped a container that a buyer rejected on arrival for
moisture — the whole shipment was lost. The receipt had never been
inspected because "the supplier is trusted". After incoming inspections
with a quarantine warehouse, bad lots are caught at the gate, and the
rejection report shows which suppliers cost money — before the container
sails.

**How we can use it:** bundle Quality with every Manufacturing and Buying
implementation for food and pharma clients — incoming inspection on
Purchase Receipt is a one-day setup that prevents the most expensive
failure a client can have (a rejected shipment). The Quality Goal
dashboard is the phase-2 sale.

## Common mistakes

- **No quarantine warehouse.** Rejected stock mixed into sellable stock is
  a recall waiting to happen.
- **Inspecting after use.** An inspection on the Delivery Note is too late
  — inspect at receipt, before the material enters production.
- **A template with no numbers.** "Looks fine" is not a parameter. Every
  check needs an acceptance value (moisture ≤ 10%, not "dry enough").
- **Failures with no Quality Action.** The same lot fails next month from
  the same supplier. Log the action, assign an owner, close it.
- **Skipping in-process inspection.** Catching a problem at the finished
  pack stage wastes the whole batch — check during production.

## Next

[07 — Projects](07-projects.md) — tasks, timesheets, costing.
