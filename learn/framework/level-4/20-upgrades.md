# 20 — Upgrades

## What it is

An upgrade moves a live site from one major version to the next —
v14 → v15 → v16. It is a project, not a command: the code changes,
the schema changes, and every custom app, Server Script, Workflow and
print format is a thing that can break. This lesson is the short
version — the rules, the order, and what to test. The full tables,
commands and checklists live in the deep reference:
[Upgrade guide — v14 → v15 → v16](../../../guides/upgrade-v14-v15-v16.md).

## The rules

1. **One major version at a time.** v14 → v15, verify, then v15 →
   v16. Never skip v15 — v16 patches assume the v15 schema is already
   in place.
2. **Staging first, always.** The full upgrade runs on a copy of
   production data.
3. **A backup that was never restored is not a backup.** Test the
   restore on staging first.
4. **Every custom app needs a branch for the target version** — or it
   is removed first.

## Minimal working example — the upgrade, end to end

```bash
# 1. Know what you are upgrading from
grep __version__ apps/frappe/frappe/__init__.py apps/erpnext/erpnext/__init__.py
bench version

# 2. Backup — and prove it restores on staging
bench --site <site> backup --with-files --compress
bench --site staging restore <backup.sql> \
  --with-public-files <public.tar> --with-private-files <private.tar>

# 3. Runtime floor for the target (v16: Python 3.14+, Node 24+, MariaDB 10.6+)
# 4. Switch branches together, in dependency order, then migrate
cd ~/frappe-bench
bench switch-to-branch version-16 frappe erpnext hrms
bench --site <site> migrate
```

On Frappe Cloud there are no bench commands — the version is switched
in the site dashboard — but the rules are the same.

## Breaking changes — the ones that bite most

| Change | Action |
|---|---|
| `has_permission` hooks | Must return an explicit `True` — `None` now denies access (v16) |
| DB commit inside document hooks | Not allowed — the framework commits |
| `frappe.sendmail(now=True)` | No longer commits (v16) |
| PDF | Chrome renderer — wkhtmltopdf deprecated, removed in v17 |
| `/app` URL | `/desk` — fix bookmarks and hardcoded links |
| Legacy ERPNext CRM | Scheduled for removal in v17 — move to Frappe CRM now |
| Server Scripts | Disabled by default on v15+ — re-enable with `bench set-config -g server_script_enabled 1` |

The full v14→v15 and v15→v16 tables, the upgrade scan
(`/frappe-upgrade-check` in frappe_core_skills), patch handling
(`never_skip_patches`, `bench migrate --skip-failing`), and the
complete checklists are in the
[upgrade guide](../../../guides/upgrade-v14-v15-v16.md).

## What to test after the upgrade

On staging, by hand, not by hope: Desk loads and `/desk` works; for
every DocType the upgrade touched — create, save, submit, cancel,
print, one list-view filter; run the app tests
(`bench --site <test_site> run-tests --app <app>`); re-check every
whitelisted method, Workflow and scheduled job; open the client's real
invoice on the Chrome renderer; check Email Queue draining and one
integration end to end. Only when staging passes does production get
a date — and the rollback plan is agreed beforehand: if migrate fails
and cannot be fixed in two hours, restore the pre-upgrade backup onto
the old code.

## When to use — and when not to

| Situation | Use |
|---|---|
| A version is out of support, or a feature needs the new one | Plan the upgrade — staging first |
| "Just run bench update on Friday" | Never on production without staging |
| A patch release (v16.60 → v16.61) | `bench update` on staging, quick smoke test, then live |
| A custom app with no branch for the target | Remove it first, or port it — do not migrate around it |
| The client asks "can we skip v15?" | No. One major at a time. |

## Common mistakes

- **Upgrading straight on production.** The staging copy exists so
  the failure happens there.
- **A backup never restored.** The restore test is the backup.
- **Skipping a failed patch.** A skipped patch is a debt entry, not a
  success — fix the data, re-run migrate.
- **Hand-editing the database to fake a patch as done.** The next
  migrate trusts that lie.
- **Forgetting the apps.** HRMS, Frappe CRM, Helpdesk and Payments
  are separate apps — each needs its own version branch.
- **No rollback plan.** If you cannot restore in under an hour on
  staging, you are not ready for production.

## Next

[21 — Ops](21-ops.md) — keeping a production site alive: backups,
monitoring, multi-site benches, and Frappe Cloud vs self-hosted.
