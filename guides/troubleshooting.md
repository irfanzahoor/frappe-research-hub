# Troubleshooting — The Error Library

The page you open when something breaks. Every entry is a real error
a beginner or intermediate developer actually hits, with the exact
message, why it happens, and the fix — in order. No theory, just the
steps.

## Before you fix anything — the first 3 checks

Most errors are solved by one of these, before you touch any code:

1. **Read the LAST lines of the error, not the first.** A traceback
   is a stack: the first lines are where the code was called from,
   the last line is the exception itself — `OperationalError`,
   `LinkValidationError`, `ModuleNotFoundError`. That last line is
   the name of your problem. Search for it, not for the whole trace.
2. **Check the Error Log in Desk.** Search "Error Log" in the
   awesome bar — every server error is saved there with its full
   traceback, even the ones the screen only shows as "Something went
   wrong". If the same error repeats, read the newest entry.
3. **Run `bench doctor`.** One command, from the bench directory,
   that shows the scheduler, background workers, Redis and Socket.IO
   status. If any of them is down, half the errors in this guide
   follow from that one fact.

If you are mid-upgrade, back up first: `bench --site <site> backup`
— a fix you can undo is a fix you can try.

---

## Stage A — Setup & Install

### A1 — Wrong Python / Node / MariaDB version for v16

```text
ERROR: This version of Frappe requires Python 3.14 or newer
```

or the install just fails halfway with a version complaint.

**When it happens:** `bench init` on a fresh server, or an upgrade to
v16 on an old bench.

**Why it happens:** v16 raised its floor: **Python 3.14, Node 24,
MariaDB 11.8, Redis/Valkey 6+, Yarn 1.22+**. The old bench was built
on Python 3.10 / Node 18, and v16 code will not even import on it.

**Fix:**

1. Check what you actually have:
   ```bash
   python3 --version && node -v && mariadb --version
   ```
2. Install the right Python and create the bench with it:
   ```bash
   bench init --frappe-branch version-16 --python python3.14 frappe-bench
   ```
3. If the bench already exists on the wrong Python, do not try to
   patch it in place — rebuild the virtualenv on Python 3.14 (see
   the [Upgrade guide](upgrade-v14-v15-v16.md)).

**Prevention:** before any install or upgrade, read the version
matrix in the [Upgrade guide](upgrade-v14-v15-v16.md) and match all
five versions — Python, Node, MariaDB, Redis, Yarn — not just one.

### A2 — MariaDB access denied for root

```text
pymysql.err.OperationalError: (1045, "Access denied for user 'root'@'localhost' (using password: YES)")
```

**When it happens:** `bench new-site` or `bench migrate` on a fresh
install.

**Why it happens:** bench logs into MariaDB with the password stored
in the site's config, and it does not match the password MariaDB
actually has for `root`. Usually the MariaDB root password was set
during install and never given to bench — or it was changed later.

**Fix:**

1. Check what bench thinks the password is:
   ```bash
   cat sites/<site>/site_config.json | grep db_password
   ```
2. Log into MariaDB as root and set the password to match:
   ```bash
   sudo mysql -u root
   ```
   ```sql
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'the-password-from-site_config.json';
   FLUSH PRIVILEGES;
   ```
3. Test it:
   ```bash
   bench --site <site> migrate
   ```

**Prevention:** write the MariaDB root password down at install time
and use the same one for every site on that server. One password per
server, not one per site.

### A3 — MariaDB is not running

```text
pymysql.err.OperationalError: (2002, "Can't connect to local MySQL server through socket '/run/mysqld/mysqld.sock'")
```

**When it happens:** any bench command after a server reboot, or on a
fresh install where MariaDB was never started.

**Why it happens:** MariaDB is a separate service. If it is stopped,
nothing in Frappe can reach the database — the error is about the
socket file, not about your site.

**Fix:**

```bash
sudo systemctl status mariadb
sudo systemctl start mariadb
sudo systemctl enable mariadb   # start it on every boot, not just now
bench --site <site> migrate     # confirm the site connects again
```

