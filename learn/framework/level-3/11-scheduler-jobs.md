# 11 — Scheduler, Background Jobs & Queues

## What it is

Two different things that beginners mix up:

- **The scheduler** runs code on a clock — every hour, every day, at
  2 AM. You register the work in `scheduler_events` in `hooks.py`. The
  scheduler does not run your code; it only **enqueues** it. A worker
  process picks it up from a Redis queue and runs it.
- **A background job** runs code *now, but not in the request*. You start
  it with `frappe.enqueue()` — for example, when a user clicks "Generate
  report" and the report takes two minutes. The user gets an answer
  immediately; the work finishes in the background.

If either part is down — scheduler, workers, or Redis — nothing runs, and
the user sees nothing. That is why "the job never ran" is a debugging
question (Lesson 16), not a code question.

## Minimal working example — spice batch expiry check

Every morning, find spice batches expiring within 30 days and email the
QA Manager. Scheduled work takes **no arguments** — the scheduler passes
none.

```python
# my_app/tasks.py
import frappe
from frappe.utils import add_days, today


def notify_expiring_batches():
    """Runs daily. No arguments — the scheduler passes none."""
    expiring = frappe.get_all("Batch",
        filters={
            "expiry_date": ("between", [today(), add_days(today(), 30)]),
            "disabled": 0,
        },
        fields=["name", "item", "expiry_date"])
    if not expiring:
        return
    rows = "\n".join(
        f"- {b['item']} ({b['name']}) expires {b['expiry_date']}"
        for b in expiring
    )
    frappe.sendmail(
        recipients=["qa.manager@nextash.example"],
        subject=f"{len(expiring)} spice batches expiring soon",
        message=f"The following batches expire within 30 days:\n\n{rows}",
    )
```

```python
# hooks.py — registry only, no logic here
scheduler_events = {
    "daily": ["my_app.tasks.notify_expiring_batches"],
    "hourly_long": ["my_app.tasks.sync_supplier_stock"],
    "cron": {"0 2 * * *": ["my_app.tasks.nightly_archive"]},
}
```

Run `bench --site <site> migrate` after any change to `hooks.py`, or the
scheduler never sees the new event.

| Event key | When | Queue |
|---|---|---|
| `all` | Every tick (v15+: 60s) | default — never more than 60s of work |
| `hourly` / `daily` / `weekly` / `monthly` | On the hour / day / week / month | default (5 min timeout) |
| `hourly_long` / `daily_long` / `weekly_long` / `monthly_long` | Same times | long (25 min timeout) |
| `cron` | Any cron expression, e.g. `0 2 * * *` | default unless you enqueue to long yourself |

## Minimal working example — a long job from a button

A user submits a Sales Order and wants a stock-availability check across
3 warehouses. That takes minutes — it must not run inside the request:

```python
# my_app/selling/api.py
import frappe
from frappe.utils.background_jobs import is_job_enqueued


@frappe.whitelist()
def check_stock_availability(sales_order):
    job_id = f"stock-check-{sales_order}"
    if is_job_enqueued(job_id):
        return _("Stock check already running for {0}").format(sales_order)
    frappe.enqueue(
        "my_app.selling.jobs.check_stock_availability",
        queue="long",
        timeout=1500,
        job_id=job_id,
        enqueue_after_commit=True,   # run only if the save commits
        sales_order=sales_order,      # simple values only — never a doc
    )
    return _("Stock check started — you will be notified when it finishes")
```

```python
# my_app/selling/jobs.py
import frappe


def check_stock_availability(sales_order):
    """Runs in a worker. Handle its own errors — log, then re-raise."""
    order = frappe.get_doc("Sales Order", sales_order)
    # ... heavy warehouse checks, commit in batches ...
    # on failure: frappe.log_error(title=..., message=frappe.get_traceback())
```

Queues are `short` (quick jobs, under a minute), `default` (1–5 min),
and `long` (heavy jobs, over 5 min, 25 min timeout). Always pass
`queue=` explicitly — never rely on the default.

## Checking health

```bash
bench doctor                                        # workers + scheduler alive?
bench --site mysite enable-scheduler                # turn the scheduler on
bench --site mysite trigger-scheduler-event daily   # run one event by hand
bench --site mysite execute my_app.tasks.notify_expiring_batches  # or run the fn directly
```

Desk → **Scheduler Log** shows when each event last ran and whether it
failed; failed jobs also write to the **Error Log** with the full
traceback. On Frappe Cloud shared benches there is no shell — manage the
scheduler from the dashboard.

## When to use — and when not to

| Situation | Use |
|---|---|
| Runs at a fixed time or interval | `scheduler_events` in hooks.py |
| Runs because a user did something | `frappe.enqueue()` from the controller / API |
| Work on one specific document | `frappe.enqueue_doc(doctype, name, method)` |
| Work over 5 minutes | `*_long` event or `queue="long"` |
| Work that must not run twice at once | `job_id=` + `is_job_enqueued()` check |
| Calling an external API | `on_submit` / `on_update` + `enqueue` — never in `validate` |
| A quick check the user waits for | Run it in the request — no job needed |

## Common mistakes

- **Arguments on a scheduled function.** The scheduler passes none — a
  `def daily_cleanup(company):` errors every tick.
- **A 20-minute job on the `daily` event.** The default queue kills it
  at 5 minutes. Use `daily_long` or `queue="long"`.
- **External API call in `validate`.** The user waits, the API is slow,
  the save times out. Enqueue from `on_submit` instead.
- **Passing a document to `enqueue`.** Jobs are serialised — pass names
  and IDs, then `frappe.get_doc` inside the job.
- **A job that is not idempotent.** Running twice must not double-post
  or double-charge. Store the external ID on the document and check it.
- **No `enqueue_after_commit`.** The job runs even if the save rolls
  back, on a document that was never saved.
- **Scheduler disabled on the dev site.** `bench new-site` leaves it
  off — run `enable-scheduler`, or the job "never runs".
- **Swallowing errors in a job.** A job that fails silently looks like
  a job that never ran. Catch, `frappe.log_error`, re-raise.
- **Forgetting `bench migrate` after editing `hooks.py`.** The scheduler
  keeps running the old list.

## Next

[12 — Notifications, Email & Integrations](12-notifications-email.md) —
telling people things happened: the Notification DocType, sending mail
from code, and webhooks.
