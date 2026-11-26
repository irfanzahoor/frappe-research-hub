# Assets — Lifecycle, Depreciation, Maintenance

## What it does

Assets tracks the things a business owns that last more than a year —
machines, vehicles, computers, furniture — from purchase to disposal.
An **Asset** is created from a Purchase Invoice, depreciated on a schedule
so the books show its falling value, maintained on a plan so it does not
break, moved between locations so it is not lost, and scrapped or sold at
the end. Without it, a business owns things it cannot find and depreciates
things it no longer has.

## Core DocTypes

| DocType | What it is |
|---|---|
| Asset | One owned item: value, location, custodian, status, depreciation schedule. |
| Asset Category | The group (Plant & Machinery, Vehicles, IT Equipment) with its accounts and depreciation defaults. |
| Asset Depreciation Schedule | The depreciation plan per finance book: method, rate, dates, amounts. |
| Asset Maintenance | The maintenance plan for an asset: tasks and their frequency. |
| Asset Maintenance Task | One recurring task (oil change every 3 months) in a maintenance plan. |
| Asset Maintenance Log | One completed maintenance event, with cost. |
| Asset Movement | Moving an asset between locations or custodians. |
| Asset Repair | A repair job: what broke, what it cost, when it was fixed. |
| Asset Value Adjustment | Revalue an asset up or down (revaluation or impairment). |
| Asset Capitalization | Capitalize stock items or services into an asset (e.g. building a machine from parts). |
| Location | Where assets live: a tree (Factory → Hall A → Line 1). |

## End-to-end flow

```text
Setup:   Asset Categories (accounts + method) → Locations
Buy:     Purchase Invoice → Asset created (or capitalised from stock)
Value:   Asset Depreciation Schedule runs → depreciation posts to the ledger
Use:     Asset Movement when it changes location or custodian
Care:    Asset Maintenance plan → Asset Maintenance Log per visit
Fix:     Asset Repair when it breaks
End:     sell or scrap → Asset Value Adjustment / disposal, ledger updated
Check:   Fixed Asset Register, Asset Depreciation report
```

- Depreciation methods: **Straight Line** (same amount every period),
  **Written Down Value** (a % of the remaining value), **Double Declining
  Balance**, or **Manual**. Pick per category, not per asset, and do not
  change it mid-life.
- The **Fixed Asset Register** is the audit answer to "what do we own?":
  every asset, its location, its custodian, its book value.
- **Asset Movement** is the control that stops assets walking away — a
  machine moved without a Movement entry is a machine the register cannot
  find.

## Worked example — a factory, one machine

A spice factory buys a grinder for Rs 1,200,000:

1. **Purchase Invoice** — the grinder is booked. An **Asset** is created
   from it, category "Plant & Machinery", location "Factory → Hall A",
   custodian the production supervisor.
2. **Asset Depreciation Schedule** — Straight Line, 10% per year, 10 years.
   Each month Rs 10,000 depreciation posts to the ledger automatically.
3. **Asset Maintenance** — oil change every 3 months, belt check every 6.
   Each visit is logged in an **Asset Maintenance Log** with its cost.
4. Year 3, the motor burns out. **Asset Repair** — Rs 85,000, two days
   downtime. The repair cost is visible against the asset, not hidden in
   general expenses.
5. Year 8, the grinder is sold for Rs 300,000. Book value is Rs 240,000 —
   the Rs 60,000 gain is booked on disposal, and the asset leaves the
   register.

## A real use case

A manufacturer had 40 machines across two halls and no register. When the
auditor asked for the fixed asset list, the accountant guessed from old
invoices — including machines sold years ago. After Assets, the Fixed Asset
Register matched the floor, depreciation posted monthly without manual
journals, and the maintenance log showed which machine cost the most in
repairs — the case for replacing it.

**How we can use it:** offer the Fixed Asset Register as the audit-ready
deliverable in every manufacturing implementation — auditors ask for it by
name, and a client who has it will not go back. Maintenance plans are the
phase-2 sale to any client with plant and machinery.

## Common mistakes

- **Assets booked as expenses.** A Rs 1,200,000 machine in "General
  Expense" breaks the balance sheet and the tax return. Capitalise it.
- **Depreciation as manual journals.** Monthly manual journals drift and
  get forgotten. Use the schedule — it posts itself.
- **No Location or custodian.** An asset with no location is an asset that
  cannot be found. Set both at creation.
- **Repairs hidden in expenses.** If repair cost is not on the asset, you
  cannot see which machine is eating money.
- **Changing the depreciation method mid-life.** It rewrites the book
  value history. Decide at setup, per category.

## Next

[09 — HR](../people/09-hr.md) — employees, leave, payroll, attendance.
