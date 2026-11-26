# Choosing Apps — When to Install One vs Build It

Every app you install is a dependency you will carry at every upgrade.
An app that saves two days today and breaks the next upgrade costs two
weeks. This guide is the decision process NexTash uses before any
`bench get-app` — on a client project or on our own sites.

## The 5 questions — ask them before installing anything

No app gets installed until all five have an answer, in writing, on the
project note:

1. **Does it solve a real problem on a real project?** Not "it looks
   useful" — a named client, a named pain, this month. An app installed
   "for later" is a dependency with no owner.
2. **Is it maintained?** Check the repo: a release in the last 6 months,
   open issues getting answers, stars as a rough signal only. A repo with
   no commit in a year is a dead app walking — you will be its maintainer.
3. **Does it match your Frappe / ERPNext version?** It needs a branch for
   your version — `version-14`, `version-15`, `version-16` — or a README
   that says so. "Works on v15" is not "works on v16".
4. **Does it have a migration path out?** Can you export the data and
   uninstall cleanly? If removing it means losing the data or hand-editing
   the database, you do not own the data — the app does.
5. **Who owns it when it breaks?** A named person, not "the team". If
   nobody owns it, it breaks on the client's busiest day and nobody knows
   whose job it is.

One "I don't know" is fine — test it on staging and find out. Two or
more "I don't know" means do not install it yet.

## Install it — when someone else already solved it well

Install when the problem is a whole module, the app is official or
well-maintained, and building it would take weeks:

