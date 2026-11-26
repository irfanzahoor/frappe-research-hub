# 11 — Scheduler, Background Jobs & Queues

## Yeh kya hai

Do alag cheezein hain jinhe beginners mix kar dete hain:

- **Scheduler** code ko ghadi par chalata hai — har ghante, har din, raat
  2 baje. Aap kaam ko `hooks.py` mein `scheduler_events` mein register
  karte hain. Scheduler aapka code nahi chalata; woh sirf usay
  **enqueue** karta hai. Ek worker process usay Redis queue se uthata hai
  aur chalata hai.
- **Background job** code ko *abhi, lekin request ke andar nahi* chalata
  hai. Aap usay `frappe.enqueue()` se shuru karte hain — misaal ke taur
  par, jab user "Generate report" par click kare aur report ko do minute
  lagte hon. User ko foran jawab mil jata hai; kaam background mein
  mukammal hota hai.

Agar in mein se koi bhi hissa band ho — scheduler, workers, ya Redis —
to kuch nahi chalta, aur user ko kuch nazar nahi aata. Isi liye "job kabhi
chali hi nahi" ek debugging sawal hai (Lesson 16), code ka sawal nahi.

## Minimal working example — spice batch expiry check

Har subah, woh spice batches dhoondhein jo 30 din ke andar expire ho
rahe hon aur QA Manager ko email karein. Scheduled kaam **koi arguments
nahi leta** — scheduler koi argument nahi bhejta.

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

`hooks.py` mein koi bhi tabdeeli ke baad `bench --site <site> migrate`
chalayein, warna scheduler naya event kabhi nahi dekhta.

| Event key | Kab | Queue |
|---|---|---|
| `all` | Har tick (v15+: 60s) | default — kabhi bhi 60s se zyada kaam nahi |
| `hourly` / `daily` / `weekly` / `monthly` | Har ghante / din / hafte / mahine | default (5 min timeout) |
| `hourly_long` / `daily_long` / `weekly_long` / `monthly_long` | Wohi waqt | long (25 min timeout) |
| `cron` | Koi bhi cron expression, misaal `0 2 * * *` | default, jab tak aap khud long mein enqueue na karein |

## Minimal working example — button se ek lamba job

Ek user Sales Order submit karta hai aur 3 warehouses mein
stock-availability check chahta hai. Is mein minutes lagte hain — yeh
request ke andar nahi chalna chahiye:

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

Queues hain `short` (chhote jobs, ek minute se kam), `default` (1–5 min),
aur `long` (bhaari jobs, 5 min se zyada, 25 min timeout). Hamesha
`queue=` saaf taur par dein — kabhi default par bharosa na karein.

## Health check karna

```bash
bench doctor                                        # workers + scheduler alive?
bench --site mysite enable-scheduler                # turn the scheduler on
bench --site mysite trigger-scheduler-event daily   # run one event by hand
bench --site mysite execute my_app.tasks.notify_expiring_batches  # or run the fn directly
```

Desk → **Scheduler Log** dikhata hai ke har event aakhri baar kab chala
aur kya woh fail hua; fail hone wale jobs **Error Log** mein bhi likhte
hain, poore traceback ke saath. Frappe Cloud shared benches par koi shell
nahi hoti — scheduler ko dashboard se manage karein.

## Kab use karein — aur kab nahi

| Situation | Use karein |
|---|---|
| Kisi fixed waqt ya interval par chalta hai | `scheduler_events` in hooks.py |
| Is liye chalta hai ke user ne kuch kiya | `frappe.enqueue()` controller / API se |
| Ek khaas document par kaam | `frappe.enqueue_doc(doctype, name, method)` |
| 5 minute se zyada ka kaam | `*_long` event ya `queue="long"` |
| Kaam jo ek saath do baar nahi chalna chahiye | `job_id=` + `is_job_enqueued()` check |
| External API ko call karna | `on_submit` / `on_update` + `enqueue` — kabhi `validate` mein nahi |
| Ek quick check jiska user intezar karta hai | Request ke andar hi chalayein — job ki zaroorat nahi |

## Aam ghaltiyan

- **Scheduled function par arguments.** Scheduler koi argument nahi
  bhejta — `def daily_cleanup(company):` har tick par error dega.
- **`daily` event par 20 minute ka job.** Default queue usay 5 minute
  par maar deta hai. `daily_long` ya `queue="long"` use karein.
- **`validate` mein external API call.** User intezar karta hai, API
  slow hoti hai, save timeout ho jata hai. Is ke bajaye `on_submit` se
  enqueue karein.
- **`enqueue` ko document dena.** Jobs serialise hote hain — naam aur
  IDs dein, phir job ke andar `frappe.get_doc` karein.
- **Aisa job jo idempotent nahi hai.** Do baar chalne se double-post ya
  double-charge nahi hona chahiye. External ID ko document par save
  karein aur check karein.
- **`enqueue_after_commit` na dena.** Job tab bhi chalta hai jab save
  rollback ho jaye, aise document par jo kabhi save hua hi nahi.
- **Dev site par scheduler disabled.** `bench new-site` usay band
  chhod deta hai — `enable-scheduler` chalyein, warna job "kabhi nahi
  chalti".
- **Job mein errors ko chhupana.** Aisa job jo khamoshi se fail ho,
  aisa lagta hai jaise job kabhi chala hi nahi. Catch karein,
  `frappe.log_error` karein, phir re-raise karein.
- **`hooks.py` edit karne ke baad `bench migrate` bhool jana.**
  Scheduler purani list hi chalata rehta hai.

## Agla

[12 — Notifications, Email & Integrations](12-notifications-email.md) —
logon ko batana ke kuch hua: Notification DocType, code se mail bhejna,
aur webhooks.
