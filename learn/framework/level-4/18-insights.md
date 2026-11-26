# 18 — Insights

## What it is

Insights turns live ERP data into dashboards — no exports, no stale
spreadsheets. Since v16.60 the dashboards embed in Desk, where managers
already work. Four pieces, in order:

| Piece | What it is |
|---|---|
| **Data Source** | Where the data lives: a DocType table, or an external database (MySQL, PostgreSQL, DuckDB, BigQuery) |
| **Query** | One question against the data — built visually (Source, Join, Filter, Group & Summarise) or in SQL |
| **Chart** | One visualisation of a query: Number, Bar, Line, Row, Table, Pie |
| **Dashboard** | Charts arranged on a grid, with filters — the page the manager opens |
| **Workbook** | The folder that holds a set of queries, charts and dashboards, with its own permissions |

## Minimal working example — a sales dashboard in Desk

Open **Insights** in Desk. Everything below happens inside one
Workbook.

**1. Workbook.** Click **+ New Workbook**, name it `Sales Overview`.

**2. Query.** A new workbook starts with a query — pick the source
table `Sales Invoice`. Then add operations in order:

```text
Source:  Sales Invoice
Filter:  docstatus = 1  AND  posting_date is this month
Group:   by customer, Sum of grand_total
```

Save the query as `Monthly Sales by Customer`. A query is reusable —
every chart below reads from it, so the logic lives in one place.

**3. Charts.** Click **+ New Chart** twice:

- **Number chart** "Revenue this month": the Sum of `grand_total`
  from the query — the one number on top.
- **Bar chart** "Revenue by customer": customer on one axis,
  `grand_total` on the other.

**4. Dashboard.** Click **+ New Dashboard**, name it `Sales
Overview`. Drag the two charts from the left panel onto the grid —
Number on the first row, Bar below it. Click **Filter**, add a filter
on `company`, so a manager with two companies sees one at a time.

Open the dashboard tomorrow and the numbers are current — Insights
queries run against live data, not a copy. Put the dashboard where it
gets opened: link it from the Desktop or the Selling workspace.

## When to use — and when not to

| Situation | Use |
|---|---|
| "How are we doing this month?" | Insights dashboard in Desk |
| One question, many views | One query, several charts |
| A number the owner checks daily | Number chart on the first row |
| A one-off question for one user | Report Builder or a saved list filter — not a dashboard |
| A printed document (invoice, gate pass) | Print Format (Lesson 08), not Insights |
| Data that must be frozen at month end | A report exported to file — a live dashboard moves |

## Common mistakes

- **Dashboards nobody opens.** A dashboard buried three clicks deep
  is decoration. Put the one number that matters where people look.
- **One query per chart.** Build the query once, chart it many ways.
  Ten copies of the same logic drift apart.
- **No filter on a multi-company dashboard.** Every chart shows all
  companies mixed together. Add the company filter.
- **A chart for every question.** Five charts that answer one question
  hide the answer. One chart, one question.
- **Sharing the workbook with everyone.** Workbooks carry their own
  permissions — share with the roles that may see the data, not the
  whole site.
- **Trusting a chart without checking the query.** A wrong filter
  makes a confident-looking wrong number. Read the query first.

## Next

[19 — Website & Portal](19-website-portal.md) — the public side of
Frappe: web pages, Web Forms, and the customer portal.