| Need | Install | Why |
|---|---|---|
| CRM | [Frappe CRM](https://github.com/frappe/crm) — `bench get-app https://github.com/frappe/crm` | Official, actively developed, web forms + pipeline. See [CRM lesson](../learn/erpnext/people/10-crm.md). |
| Support desk | [Frappe Helpdesk](https://github.com/frappe/helpdesk) | Official, SLAs + portal + knowledge base. See [Helpdesk lesson](../learn/erpnext/people/11-helpdesk.md). |
| HR | Frappe HRMS (hrms app) | Official HR: leave, attendance, payroll. See [HR lesson](../learn/erpnext/people/09-hr.md). |
| Chat | Raven (official, github.com/frappe/raven) | Team chat inside Desk; v3 is the current version. |
| POS | [POSNext](https://github.com/BrainWise-DEV/POSNext) (v15+, offline mode) or [POS Prime](https://github.com/ravindu2012/pos-prime) (v14/v15/v16, zero core changes) | A POS is a product, not a feature — never build one from scratch. |
| Dashboards | [Frappe Insights](https://github.com/frappe/insights) | Official BI on live data. Note: v3.50 removed v2 — migrate v2 dashboards first. |
| WhatsApp | [Frappe WhatsApp Suite](https://github.com/shridarpatil/frappe_whatsapp) (+ chat UI + chatbot) or official [WABA Integration](https://github.com/frappe/waba_integration) | The channel clients in Pakistan actually read. |

Rule of thumb: **if the app is official Frappe code, install it first and
argue later.** Official apps get version branches, upgrade patches and a
migration path — the three things that cost you at upgrade time.

## Build it — when the gap is small and specific

Build when the need is one register, one form, one small workflow — not a
whole module:

- **A gate-pass register, a sample tracker, a visitor log.** A Studio
  mini-app, built visually in a day by an analyst (see
  [Studio, Flow & Insights](../learn/erpnext/v16/13-studio-flow-insights.md)).
  Installing a whole app for one register is like hiring a company to
  fix a tap.
- **One extra field or one small rule on an existing DocType.** A Custom
  Field (as a fixture) or a Server Script — not an app, not a fork.
  See [Server Scripts](../learn/framework/level-2/05-server-scripts-events.md).
- **A gap nobody has built for.** Pakistan payments are the real example:
  there is no free public Easypaisa / JazzCash app — the catalog's
  biggest gap. That is a build (on Payment Core,
  github.com/aerele/payment-core), and it is a product opportunity, not
  just a project task.

If the build is under a day in Studio or a week in code, build it. If it
is over a month, look for an app again — or charge the client for the
build honestly, as a product, not a favour.

## Extend it — the middle path

Most real work is neither install nor build — it is extending what is
already there, from your own app:

- Custom Fields and Property Setters, exported as fixtures.
- Server Scripts for one quick rule (see
  [Server Scripts](../learn/framework/level-2/05-server-scripts-events.md)).
- `doc_events` in hooks.py pointing at an override file in your app.
- A whitelisted method + `frappe.call` for a button that does server work.

And the hard rule, always: **never edit another app's code.** Not one
line, not "just this once". The next `bench update` wipes it, and the
client finds out on a Monday. Extend from your app, or do not do it.
(See [Common mistakes](common-mistakes.md) §2.)

## Red flags — walk away

- **Abandoned.** Last commit over a year ago, issues unanswered. TailPOS
  (last activity Oct 2022) and ALYF Banking (repo flagged Archived) are
  the catalog's examples — staging test only, never promise them.
- **It forks core DocTypes.** An app that replaces or rewrites Sales
  Order / Stock Entry will break on the next ERPNext update. Check what
  it overrides before you install it.
- **No version branch for your Frappe version.** "Works on v15" on a v16
  site is a staging-test failure waiting to happen.
- **It needs Administrator to work.** An app that only functions as
  Administrator has a permission model of "everyone is admin". Do not
  put it on a client site.
- **Paid, with no trial.** A price with no way to test on staging is a
  sales call, not a product. Ask for a staging licence first.
- **No uninstall story.** If the README says nothing about removing it,
  assume the data is trapped.

## Worked example — one client, three needs

A spice manufacturer (the fmc demo client) asks for three things. Same
framework, three different answers:

**(a) CRM — install.** Real problem (leads live in WhatsApp), official
app (Frappe CRM, github.com/frappe/crm), version-16 branch, data
exportable, owner: the sales lead. **Decision: `bench get-app` Frappe
CRM.** Never start a client on the legacy ERPNext CRM — it is scheduled
for removal in v17.

**(b) Gate-pass register — build.** One form, one list, one approval.
No app in the catalog does just this, and a whole app for one register
is a dependency with no payoff. **Decision: build it in Studio in a day**
— form, list view, approval step — published to the Desktop. (This is
the [Studio example](../learn/erpnext/v16/13-studio-flow-insights.md).)

**(c) WhatsApp notifications — install.** Real problem (customers never
read email), maintained app, version branch exists. **Decision: install
the Frappe WhatsApp Suite** (Business Cloud API + in-Desk chat + chatbot)
— or the official WABA Integration if the client wants Frappe-maintained
code only. Order and invoice alerts go out on document events; the
chat UI replaces the shared phone the sales team passes around.

## Maintenance cost — every app is an upgrade dependency

An installed app is not free after install day. At every upgrade, each
app is one more branch to check, one more `migrate` that can fail, one
more staging test. Before the next upgrade, list every installed app
and ask the 5 questions again — an app that was right last year can be
abandoned this year. The full upgrade process is in the
[Upgrade guide](upgrade-v14-v15-v16.md).

## Before you `bench get-app` — checklist

- [ ] A real problem on a real project, named in writing
- [ ] Repo checked: recent release, issues answered, version branch for your Frappe version
- [ ] Uninstall + data export tested on staging first
- [ ] An owner named for when it breaks
- [ ] Installed on staging, tested with real user accounts (not Administrator)
- [ ] Upgrade impact noted: one more app on the upgrade checklist

## Sources

App facts from the [Apps Catalog](../research/apps-catalog.md) (66 apps,
11 categories, verified Nov 2026) and the [ERPNext lessons](../learn/erpnext/README.md).
Decision rules from real NexTash projects; upgrade cost from the
[Upgrade guide](upgrade-v14-v15-v16.md).