**Prevention:** `enable` the service at install time (step 3 above),
not just `start` it. After every reboot, `bench doctor` is the
one-command check.

### A4 — Redis connection refused

```text
redis.exceptions.ConnectionError: Error 111 connecting to 127.0.0.1:13000. Connection refused.
```

**When it happens:** `bench start`, or the site loads but background
jobs and caching silently do nothing.

**Why it happens:** Frappe talks to Redis for the queue, the cache
and Socket.IO. If Redis is stopped, the web process starts but
nothing that needs the queue works — and the error names a port
(11000, 12000 or 13000 on a dev bench, 6379 in production).

**Fix:**

```bash
redis-cli ping        # should answer PONG
sudo systemctl status redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
bench doctor          # confirms Redis is back for all three queues
```

**Prevention:** same as MariaDB — enable the service at install time.
On v16, Valkey is an accepted replacement for Redis; either way, one
of them must be running before `bench start`.

### A5 — `bench build` fails on assets / Yarn

```text
error Command failed.
Exit code: 1
Command: /usr/bin/node .../yarn install
```

**When it happens:** after `bench update`, after installing an app,
or on a fresh bench.

**Why it happens:** the JavaScript build needs the right Node version
(v16 needs Node 24) and a working Yarn install. The two usual causes
are the wrong Node version (see A1) and a half-installed or corrupted
`node_modules`.

**Fix:**

1. Check Node first: `node -v` — v16 needs v24.
2. Reinstall the bench's dependencies, then rebuild:
   ```bash
   bench setup requirements
   bench build
   ```
3. If one app is the problem, build only it:
   ```bash
   bench build --app <app>
   ```
   and read the lines just above the failure — they name the file
   that broke the build.

**Prevention:** never install a second Node version over the first
with `apt` and forget which one is on the PATH. Use one Node manager
for the whole server and pin the version in your install notes.

### A6 — `ModuleNotFoundError: No module named 'frappe'`

```text
ModuleNotFoundError: No module named 'frappe'
```

**When it happens:** any `bench` command, or a Python script that
imports frappe.

**Why it happens:** you are running the command from the wrong
directory, or from a shell where the bench's virtualenv is not on the
path. `frappe` only exists inside the bench's `env/`.

**Fix:**

1. Go to the bench directory and try again:
   ```bash
   cd ~/frappe-bench
   bench --version
   ```
2. If it still fails, the virtualenv is broken — reinstall the
   bench's requirements:
   ```bash
   bench setup requirements
   ```

**Prevention:** always `cd` into the bench directory before running
bench commands. Put the bench path in your shell notes, not in your
memory.

### A7 — Port 8000 already in use

```text
OSError: [Errno 98] Address already in use
```

**When it happens:** `bench start` when another bench (or an old,
still-running one) already holds port 8000.

**Why it happens:** only one process can listen on a port. The usual
cause is a `bench start` that was never stopped — its terminal was
closed but the processes kept running.

**Fix:**

1. Find what holds the port:
   ```bash
   sudo lsof -i :8000
   ```
2. Stop the old bench properly (`bench stop` from its directory), or
   kill the process by its PID:
   ```bash
   kill <pid>
   ```
3. Or give this bench a different port — add to
   `sites/common_site_config.json`:
   ```json
   "webserver_port": 8001
   ```
   then restart the bench.

**Prevention:** one bench per port, written down. Stop a dev bench
with Ctrl+C in its own terminal, not by closing the terminal window.

---

## Stage B — Development

### B1 — `bench migrate` fails on a patch

```text
frappe.modules.patch_handler.PatchError: Patch myapp.patches.v16_0.fix_data execute failed
```

or:

```text
ModuleNotFoundError: No module named 'frappe.patches.v15_0.some_patch'
Migration exit code: 1
```

**When it happens:** `bench migrate` after an update or after pulling
new app code.

