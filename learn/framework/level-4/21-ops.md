# 21 — Ops

## What it is

Ops is keeping a production site alive: backed up, monitored, and
recoverable. Nobody notices good ops — until the day the disk fills,
the scheduler stops, or a site will not come back. This lesson is the
weekly routine and the decisions (multi-site, Cloud vs self-hosted)
that make the bad day survivable.

## Minimal working example — the weekly ops routine

Run these every week, on every production site. Thirty minutes, same
order:

```bash
# 1. Backup — database + files, compressed
bench --site mysite.local backup --with-files --compress

# 2. Prove the backup restores (on a spare site, monthly at least)
bench --site spare.local restore <backup.sql> \
  --with-public-files <public.tar> --with-private-files <private.tar>

# 3. Are the workers and scheduler alive?
bench doctor

# 4. Disk space — a full disk stops the database
df -h
```

Then in Desk: **Error Log** — read every new error, don't just count
them (one error repeated 200 times is one bug, fix it); **Email
Queue** — draining, not stuck; **Background Jobs** — the scheduler
ran last night's jobs. On v16, offsite backups are a separate app
(`frappe/offsite_backups`) — install it, do not assume backups leave
the server by themselves. Keep backup files off the server: a backup
on the same disk as the database is a copy, not a backup.

## Multi-site benches

One bench can host many sites — they share the apps, each has its own
database and files:

```bash
bench new-site client2.local
bench --site client2.local install-app erpnext
bench --site client2.local install-app my_app
```

Use it for: one bench per client group, a staging site next to
production, a training site with sample data. Never share a database
between sites, and never test on the production site — a test site
costs nothing, a test on production costs a business day.

## Frappe Cloud vs self-hosted

| | Frappe Cloud | Self-hosted |
|---|---|---|
| Who runs the server | Frappe — updates, backups, monitoring included | You — OS, bench, backups, monitoring |
| Bench commands | No shell — version and settings in the site dashboard | Full shell: `bench`, `console`, custom scripts |
| Control | Limited (no custom bench commands, no server access) | Full — any app, any integration, any schedule |
| Scaling | Pick a plan, Frappe scales it | You size and scale the server |
| Cost shape | Per site, per month | Server + your time |

Pick Cloud when the client wants ERP without an IT person, and the
standard apps are enough. Pick self-hosted when you need shell access,
custom bench work, private integrations, or data that must stay on the
client's own server. Either way, the ops routine above still applies
— Cloud automates the backup, it does not remove the need to check
that the backup exists and restores.

## When to use — and when not to

| Situation | Use |
|---|---|
| A site is live | The weekly routine, every week, no exceptions |
| A second client on the same bench | A second site, not a second bench |
| A test or training environment | A separate site on the same bench |
| "The backup exists" | The restore test — a backup never restored is not a backup |
| An error in the log | Read it and fix the cause — do not clear the log |
| A client with no IT staff | Frappe Cloud, with you checking the routine |

## Common mistakes

- **No restore test.** The backup file exists, the restore fails.
  Found out on the worst day.
- **Backups on the same disk.** The disk dies, the backup dies with
  it.
- **Scheduler silently stopped.** No emails, no notifications, no
  auto-reposts — and nobody notices for a week. `bench doctor` is
  the check.
- **Testing on production.** A test import on the live site is a
  live import. Use the test site.
- **Ignoring the Error Log.** Errors compound. One unread error is
  a bug report nobody filed.
- **One bench, one site, forever.** A second site on the same bench
  is free — staging, training, and the next client all live there.

## Next

You have finished the Framework path — all 21 topics, from your first
bench to a production site you can keep alive.

- **Review the map:** [Learn: Frappe Framework — Noob to Pro](../README.md)
- **Use it on real modules:** [Learn: ERPNext Modules](../../erpnext/README.md) — all 14 modules, from Accounting to cross-module flows
- **Do real work with it:** [Guides](../../../guides/README.md) — upgrade, go-live, and the common mistakes to avoid
- **Stay current:** [Research: what changed 2024–2026](../../../research/history-2024-2026.md) and the [apps catalog](../../../research/apps-catalog.md) — the hub grows with the ecosystem

The path is finished. The learning is not — the next production site
is where these lessons earn their keep.
