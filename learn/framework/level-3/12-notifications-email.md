# 12 — Notifications, Email & Integrations

## What it is

Three ways Frappe tells someone something happened, and one way it tells
*another system*:

| Way | For |
|---|---|
| **Notification** DocType | No-code alerts on a document event — configurable by users, shipped as a fixture |
| **`frappe.sendmail()`** | Email from code, with full control over when and what |
| **`frappe.publish_realtime()`** | Live updates in the browser (the bell icon, a list refresh) |
| **Webhook** DocType | Frappe calls an external URL when a document event happens |

Email is queued, not sent instantly: `frappe.sendmail` puts a row in the
**Email Queue**, and the scheduler sends it. That is why mail needs a
working scheduler (Lesson 11) and an **Email Account** with "Enable
Outgoing" ticked.

## Minimal working example — Notification, no code

A Quality Inspection is rejected. The QA Manager and the person who
created it must know. Desk → **Notification** → New:

| Field | Value |
|---|---|
| Document Type | Quality Inspection |
| Event | Value Change |
| Value Changed | `status` |
| Condition | `doc.status == "Rejected"` |
| Channel | Email |
| Recipients | By Role: Quality Manager; By Document Field: `owner` |
| Subject | `Inspection {{ doc.name }} rejected` |
| Message | `Batch {{ doc.batch_no }} failed inspection. Reason: {{ doc.remarks }}` |

Events available: **New, Save, Submit, Cancel, Value Change, Days
Before, Days After, Method, Custom**. "Days Before/After" runs on a date
field — for example, remind the buyer 7 days before a supplier contract
ends. Conditions are Python expressions on `doc`. Messages are Jinja —
`{{ doc.name }}`, `{{ doc.customer }}`, any field on the document.

## Minimal working example — email from code

Same idea, but the logic decides who gets it. First add an `approved_by`
Link field (Options: User) to the Gate Pass DocType — who approved this
pass. Send from `on_submit` / `on_update`, never from `validate` —
validation may still fail, and then you emailed about a document that
was never saved.

```python
# my_app/my_module/doctype/gate_pass/gate_pass.py
import frappe
from frappe import _


class GatePass(Document):
    def on_submit(self):
        frappe.sendmail(
            recipients=[self.approved_by],
            subject=_("Gate Pass {0} submitted").format(self.name),
            message=_(
                "Gate Pass {0} for visitor {1} was submitted by {2}."
            ).format(self.name, self.visitor_name, frappe.session.user),
            reference_doctype=self.doctype,   # links the mail in the timeline
            reference_name=self.name,
        )
```

Keep the default queueing. Never `now=True` in production — it sends
inside the request, blocks the user, and on v16 it does not commit. Bulk
mail (hundreds of customers) goes through `frappe.enqueue` first.

A reusable body lives in an **Email Template** — a
`templates/emails/order_approved.html` file in your app, passed as
`template="order_approved", args={"doc": doc}` instead of `message=`.

## Email Account setup

Desk → **Email Account** → New: SMTP host/port and login for outgoing,
IMAP for incoming. Tick **Enable Outgoing** to send, **Enable Incoming**
to receive; incoming mail can create documents — set **Append To** to a
DocType. If mail never arrives, check in order: outgoing enabled →
**Email Queue** status and error → scheduler enabled (`bench doctor`) →
`mute_emails` in `site_config.json`.

## Minimal working example — realtime + webhook

Tell the browser a long job finished (Lesson 11), and tell the warehouse
system a Sales Order was submitted:

```python
# inside the background job, when it finishes
frappe.publish_realtime(
    "stock_check_done",
    {"sales_order": order.name, "shortages": shortages},
    user=frappe.session.user,
)
```

```js
// public/js/sales_order.js
frappe.realtime.on("stock_check_done", (data) => {
    frappe.msgprint(__("Stock check finished for {0}", [data.sales_order]));
});
```

Webhook — Desk → **Webhook** → New: Document Type **Sales Order**, Doc
Event **After Submit**, the warehouse system's URL, Method **POST**, and
a Jinja JSON body in Request Structure:

```json
{"order": "{{ doc.name }}", "customer": "{{ doc.customer }}", "items": {{ doc.items | tojson }}}
```

Set a **Webhook Secret** in production. The receiver verifies the
`X-Frappe-Webhook-Signature` header (HMAC-SHA256) to know the call
really came from your site. Incoming webhooks are the mirror image: a
whitelisted method that verifies the signature or token first, then
enqueues the processing — never processes a webhook inside the request.

## When to use — and when not to

| Situation | Use |
|---|---|
| Alert on a doc event, users may change the rule | Notification DocType |
| Email from code with custom logic | `frappe.sendmail()` |
| Live UI update (bell, list refresh) | `frappe.publish_realtime()` |
| Another system must know an event happened | Webhook DocType |
| Bulk mail to hundreds of recipients | `frappe.enqueue` + `sendmail` |
| A one-off email to one person | Share the document + a comment — no code |

## Common mistakes

- **`frappe.sendmail` in `validate`.** The save can still fail after
  the mail went out. Send from `on_submit` / `on_update`.
- **`now=True` in production.** It blocks the request and, on v16, does
  not commit. Queue the mail and let the scheduler send it.
- **No Email Account with outgoing enabled.** `sendmail` queues the
  mail, the queue never sends, and nobody notices for a week.
- **A Notification with no condition** on a busy DocType. Every save of
  every Sales Order emails the whole team.
- **Secrets in a webhook URL or a Notification.** Keys live in
  `site_config.json` or a Password field (Lesson 15), never in a URL.
- **No timeout on an external call.** A hung supplier API hangs your
  worker. Always `timeout=30`, try/except, `frappe.log_error`.
- **Processing a webhook in the request.** Verify, enqueue, return. The
  sender retries if you are slow, and you process it twice.

## Next

[13 — Testing](13-testing.md) — proving the code works before the client
finds out it doesn't: unit tests, test data, and UI tests.