**Why it happens:** a patch is a one-off script listed in the app's
`patches.txt`. It fails because its file is missing (incomplete
update), its code has a bug, or it expects data that is not there.
The migrate stops at the first failing patch — everything after it
has not run yet.

**Fix:**

1. Read the failing patch name from the error — it is the first thing
   to fix, not the whole migrate.
2. Check the apps are on matching branches:
   ```bash
   bench version --format table
   git -C apps/frappe status --short
   git -C apps/frappe branch --show-current
   ```
   A patch file missing from disk means the update did not finish —
   restore the correct app code from the matching release, then
   re-run `bench --site <site> migrate`.
3. If the patch itself is broken, fix its code, then re-run it by
   appending a date comment to its line in `patches.txt`:
   ```text
   myapp.patches.v16_0.fix_data #2026-11-26
   ```
   then `bench --site <site> migrate` again.
4. Last resort only: `bench --site <site> migrate --skip-failing`
   skips the patch and marks it done. Use it only when you know the
   patch is safe to skip — a skipped data patch leaves the data it
   was supposed to move in the old shape, and the site looks fine
   until it does not.

**Prevention:** back up before every migrate
(`bench --site <site> backup`), and run migrations on staging first.
Never run `migrate` on production the first time you run it anywhere.

### B2 — `Unknown column` after a code change

```text
pymysql.err.OperationalError: (1054, "Unknown column 'tabSales Order.new_field' in 'field list'")
```

**When it happens:** after adding a field to a DocType, or after
switching an app's branch.

**Why it happens:** the code knows about the field but the database
does not — the schema sync in `migrate` has not run, or ran against
different code than is installed now.

**Fix:**

```bash
bench --site <site> migrate
bench --site <site> clear-cache
```

If it still fails, the code and the branch disagree — check
`git -C apps/<app> status` for uncommitted or half-pulled changes,
fix the branch, and migrate again.

**Prevention:** every DocType change ends with `migrate`, every time,
before you test. See [Lesson 03](../learn/framework/level-1/03-first-doctype.md).

### B3 — "Not Permitted" when opening a DocType

```text
Not Permitted
You do not have enough permissions to access this document.
```

**When it happens:** a user opens a DocType or a document that
Administrator opens fine.

**Why it happens:** the user's role has no permission on that
DocType, or a User Permission restricts them to specific documents
(for example, only their own company's records).

**Fix:**

1. Open **Role Permission Manager**, pick the DocType, and check the
   row for the user's role — read, write, create, submit, delete
   are separate ticks. Tick what the job needs, nothing more.
2. Check **User Permissions** for that user — a restriction to one
   Company or Warehouse hides everything else.
3. Test as the real user, not as Administrator — Administrator sees
   everything, so testing as Administrator tests nothing.

**Prevention:** test every new role with a real user account before
go-live. See [Lesson 09](../learn/framework/level-2/09-permissions-roles.md)
and the [Go-Live Checklist](go-live-checklist.md).

### B4 — "Data too long for column"

```text
pymysql.err.DataError: (1406, "Data too long for column 'remarks' at row 1")
```

**When it happens:** saving a document with a long value in a Data
field.

**Why it happens:** a **Data** field holds at most 140 characters.
The form lets you type more, and the database refuses it on save.

**Fix:** change the field's type to **Small Text** (up to 65,535
characters) in Customize Form, then `bench --site <site> migrate`.

**Prevention:** use Data only for short values — names, codes, phone
numbers. Anything a user might write a sentence in is Small Text
from the start.

### B5 — Link validation fails / "Could not find"

```text
frappe.exceptions.LinkValidationError: Could not find Customer: Karachi Spice Traders
```

**When it happens:** saving a document whose Link field points at a
document that does not exist.

**Why it happens:** the linked document was deleted or renamed, or
the value was typed by hand with a typo. Frappe refuses to save a
dangling link — that is the validation working, not a bug.

**Fix:**

