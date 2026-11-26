# 17 — Studio & Flow

## What it is

Two v16.60 features that change who builds things:

- **Studio** is a visual app builder, merged into the Framework. You
  assemble pages from blocks, bind them to Frappe data, and publish —
  no code. The app lives in the database as **Studio App** and
  **Studio Page** records, and can be exported into a standard Frappe
  app for git and deployment.
- **Flow** is an AI assistant inside Desk (beta, v16.60+). You ask in
  plain language and it works on your site — answers questions about
  live data, creates records, drafts documents. It works with the
  permissions of the person asking, so it can never see or change more
  than they can. It uses your own AI provider keys.

Lesson 13 in the ERPNext path introduced both at feature level. This
lesson is the hands-on version: build one mini-app, ask one question.

## Minimal working example — a Gate Pass mini-app in Studio

Reuse the Gate Pass DocType from Lesson 03 as the data source. Desk →
search **Studio** → New **Studio App**:

| Field | Value |
|---|---|
| App Name | `gate-pass-app` |
| Title | Gate Pass |
| Route | `gate-pass` |
| Home Page | `passes` |

**Page 1 — the list.** New **Studio Page**, route `passes`. Add a
data resource of type **Document List** on DocType **Gate Pass**, then
drag a table block onto the page and bind its rows to that resource
(columns: name, visitor, company, date). This is the page the guard
opens on a phone.

**Page 2 — the form.** New **Studio Page**, route `new-pass`. Add a
data resource of type **Document** on DocType **Gate Pass** (new
document), then drag form blocks bound to its fields: visitor name,
company, purpose, items. Add a submit button that saves the document.

Preview both pages from the Studio toolbar, fix the layout, then
**Publish**. The app is live at `/gate-pass` on your site. To ship it
as code (git, other sites): turn on developer mode, open the app in
Studio, click **Export App**, turn on **Enable App Export**, pick your
Frappe app, and click **Update** — Studio writes it to
`apps/<your_app>/studio/<app_name>/`.

## Minimal working example — one Flow question

Setup first (System Manager only): open `/flow` on your site, choose a
provider (Anthropic, OpenAI, or a custom OpenAI-compatible server such
as Ollama), paste its API key, click **Connect**, and pick the model
new chats start with. Give users the **Flow User** role.

Then, anywhere in Desk, press **Ctrl+I** (Cmd+I on Mac) and ask:

> "Which customers have overdue Sales Invoices, and how much is each
> one owed?"

Flow reads the live data and answers with the numbers — and only the
customers the signed-in user is allowed to see. Ask it to act, and it
will offer to: *"Create a ToDo for the sales manager listing the three
oldest overdue invoices."* Read what it is about to do before you
approve it — Flow can misread data, and an approved action is a real
action (beta).

## When to use — and when not to

| Situation | Use |
|---|---|
| A small app that does not justify a developer | Studio — visitor register, sample tracking, gate pass |
| An analyst needs a form + list in a day | Studio |
| A question about live data ("which orders are late?") | Flow |
| A draft document or a first version of a record | Flow, then verify |
| A full module (Manufacturing, HR, Accounting) | The module — Studio is for the gap around modules, not a replacement |
| A rule that must always hold | Controller code (Lesson 05), never Flow |
| A production change on live data | A human, with a backup — Flow drafts, people decide |

## Common mistakes

- **Building in Studio what belongs in a module.** If the app is
  really Manufacturing or HR, use the module.
- **Trusting Flow's answer without checking.** Verify the numbers
  against the report before acting on them.
- **No owner for the AI keys.** Flow uses your own provider keys —
  decide whose account and budget they are before the pilot, not
  after the bill.
- **Skipping the permission check.** Flow respects permissions, but
  the underlying roles must be right first — an over-permissioned
  user makes the AI over-informed.
- **A Studio app nobody can find.** Publish it, then put it where
  people look: the Desktop, or a link from the module it belongs to.
- **Never exporting the app.** A database-only app cannot go to git
  or to another site. Export it once it works.

## Next

[18 — Insights](18-insights.md) — dashboards on live data, built in
Desk: data source, query, chart, dashboard.
