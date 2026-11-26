# Upgrade Guide — v14 → v15 → v16

Upgrades are projects, not commands. Every rule below comes from an
upgrade that went wrong — usually because someone ran it straight on
production.

## The rules

1. **One major version at a time.** v14 → v15, verify, then v15 → v16.
   Never skip v15 — v16 patches assume v15 schema is already in place.
2. **Staging first, always.** The full upgrade runs on a copy of production data.
3. **A backup that was never restored is not a backup.** Test the restore on staging first.
4. **Every custom app needs a branch for the target version** — or it is removed first.

## 1. Readiness check

Establish what you are upgrading from — the source of truth, not memory:

```bash
grep __version__ apps/frappe/frappe/__init__.py apps/erpnext/erpnext/__init__.py
bench version
```

Then run the upgrade scan from
[frappe_core_skills](https://github.com/irfanzahoor/frappe_core_skills)
(`/frappe-upgrade-check`): it searches your apps for every removed or
changed API in the tables below and lists the files. Fix the hits
first — found on staging it is a delay, on production an outage.

Runtime floor for the target version (from the frappe-upgrade skill):
v15 needs Python 3.10–3.11 and Node 18/20; v16 needs Python **3.14+**
(older versions fail with SyntaxError) and Node **24+**. MariaDB 10.6+
on both; Ubuntu 24.04 recommended for v16.

Also list, on paper, before you start: every custom app, Server Script,
Workflow, print format and integration (payment gateway, WhatsApp,
email). Each one can break, and each needs an owner.

## 2. Backup — and prove it restores

```bash
bench --site <site> backup --with-files --compress
```

Then restore that backup onto the staging site and confirm the site
opens and a document can be created. Take a server snapshot too (VM
snapshot, or a Frappe Cloud backup), and keep the backup files until
at least a week after the upgrade — deleting them on upgrade day is
how a bad upgrade becomes a disaster.

```bash
bench --site staging restore <backup.sql> --with-public-files <public.tar> --with-private-files <private.tar>
```

## 3. Upgrade order

Framework first, then ERPNext, then the separate apps, then your
custom apps. The branches are switched together, in dependency order:

```bash
cd ~/frappe-bench
bench switch-to-branch version-15 frappe erpnext hrms  # v14 -> v15
bench --site <site> migrate
bench switch-to-branch version-16 frappe erpnext hrms  # v15 -> v16
bench --site <site> migrate
```

`bench migrate` runs the patches for every app in dependency order.
HRMS, Frappe CRM, Helpdesk and Payments are separate apps — each needs
its own version-15 / version-16 branch. A custom app with no branch
is removed before migrating, not after it fails.

On Frappe Cloud there are no bench commands — the version is switched
in the site dashboard — but the rules are the same. After the jump,
monthly patches come through `bench update` (v16.61.0 and friends are
monthly now — see [history](../research/history-2024-2026.md)).

## 4. Breaking changes — v14 → v15

The hits the upgrade scan finds most often:

| Old / removed | Use |
|---|---|
| `frappe.db.set()` | `doc.db_set()` |
| `frappe.db.update()` | `frappe.db.set_value()` |
| `frappe.db.set_value()` on Singles | `frappe.db.set_single_value()` |
| `frappe.db.set_temp` / `get_temp` | `frappe.cache` |
| JS `window.get_today` / `show_alert` / `user` / `roles` | `frappe.datetime.get_today`, `frappe.show_alert`, `frappe.session.user`, `frappe.user_roles` |
| `this` in Client Scripts | `frm` / `cur_frm` |

Also: **Server Scripts are disabled by default on v15+** — re-enable
with `bench set-config -g server_script_enabled 1`. Event Streaming
moved to its own app, and the frontend is Vue 3 — custom Vue 2
components need a rewrite; check on staging, not live.

## 5. Breaking changes — v15 → v16

| Change | Action |
|---|---|
| `has_permission` hooks | Must return an explicit `True` — returning `None` now denies access |
| DB commit inside document hooks | Not allowed — the framework commits |
| Default list sort | `creation` (was `modified`) — pass `order_by` explicitly where order matters |
| `frappe.get_doc(dt, name, field=val)` | No longer sets values |
| `frappe.sendmail(now=True)` | No longer commits |
| State-changing API methods | POST only (`logout`, `upload_file`, `send_login_link`) |
| PDF | Chrome renderer — **wkhtmltopdf is deprecated**, removed in v17 |
| Classic print formats | Deprecated — they stop working in v17, rebuild on the new print designer now |
| `/app` URL | `/desk` — fix bookmarks and hardcoded links |
| Blog, Newsletter, Energy Points, Offsite backups | Separate apps (offsite backups: `frappe/offsite_backups`) |

Two app moves to plan, not discover: **legacy ERPNext CRM is scheduled
for removal in v17** — move the client to the Frappe CRM app now,
during the v16 upgrade. And **standard workspace customisations reset
on upgrade** — keep them in your own app as fixtures, never Desk edits.

## 6. Patches — and a failed patch

Schema and data changes live in `patches/` with an entry in
`patches.txt` — one patch per change, idempotent where possible.
Patches that must never be skipped are listed in `hooks.py` as
`never_skip_patches = ["my_app.patches.v16_0.critical_data_fix"]`.

If a patch fails, migration stops. Read the traceback — it names the
patch and the row. Fix the **data** on staging (a bad value, a
duplicate, a missing master), not the patch. Never hand-edit the
database to fake a patch as done — the next migrate trusts that lie.
Re-run `bench --site <site> migrate`; it resumes from the failed
patch. `bench migrate --skip-failing` is for non-critical failures
only — a skipped patch is a debt entry, not a success.

A spice-factory client once had a patch fail on a duplicate batch number.
The fix was merging the duplicates on staging, then re-running migrate
— ten minutes. Skipping the patch would have left two batches with one
number in production stock.

## 7. Test the upgrade on the staging copy

Restore the production backup to staging, run the whole upgrade
there, then test — by hand, not by hope: Desk loads and `/desk`
works; for every DocType the upgrade touched, create, save, submit,
cancel, print, and one list-view filter; run the app tests with
`bench --site <test_site> run-tests --app <app>`; re-check every
whitelisted method, workflow and scheduled job; open the client's
real invoice on the Chrome renderer. Only when staging passes does
production get a date.

**Rollback plan:** if migrate fails halfway, **restore the pre-upgrade
backup onto the old code** (git checkout the old branches, restore DB
+ files). If you cannot do that in under an hour on staging, you are
not ready to upgrade production. Agree it with the client beforehand:
"if migrate fails and cannot be fixed in two hours, we restore."

## 8. Checklists

**Before the upgrade:**

- [ ] Current versions recorded; upgrade scan run, hits fixed
- [ ] Runtime meets the target version (Python, Node, MariaDB, OS)
- [ ] Backup taken with `--with-files --compress`, restore tested
- [ ] Every app has a branch for the target version (or is removed)
- [ ] Server Scripts, workflows, print formats, integrations listed, each with an owner
- [ ] Full upgrade rehearsed on a staging copy of production data
- [ ] Staging tests pass (create/save/submit/cancel/print, run-tests)
- [ ] Rollback plan agreed with the client, restore rehearsed

**After the upgrade:**

- [ ] Desk loads, `/desk` URL, workspaces correct
- [ ] Reports open (General Ledger, Stock Balance, Trial Balance)
- [ ] Print formats render on Chrome PDF — real invoice checked
- [ ] Scheduled jobs running (Scheduler, Background Jobs)
- [ ] Email Queue draining, email sending works
- [ ] Integrations tested end-to-end (payment gateway, WhatsApp, webhooks)
- [ ] Permissions: `has_permission` hooks return `True`, roles tested with real users, not Administrator
- [ ] Dashboards: upgraded sites keep classic dashboards until changed — switch to Insights only after checking each one
- [ ] Offsite backups app installed (v16 — no longer built in)
- [ ] Backup taken after the upgrade

## Sources

Deep reference: [frappe-upgrade skill](https://github.com/irfanzahoor/frappe_core_skills/tree/develop/skills/frappe-upgrade)
(breaking-change tables, runtime, checklist) and the v16 release notes
([history](../research/history-2024-2026.md)). Lessons: [05 — Server Scripts](../learn/framework/level-2/05-server-scripts-events.md), [09 — Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md), [13 — Testing](../learn/framework/level-3/13-testing.md).