1. Check the linked document exists: search for it in Desk.
2. If it was renamed, update the Link field to the new name.
3. If it was deleted, recreate it — or clear the field if the link
   is optional.
4. In code, check before you link:
   ```python
   if not frappe.db.exists("Customer", customer_name):
       frappe.throw(_("Customer {0} does not exist").format(customer_name))
   ```

**Prevention:** never delete a master (Customer, Item, Warehouse)
that transactions point to. Cancel or disable it instead, and let
the links keep resolving.

### B6 — Mandatory field error on save

```text
frappe.exceptions.MandatoryError: [Sales Order, SO-0001]: posting_date
```

**When it happens:** saving a document that looks complete — every
visible field is filled.

**Why it happens:** a field is marked mandatory but hidden by a
**Depends On** condition, or sitting in a collapsed section. The user
cannot see it, so they cannot fill it, and the save refuses.

**Fix:** open **Customize Form** for the DocType, find the mandatory
field, and either remove the **Mandatory** tick or remove the
**Depends On** that hides it. A field cannot be both mandatory and
invisible.

**Prevention:** when you add a Depends On to a field, check its
Mandatory tick in the same edit. See the
[Common Mistakes](common-mistakes.md) guide.

### B7 — Server Script / Client Script does not run

No error at all — the script just does nothing.

**When it happens:** after writing a script that should fire on
save, submit, or form load.

**Why it happens:** almost always one of four things — the script is
in the wrong place, the event name is wrong, the DocType was not
reloaded after the change, or the script itself has an error that
only shows in the log.

**Fix:**

1. Check the location. Client behaviour lives in the DocType's
   `.js` file in the app (`<app>/<app>/doctype/<doctype>/<doctype>.js`);
   server behaviour lives in a `doc_events` hook in `hooks.py` or a
   Server Script document — not the other way round.
2. Check the event name: `validate` runs on every save, `on_submit`
   only on submit, `refresh` every time the form opens. A
   submit-only rule in `validate` blocks drafts too.
3. Reload the DocType: `bench --site <site> migrate`, then
   `bench --site <site> clear-cache` — and for Client Scripts,
   `bench build` and a hard refresh (Ctrl+Shift+R).
4. Look for the error: browser console (F12) for Client Scripts,
   **Error Log** in Desk for Server Scripts.

**Prevention:** one script, one event, one file — and test it the
minute you write it, not at the end of the day. See
[Lesson 05](../learn/framework/level-2/05-server-scripts-events.md)
and [Lesson 06](../learn/framework/level-2/06-client-scripts.md).

### B8 — Print format shows old output, or a blank PDF

**When it happens:** after editing a Print Format, the printed
document still shows the old layout — or prints blank.

**Why it happens:** print output is cached, and a Jinja error in the
format fails silently on the page while the real error goes to the
log.

**Fix:**

1. Clear the cache and rebuild:
   ```bash
   bench --site <site> clear-cache
   bench build
   ```
2. Check the Print Format is set as **Default** for the DocType, and
   that the document is actually using it (Print → Format dropdown).
3. Check **Error Log** for a Jinja error — a bad `{{ }}` in the
   format is the usual cause of a blank print.

**Prevention:** test a print format on one real document before
telling users about it. See
[Lesson 08](../learn/framework/level-2/08-reports-print-formats.md).

---

## Stage C — Production & Go-Live

### C1 — "Something went wrong" / Internal Server Error

```text
Internal Server Error
Something went wrong. Please try again or contact support.
```

**When it happens:** any page, any time — usually right after a
deploy or an update.

**Why it happens:** this message is a cover for a real server error.
The cause is in the logs, never on the screen.

**Fix:**

1. Open **Error Log** in Desk — the newest entry has the full
   traceback. Read its last line first (see the checks at the top).
2. If Desk itself is down, read the logs on the server:
   ```bash
   tail -50 logs/web.error.log
   tail -50 logs/frappe.log
   ```
3. Check the disk is not full — a full disk causes random 500s on
   otherwise healthy sites:
   ```bash
   df -h
   ```

