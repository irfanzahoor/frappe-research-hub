# Helpdesk — Tickets, SLAs, Support Workflow

## What it does

Helpdesk turns support chaos into a queue: every request becomes an
**HD Ticket** with a type, a priority, an owner, and a clock. The clock is
the **Service Level Agreement** — first response and resolution targets
that the team is measured against. Tickets arrive from email, the customer
portal or a form; agents work them in a team; and the knowledge base
(**HD Article**) answers the question before it becomes a ticket.
Frappe Helpdesk is a separate app (`bench get-app helpdesk`), renumbered
to v16.x in November 2026 — unlimited agents, no per-seat fee.

## Core DocTypes

| DocType | What it is |
|---|---|
| HD Ticket | One request: customer, subject, type, priority, status, agent, SLA. |
| HD Agent | A support agent: who can be assigned tickets. |
| HD Team | A group of agents (e.g. "ERP Support", "Billing"). |
| HD Service Level Agreement | Response and resolution targets per priority and customer. |
| HD Service Level Priority | One priority's targets inside an SLA (e.g. Urgent: 1 hr response). |
| HD Ticket Type | The kind of request: Bug, Question, Feature Request. |
| HD Ticket Priority | Urgent, High, Medium, Low. |
| HD Ticket Status | Open, Replied, Resolved, Closed. |
| HD Customer | A customer in Helpdesk, linked to their ERPNext Customer. |
| HD Article | One knowledge-base article, in a category. |
| HD Article Category | A section of the knowledge base (Getting Started, Billing). |
| HD Saved Reply | A canned response for a common answer. |
| HD Ticket Template | A form template for raising a ticket (fields per type). |

## End-to-end flow

```text
Raise:    email / portal / form → HD Ticket (auto-created, type + priority set)
Assign:   ticket → HD Team → HD Agent (round-robin or manual)
Work:     agent replies, ticket moves Open → Replied → Resolved
Clock:    SLA measures first response and resolution against targets
Close:    customer confirms → Closed; feedback requested
Learn:    repeated questions → HD Article → fewer tickets next month
Check:   ticket ageing, SLA breach, first-response time reports
```

- A ticket has **one owner at a time**. An unassigned ticket is a ticket
  nobody is working on — the queue view makes that visible.
- The **SLA clock** starts when the ticket is created and pauses when the
  agent waits for the customer. Breaches are the report the support lead
  checks every morning.
- **HD Article** is the cheapest support there is: every question answered
  once in the knowledge base is a ticket that never arrives.
- A **Saved Reply** keeps answers consistent — the same question gets the
  same correct answer, whoever is on shift.

## Worked example — NexTash support, one week

A client's user cannot post a Purchase Receipt:

1. She emails support. An **HD Ticket** is auto-created: type Question,
   priority High, customer linked to their ERPNext Customer.
2. The ticket lands in the **"ERP Support" team** queue and is assigned to
   an agent. The SLA says first response within 4 hours.
3. The agent finds the cause — a missing permission on the Purchase Receipt
   DocType — and replies with the fix. Status → Replied.
4. The client confirms it works. Status → Resolved → Closed.
5. The same question arrives from a second client. The agent writes an
   **HD Article** ("Why you cannot submit a Purchase Receipt") and a
   **Saved Reply** pointing to it. The third time, the answer takes 30
   seconds.

## A real use case

A software company ran support from a shared inbox. The same question was
answered five different ways, urgent requests sat behind routine ones, and
nobody knew how many tickets were open. After Helpdesk, the queue showed
the real workload, the SLA report showed first-response time dropping from
a day to two hours, and the knowledge base cut repeat tickets by a third.

**How we can use it:** run NexTash's own client support on Helpdesk — it
is the demo and the tool in one. Then sell it to any client whose support
runs on a shared inbox or WhatsApp: the SLA report is the pitch ("your
customers will know you answer in hours, not days"), and the knowledge
base is the phase-2 sale.

## Common mistakes

- **No SLA.** Without targets, "urgent" is an opinion and response time is
  whatever happened. Set the SLA on day one.
- **Tickets with no owner.** The queue must show unassigned tickets
  prominently — or they rot.
- **Resolving without confirming.** A ticket closed before the customer
  confirms is a ticket that reopens angrier.
- **No knowledge base.** Answering the same question ten times is ten
  tickets that an article would have prevented.
- **Support in a shared inbox.** Email has no queue, no owner, no clock.
  That is exactly what Helpdesk replaces.

## Next

[12 — Support & Portal](12-support-portal.md) — customer portal,
communication, portal users.
