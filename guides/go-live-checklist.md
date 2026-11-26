# Go-Live Checklist

Go-live is a project, not a day. The system is ready when the data is
right, the users can do their jobs, and the old system can still save
you. A distributor went live with perfect code and wrong opening
stock — the first month's reports were fiction. This checklist exists
so that does not happen again.

## 1. Data import order

Import in dependency order — a transaction cannot reference a master
that does not exist yet:

```text
1. Company → Chart of Accounts → Cost Centers → Tax Templates
2. Masters: Item (+ Item Group, UOM, Warehouse), Customer, Supplier,
   Price List, BOM
3. Opening balances: stock + accounts (section 2)
4. Open transactions: open Sales Orders, Purchase Orders, open
   Sales/Purchase Invoices, open Payment Entries
```

Rules: **one file per DocType**, imported with Data Import (v16.50
has a step-based wizard — use it). Validate on a test import first;
never import straight into live. Reconcile every import: row counts
in the file vs rows in the system, ten records opened by hand. Bad
data is fixed in the file and re-imported — the file is the record.

## 2. Opening balances

**Stock** — Stock Reconciliation, posting date = the cutover date,
with a reason on every line. Bin quantities must match the physical
count. If the warehouse count and the sheet disagree, the count wins
and the difference is written down, not hidden.

**Accounts** — customer and supplier opening balances through the
Opening Invoice Creation Tool (one opening invoice per party, dated
the cutover date), bank and cash opening through Journal Entry.
Then the test that matters: **Trial Balance must balance**
(debits = credits) before go-live. If it does not balance, go-live
waits.

**Reconcile before the users arrive:** stock value in the books vs
the stock report, Accounts Receivable vs the customer ledger,
Accounts Payable vs the supplier ledger. Three numbers, three
matches, no exceptions.

## 3. Permissions & roles

- Roles and permissions set in Role Permission Manager — per DocType,
  per role, not per person. User Permissions (Company, Warehouse,
  Branch) for users who must see only their own branch or warehouse.
- **Test with real user accounts.** Log in as the accountant, the
  store keeper, the sales rep — and do their actual job: create a
  Sales Invoice, submit a Stock Entry, approve a Purchase Order.
  Testing as Administrator proves nothing; Administrator can do
  everything.
- Portal users (customers, suppliers) tested too — they log in
  through the portal and see only their own documents.
- On v16, `has_permission` hooks must return an explicit `True`
  (see [Lesson 09](../learn/framework/level-2/09-permissions-roles.md)).
  A hook returning `None` locks everyone out.
- Hiding a field in JS is not security — use permlevel. Validation
  on the server, not only in JS (see
  [Common mistakes](common-mistakes.md)).

## 4. User training

- **NexTash trains the client's super users; super users train
  their teams.** Training the whole staff directly does not scale
  and does not stick.
- Material per role, one page per job: "How to make a Sales
  Invoice", "How to receive stock", "How to approve a leave
  application". Short SOPs, not a manual nobody reads.
- Training happens on a **training site with sample data**, never on
  live. Users break things in training and learn; users break
  things in live and the business stops.
- Every role does its real work once in training — the first real
  invoice should not be the first invoice ever made.

## 5. Cutover plan

- **Freeze date agreed in writing.** No new transactions in the old
  system after Friday close. Anything after the freeze goes into
  ERPNext.
- **Final import on Saturday:** masters delta (customers or items
  added during the week), opening balances, open transactions.
- **Delta entries:** anything that slipped through after the final
  import is entered by hand on Monday morning and ticked off a list.
- **Communication:** every user knows the freeze date, the go-live
  date, and who to call when stuck. The client's manager announces it.

## 6. Backups & restore test

```bash
bench --site <site> backup --with-files
```

- Scheduled backups on before go-live (on v16, offsite backups are
  a separate app — install it, do not assume it is built in).
- **Restore tested on a spare site before go-live.** A backup that
  was never restored is not a backup.
- Backup files kept off the server — a backup on the same disk as
  the database is a copy, not a backup.

## 7. Monitoring

Week 1, someone checks daily: **Scheduler running** — `bench
doctor` and the Background Jobs list in Desk. A stopped scheduler
means no emails, no notifications, no auto-reposts — silently.
**Email Queue draining** — emails sent, not stuck. **Error Log
clean** — every error read, not just counted; one error repeated
200 times is one bug, fix it. **Disk space** — a full disk stops the
database. **Integrations end-to-end** — payment gateway, WhatsApp,
webhooks: one real transaction each, on go-live day.

## 8. Rollback / Plan B

- **The old system stays runnable for one week.** Excel, the old
  ERP, the paper register — whatever it was, it is not deleted on
  go-live day.
- **The rollback trigger is agreed in advance:** e.g. "if invoicing
  is down for two hours, we revert to the old system and re-plan."
  Decided calmly now, not in a panic on Monday.
- Data entered in ERPNext before a rollback must be exportable —
  know how to get it out (report export) before you need it.

## 9. Go-live day runbook

| Time | Action | Owner |
|---|---|---|
| 08:00 | Scheduler, Email Queue, Error Log, disk checked; backup taken | NexTash |
| 08:30 | Users log in; each role opens its own workspace | Super users |
| 09:00 | First real Sales Invoice made together with the sales team | Sales super user |
| 10:00 | First stock movement checked against Bin | Store keeper |
| 12:00 | First Payment Entry, bank balance checked | Accountant |
| 14:00 | Error Log reviewed; any error fixed or logged with an owner | NexTash |
| 16:00 | Day-1 sign-off call: what worked, what is blocked, tomorrow's list | Client manager + NexTash |
| 17:00 | Backup taken; day-1 notes written down | NexTash |

## Go-live checklist

**Data**
- [ ] Masters imported in order, row counts reconciled
- [ ] Opening stock reconciled to physical count
- [ ] Opening balances imported; Trial Balance balances
- [ ] AR / AP / stock value reconciled to the ledgers
- [ ] Open transactions imported (orders, open invoices)

**Permissions**
- [ ] Roles set per DocType; User Permissions per branch/warehouse
- [ ] Tested with real user accounts, not Administrator
- [ ] Portal users tested

**Training**
- [ ] Super users trained; SOPs per role written
- [ ] Every role did its real work once on the training site

**Cutover**
- [ ] Freeze date agreed in writing; final import done
- [ ] Delta list ready for Monday morning

**Backups & monitoring**
- [ ] Scheduled backups on; restore tested on a spare site
- [ ] Scheduler, Email Queue, Error Log checked; integrations tested end-to-end

**Rollback**
- [ ] Old system runnable for one week
- [ ] Rollback trigger agreed with the client

## Sources

Lesson cross-references: [01 — Accounting](../learn/erpnext/core/01-accounting.md)
(opening balances, Trial Balance),
[02 — Stock & Inventory](../learn/erpnext/core/02-stock-inventory.md)
(Stock Reconciliation, Bin),
[09 — Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md),
[11 — Scheduler & Background Jobs](../learn/framework/level-3/11-scheduler-jobs.md),
[12 — Notifications & Email](../learn/framework/level-3/12-notifications-email.md),
and [Common mistakes](common-mistakes.md) (permissions, ledger rules).