**Prevention:** never deploy on Friday evening without a backup and
a rollback plan. See the [Go-Live Checklist](go-live-checklist.md).

### C2 — Scheduler is not running

No error message — scheduled jobs, email, and reminders just never
happen.

**When it happens:** after a fresh production setup, after a restore,
or after someone turned the scheduler off and forgot.

**Why it happens:** the scheduler is a per-site switch. If it is off,
no scheduled job runs at all — not just email. In production it also
needs the supervisor workers running.

**Fix:**

```bash
bench --site <site> scheduler status
bench --site <site> enable-scheduler
bench doctor          # shows scheduler + workers in one place
```

In production, also check the workers:

```bash
sudo supervisorctl status
bench setup supervisor   # regenerates the supervisor config if it is missing
```

And check `sites/<site>/site_config.json` does not have
`"pause_scheduler": 1` left over from a migration or a staging copy.

**Prevention:** `bench doctor` after every deploy and every reboot.
A scheduler that has been off for a week is a week of unsent mail
and unrun jobs. See
[Lesson 11](../learn/framework/level-3/11-scheduler-jobs.md).

### C3 — Emails stuck in the Email Queue

**When it happens:** mails sit in **Email Queue** with status
**Not Sent** or **Sending** for hours — or arrive 2–5 minutes late.

**Why it happens:** Frappe does not send mail the moment you create
it. A background job (`frappe.email.queue.flush`) picks entries up
every 4 minutes, so a delay of a few minutes is normal. Hours means
one of three things is wrong: sending is suspended, mail is muted,
or the scheduler is not running (see C2).

**Fix:**

1. Open **Email Queue** in Desk. If the top-right button reads
   **Resume Sending**, sending is switched off for the whole site —
   click it.
2. Check `sites/<site>/site_config.json` for `"mute_emails": 1` —
   usually left on from testing or a staging copy. Remove it and
   restart the bench.
3. Check the scheduler is running (C2 above).
4. Flush the queue by hand to confirm it works:
   ```bash
   bench --site <site> execute frappe.email.queue.flush
   ```
5. A failed entry can be retried from its own form — open it and use
   **Send Now**. If it fails again, read its **Error** field: it
   names the real problem (wrong password, blocked port 25, bad
   SMTP host).

**Prevention:** after every staging restore, check `mute_emails`
before anyone wonders why no mail arrived. See
[Lesson 12](../learn/framework/level-3/12-notifications-email.md).

### C4 — `bench update` fails: local changes would be overwritten

```text
error: Your local changes to the following files would be overwritten by merge
```

**When it happens:** `bench update` after someone edited files
inside `apps/frappe` or `apps/erpnext` directly on the server.

**Why it happens:** `bench update` pulls new code with git, and git
refuses to overwrite files you changed. The changes are usually an
accidental edit — or a fix someone made on the server and never
committed anywhere.

**Fix:**

1. See what changed:
   ```bash
   git -C apps/frappe status --short
   git -C apps/erpnext status --short
   ```
2. If the changes are accidental, stash them and update:
   ```bash
   git -C apps/frappe stash
   bench update
   ```
3. If they are a real fix, commit them to your own app or branch
   first — never leave a fix uncommitted inside `apps/frappe`.
4. `bench update --reset` discards local changes and updates anyway.
   Use it only when you are sure the changes are disposable — it
   cannot be undone.

**Prevention:** never edit framework or ERPNext code on the server.
Custom code lives in your own app; the server's `apps/frappe` and
`apps/erpnext` stay clean.

### C5 — Restored backup, broken site / version mismatch

```text
pymysql.err.OperationalError: (1054, "Unknown column ...")
```

or the site loads but documents behave wrongly, right after a
restore.

**When it happens:** after `bench --site <site> restore <backup>`,
especially when the backup came from a different server or version.

**Why it happens:** a backup is data, not code. Restoring it puts
old data under new code (or the reverse), and the schema does not
match until a migrate runs. If the apps are on a different major
version than the backup, no migrate can fix that.

