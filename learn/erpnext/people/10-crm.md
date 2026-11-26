# CRM — Leads, Deals, Web Forms (Frappe CRM)

## What it does

CRM turns strangers into customers: capture a **Lead**, qualify it, work
it as a **Deal** through stages, and close it. **Use Frappe CRM — the
separate app — not the legacy CRM inside ERPNext.** The legacy module
(Lead, Opportunity in ERPNext core) is scheduled for deprecation and
will be completely removed in version 17, and Frappe CRM is where all
new development happens: web forms for lead capture, deal pipelines,
enrichment, and workflow automations. In November 2026 it was renumbered
to the Framework scheme (v16.x targets Frappe v16) and runs on ~2,500
paid sites.

## Core DocTypes

| DocType | What it is |
|---|---|
| CRM Lead | One prospect: name, contact, source, status. The top of the funnel. |
| CRM Deal | One opportunity: value, stage, probability, expected close date. |
| CRM Organization | The company a lead or deal belongs to. |
| CRM Task | A follow-up: call, visit, send a quote — with a due date and owner. |
| CRM Call Log | One call: who, when, what was said, next step. |
| FCRM Note | A note on a lead or deal. |
| CRM Lead Status / CRM Deal Status | The pipeline stages (New, Contacted, Qualified, Won, Lost). |
| CRM Service Level Agreement | Response-time targets for leads (first reply within X hours). |
| CRM Form Script | Scripting for the CRM's web forms (validation, defaults). |

Install it with `bench get-app crm` — it is a separate app, not part of
ERPNext core. Leads captured on the website arrive through the CRM's web
forms; a lead becomes a deal when it is qualified, and a deal becomes a
Customer + Quotation in ERPNext when it is won.

## End-to-end flow

```text
Capture:  web form / email / manual → CRM Lead
Qualify:  Lead → contact, understand the need → convert to CRM Deal
Work:     CRM Deal through stages → CRM Task + CRM Call Log per step
Close:    Won → Customer + Quotation in ERPNext → Sales Order
Lose:     Lost → CRM Lost Reason recorded (the data that fixes the funnel)
Check:   CRM dashboard — pipeline value, conversion rate, ageing deals
```

- A **Lead** is unqualified interest; a **Deal** is a qualified
  opportunity with a value. Converting too early fills the pipeline with
  noise; converting too late means nobody follows up.
- Every deal needs a **next step** — a CRM Task with a date and an owner.
  A deal with no next step is a deal that dies quietly.
- **Lost Reason** is the most valuable field in the CRM. "Too expensive"
  ten times in a row is a pricing problem, not a sales problem.
- The CRM has its own **Service Level Agreement**: first response within
  a set time. Leads answered late are leads lost to a competitor.

## Worked example — NexTash, one lead to one project

A food manufacturer fills the "Get a quote" form on the NexTash site:

1. **CRM Lead** created automatically from the web form: company, contact,
   "ERPNext for spice factory", source Website.
2. Irfaan calls the same day. **CRM Call Log**: "wants Manufacturing +
   Quality, 40 users, currently on Excel". Lead status → Qualified.
3. **CRM Deal** created: value Rs 1,800,000, stage "Proposal", close date
   next month. **CRM Tasks**: send proposal (Tue), follow-up call (Fri).
4. The client accepts. Deal → Won. A **Customer** and **Quotation** are
   created in ERPNext, and the work starts as a **Project** (see lesson 07).
5. The dashboard shows the funnel: 12 leads this month, 5 qualified, 2
   won — and the lost deals say "no budget this quarter", which is a
   follow-up list for next quarter, not a dead end.

## A real use case

A distributor's sales team kept leads in personal WhatsApp chats. When a
salesperson left, the leads left with him. After Frappe CRM, every lead is
in the system with an owner and a next step, the manager sees the whole
pipeline in one dashboard, and a lead unanswered for 24 hours is visible —
not discovered a month later.

**How we can use it:** use Frappe CRM for NexTash's own pipeline first —
it is the demo every sales call starts from. Then sell it to every client
whose sales run on WhatsApp and memory: unlimited agents, no per-seat fee,
and the web form turns their website into a lead machine. Always install
Frappe CRM on new projects; never start a client on the legacy ERPNext CRM.

## Common mistakes

- **Using the legacy ERPNext CRM.** It is scheduled for removal in v17.
  New implementations go on Frappe CRM, full stop.
- **Leads with no owner and no next step.** An unowned lead is a lost
  lead. Every lead needs an owner the day it arrives.
- **No Lost Reason.** A lost deal without a reason teaches nothing.
  Record it every time.
- **Deals stuck at one stage for weeks.** An ageing deal is a dead deal
  with the stage left open. Review the pipeline weekly and close or
  re-date.
- **No web form.** If leads only arrive by phone, the website is doing
  nothing. The form is a one-hour setup.

## Next

[11 — Helpdesk](11-helpdesk.md) — tickets, SLAs, support workflow.
