# Studio, Flow & Insights in Desk (v16.60+)

## What it does

v16.60 (17 Nov 2026) moved three things into the core Desk experience.
**Studio** — the drag-and-drop app builder — merged into Framework, so
small apps are built visually, without code. **Frappe Flow** (alpha) is
the AI harness inside Desk: an LLM that analyses your data and fills
forms, permission-aware, using your own AI keys. **Insights** dashboards
now embed in Desk, so managers see live charts where they work instead of
exporting to Excel. Together they change what a "customisation" is: from a
developer task to something an analyst can build in a day.

## Core pieces

| Piece | What it is |
|---|---|
| Studio | Build a mini-app visually: pages, layouts, data sources, CRUD — no code. Apps are standard Frappe apps under the hood. |
| Frappe Flow | The AI harness in Desk (alpha): ask questions of your data, draft documents, fill forms — the AI only sees what the user may see. |
| Insights Dashboard | A live dashboard in Desk: charts and numbers from ERP data, refreshed on open. |
| Insights Workbook | A set of related queries and charts, worked on like a spreadsheet of live data. |
| Insights Query | One question against the data (SQL or visual builder). |
| Insights Data Source | Where a query reads from: a DocType, a table, or an external database. |
| Insights Chart | One chart built from a query. |

Studio builds apps; Flow talks about your data; Insights shows it. None
of them replaces the modules — they sit on top of them.

## End-to-end flow

```text
Build:   Studio → new mini-app (e.g. gate pass, sample tracking) → publish to Desktop
Ask:     Flow → "which customers are overdue?" → answer from live data, permission-aware
See:     Insights Dashboard → sales, stock, finance charts embedded in Desk
Act:     dashboard number → drill into the document → fix it there
```

- **Studio** is for the small app that does not justify a developer:
  visitor register, gate pass, sample tracking, asset check-in. Build it
  visually, publish it to the Desktop, and it behaves like any other app.
- **Flow** is permission-aware by design: it can only see what the signed-
  in user can see. It does not bypass permissions, and it uses your own AI
  keys — the data goes to your AI provider, not to Frappe.
- **Insights** in Desk means the dashboard is where the work happens.
  Build the query once, put the chart on a dashboard, and the manager opens
  Desk and sees it — no export, no stale spreadsheet.
- v16.61 added **Flow public agents** and an AI assistant that can view
  images — the harness is being extended every month on the new monthly
  release train.

## Worked example — a gate pass app in a day

A factory's gate pass is a paper slip: who took what out, signed by the
guard:

1. In **Studio**, an analyst builds a "Gate Pass" mini-app: a form (item,
   qty, vehicle, driver, purpose), a list view, and an approval step.
2. The app is published to the Desktop. The guard opens it on a phone and
   logs each pass; the store manager approves from Desk.
3. The manager asks **Flow**: "how many gate passes this week, and for
   which items?" — the answer comes from the live data, with the numbers.
4. An **Insights Dashboard** shows passes per day and the top items
   leaving the gate — the first sign of a pilferage pattern, visible
   without anyone running a report.

## A real use case

A client's quality head wanted a sample-tracking register — samples sent
to labs, results back, expiry dates. As a coded app it was a two-week
job; in Studio it was built in a day by an analyst, with the lab results
entering through a form the lab technician could use. The client got the
app in the same week they asked for it — and asked for two more.

**How we can use it:** offer Studio-built mini-apps as a new service
line — fixed-price, built in days, billed per app. Train one NexTash
analyst on Studio so small apps stop consuming developer time. Offer Flow
as a pilot to one friendly client on a test site ("ask your ERP" on their
own data) before selling it widely.

## Common mistakes

- **Building in Studio what belongs in a module.** If the app is really
  Manufacturing or HR, use the module. Studio is for the gap around the
  modules, not a replacement for them.
- **Trusting Flow's answer without checking.** Flow analyses data; it can
  misread it. The answer is a starting point — verify against the report.
- **Dashboards nobody opens.** A dashboard buried three clicks deep is
  decoration. Put the one number that matters on the Desktop.
- **Giving the AI keys nobody owns.** Flow uses your own AI keys — decide
  whose account and budget they are before the pilot, not after the bill.
- **Skipping the permission check.** Flow respects permissions, but the
  underlying roles must be right first — an over-permissioned user makes
  the AI over-informed.

## Next

[14 — Cross-Module Flows](14-cross-module-flows.md) — forecast → MPS →
MRP, sales → stock → accounts.