**Fix:**

1. Always migrate after a restore:
   ```bash
   bench --site <site> restore /path/to/backup.sql.gz
   bench --site <site> migrate
   ```
2. Check the versions match the backup's versions:
   ```bash
   bench version --format table
   ```
   If the backup is v15 and the bench is v16, install the matching
   branches first (`bench get-app erpnext --branch version-15`),
   then restore, then migrate.
3. If the restore itself fails, check the file is a bench backup
   (`.sql.gz` from `bench backup`) and that there is free disk space
   for the restore.

**Prevention:** label every backup with its version and date, and
test a restore on staging before you ever need one for real. See
[Lesson 21](../learn/framework/level-4/21-ops.md).

### C6 — 504 Gateway Timeout on big reports

```text
504 Gateway Time-out
```

**When it happens:** running a large report, a bulk import, or any
long operation from the browser.

**Why it happens:** the web request has a time limit. A report that
scans a year of Stock Ledger entries, or an import of ten thousand
rows, takes longer than the limit — the server is still working, but
the browser has already given up.

**Fix:**

1. Do not run heavy work in a web request. Move it to a background
   job with `frappe.enqueue` — the user gets an answer when it is
   done, not a timeout. See
   [Lesson 11](../learn/framework/level-3/11-scheduler-jobs.md).
2. For reports, filter first: a date range and a warehouse cut the
   rows before the query runs, not after.
3. Check the log to confirm it was a timeout and not an error:
   ```bash
   tail -50 logs/web.log
   ```

**Prevention:** any operation that can grow with the data — reports,
imports, reconciliations — belongs in a background job from the day
it is written, not after the first timeout. See
[Lesson 14](../learn/framework/level-3/14-performance.md).

### C7 — Desk is blank / assets 404 after an update

**When it happens:** after `bench update`, the login page loads but
Desk is blank, or the browser console shows 404s for `.js` and
`.css` files.

**Why it happens:** the built assets on disk are from the old code,
or the browser is holding the old ones. The site is fine; the files
it serves are stale.

**Fix:**

```bash
bench build
bench --site <site> clear-cache
```

Then hard-refresh the browser (Ctrl+Shift+R). If `bench build`
itself fails, see A5 — it is usually the Node version.

**Prevention:** every update ends with `bench build` + `clear-cache`
before you tell users the site is back. Put it in the deploy
checklist, not in your memory.

---

## Still stuck?

1. Work the problem like [Lesson 16 — Debugging](../learn/framework/level-3/16-debugging.md):
   reproduce it in the console, isolate the smallest case, read the
   last line of the traceback.
2. Search the [Frappe Forum](https://discuss.frappe.io) for the exact
   error text — if you hit it, someone hit it before you.
3. If you post, include four things or nobody can help you: the
   Frappe/ERPNext version (`bench version`), the full traceback
   (last 20 lines), what you were doing when it happened, and what
   you already tried from this guide.
4. If it looks like a framework bug, open an issue on
   [frappe/frappe](https://github.com/frappe/frappe) with the same
   four things — and a minimal reproduction, not your whole site.

## How we can use it

This is the page NexTash support opens first on a client call: the
client reads out the error, we find it here, and the fix starts in
minutes instead of after an hour of guessing. New team members learn
the same way — every error they hit the first time is already written
down with the fix that worked last time. When an error is missing
from this page, that is the signal to add it: a library that grows
with every incident is worth more than one that was complete on day
one.

## Sources

Error messages and fixes verified against Frappe docs
(Email Queue, password-reset mail), Frappe Cloud docs (migrate
out-of-memory, failed updates), the Frappe Forum, and the
`bench migrate --skip-failing` / `never_skip_patches` behaviour in
Frappe's patch handler. Version requirements (v16: Python 3.14,
Node 24, MariaDB 11.8) from the Frappe `pyproject.toml` dependency
ranges. Lesson links point at this hub's own lessons.
