# Support & Portal — Customer Portal, Communication, Portal Users

## What it does

The portal is where customers help themselves: they log in and see their
orders, invoices, payments and support tickets — without emailing anyone.
A **Portal User** is a contact given a login linked to a Customer; the
portal shows them only their own documents. Behind it is **communication**:
every email, call and comment on a document is recorded on that document,
so the full history of a customer is one click away. The portal turns
"where is my order?" from a support ticket into a page the customer opens
themselves.

## Core DocTypes

| DocType | What it is |
|---|---|
| Portal User | A login for a customer contact: user, Customer, roles. The child table on Customer that grants portal access. |
| Customer | The master: the portal shows this customer's own orders, invoices and tickets. |
| Contact | The person at the customer: email, phone — becomes a Portal User when given access. |
| HD Customer | The Helpdesk side of a customer: links their tickets to the ERPNext Customer. |
| HD Ticket | What the customer raises and tracks in the portal. |
| Web Form | A public form (lead capture, ticket raising, feedback) that writes into the system. |
| Website Settings | The site configuration behind the portal pages. |
| Issue | The legacy ERPNext support ticket (being replaced by HD Ticket). |
| Email / Comment | Communication recorded on a document — the history of every conversation. |

## End-to-end flow

```text
Setup:   Customer → Contact → Portal User (login + roles)
Visit:   customer logs in → sees their Sales Orders, Invoices, Payments
Ask:     customer raises an HD Ticket from the portal
Track:   ticket status visible in the portal; replies by email + portal
Pay:     customer sees outstanding invoices and pays (where configured)
Check:   portal usage, open tickets per customer, ageing receivables
```

- A Portal User sees **only their own Customer's documents** — User
  Permissions enforce it. A portal login that can see another customer's
  invoices is a data leak; test it with a real portal account before
  go-live.
- Every email and comment is stored **on the document** it belongs to.
  When a customer calls, the history is on their Sales Order or ticket —
  nobody has to search an inbox.
- A **Web Form** is the public front door: a lead form, a ticket form, a
  feedback form. It writes straight into the system, so nothing is
  re-typed.
- For a richer portal (custom pages, dashboards, document libraries),
  build it with **Frappe Builder** — the website builder that ships with
  the Frappe stack.

## Worked example — a distributor, one customer

Al-Noor Traders supplies 200 retailers. One retailer, "Karachi Mart",
keeps calling to ask where its delivery is:

1. A **Contact** (the store manager) is created on the Customer and given
   a **Portal User** login.
2. He logs in and sees his **Sales Orders** (what is promised), **Delivery
   Notes** (what shipped, with dates) and **Sales Invoices** (what is owed).
3. A delivery is short. He raises an **HD Ticket** from the portal — it
   lands in the support queue with his Customer already linked.
4. The agent replies; the answer and the ticket status are visible in the
   portal. The next "where is my order?" call never happens.
5. Month end, the store manager downloads his own statement from the
   portal — no one at Al-Noor has to send it.

## A real use case

A supplier's sales team spent an hour a day answering "where is my order?"
and emailing statements. After the portal, customers checked orders
themselves, statements were self-service, and the support queue shrank —
the team spent the hour selling instead. The portal also became the reason
one big customer stayed: "your competitors make us call for everything."

**How we can use it:** include the portal in every B2B implementation as
the self-service add-on — it is a small setup (Portal Users + permissions)
with a visible payoff the client's customers feel. A Builder-built custom
portal page is a fixed-price upsell for clients who want more than the
standard pages.

## Common mistakes

- **Portal access without testing permissions.** Always log in as a real
  portal user and check they see only their own documents.
- **Portal Users for the wrong contacts.** Only people who should see the
  account get a login — not every email on the account.
- **Communication outside the system.** Deals agreed on WhatsApp and never
  recorded are deals the next person cannot see. Log it on the document.
- **No ticket form in the portal.** If customers can only email, the
  portal is a display window, not a channel. Add the form.
- **Hiding the portal.** A portal nobody is told about is a portal nobody
  uses. Announce it at go-live, with logins sent to every customer.

## Next

[13 — Studio, Flow & Insights](../v16/13-studio-flow-insights.md) — the
new v16 tools in Desk.
