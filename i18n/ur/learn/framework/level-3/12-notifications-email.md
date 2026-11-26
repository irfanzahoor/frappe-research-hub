# 12 — Notifications, Email & Integrations

## Yeh kya hai

Teen tareeqe jin se Frappe kisi ko batata hai ke kuch hua, aur ek
tareeqa jin se woh *doosre system* ko batata hai:

| Tareeqa | Kis liye |
|---|---|
| **Notification** DocType | Document event par no-code alerts — users configure kar sakte hain, fixture ke taur par ship hota hai |
| **`frappe.sendmail()`** | Code se email, poore control ke saath ke kab aur kya bhejna hai |
| **`frappe.publish_realtime()`** | Browser mein live updates (bell icon, list refresh) |
| **Webhook** DocType | Jab document event ho to Frappe kisi external URL ko call karta hai |

Email foran nahi bheji jati, queue hoti hai: `frappe.sendmail` **Email
Queue** mein ek row daalta hai, aur scheduler usay bhejta hai. Isi liye
mail ke liye working scheduler chahiye (Lesson 11) aur ek **Email
Account** jis mein "Enable Outgoing" tick ho.

## Minimal working example — Notification, bina code

Ek Quality Inspection reject ho jati hai. QA Manager aur jis ne usay
banaya tha, dono ko pata hona chahiye. Desk → **Notification** → New:

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

Events yeh hain: **New, Save, Submit, Cancel, Value Change, Days
Before, Days After, Method, Custom**. "Days Before/After" date field par
chalta hai — misaal ke taur par, supplier contract khatam hone se 7 din
pehle buyer ko remind karein. Conditions `doc` par Python expressions
hain. Messages Jinja hain — `{{ doc.name }}`, `{{ doc.customer }}`,
document ka koi bhi field.

## Minimal working example — code se email

Wohi idea, lekin logic tay karta hai ke kis ko milegi. Pehle Gate Pass
DocType mein ek `approved_by` Link field (Options: User) add karein — kis
ne yeh pass approve kiya. `on_submit` / `on_update` se bhejein, kabhi
`validate` se nahi — validation abhi bhi fail ho sakti hai, aur phir aap
ne aise document ke baare mein email kar diya jo kabhi save hua hi nahi.

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

Default queueing hi rakhein. Production mein kabhi `now=True` na dein —
yeh request ke andar bhejta hai, user ko rokta hai, aur v16 par yeh
commit nahi karta. Bulk mail (saikron customers) pehle
`frappe.enqueue` se jati hai.

Reusable body **Email Template** mein hoti hai — aapki app mein
`templates/emails/order_approved.html` file, jo `message=` ke bajaye
`template="order_approved", args={"doc": doc}` ke taur par pass hoti hai.

## Email Account setup

Desk → **Email Account** → New: outgoing ke liye SMTP host/port aur
login, incoming ke liye IMAP. Bhejne ke liye **Enable Outgoing** tick
karein, receive karne ke liye **Enable Incoming**; incoming mail
documents bana sakti hai — **Append To** ko kisi DocType par set karein.
Agar mail kabhi nahi aati, to is order mein check karein: outgoing
enabled → **Email Queue** status aur error → scheduler enabled
(`bench doctor`) → `site_config.json` mein `mute_emails`.

## Minimal working example — realtime + webhook

Browser ko batayein ke lamba job khatam ho gaya (Lesson 11), aur
warehouse system ko batayein ke Sales Order submit ho gaya:

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
Event **After Submit**, warehouse system ka URL, Method **POST**, aur
Request Structure mein Jinja JSON body:

```json
{"order": "{{ doc.name }}", "customer": "{{ doc.customer }}", "items": {{ doc.items | tojson }}}
```

Production mein **Webhook Secret** set karein. Receiver
`X-Frappe-Webhook-Signature` header (HMAC-SHA256) ko verify karta hai
taake pata chale ke call waqai aapki site se aayi hai. Incoming webhooks
is ka ulta hain: ek whitelisted method jo pehle signature ya token
verify karta hai, phir processing ko enqueue karta hai — kabhi bhi
webhook ko request ke andar process nahi karta.

## Kab use karein — aur kab nahi

| Situation | Use karein |
|---|---|
| Doc event par alert, users rule badal sakte hain | Notification DocType |
| Custom logic ke saath code se email | `frappe.sendmail()` |
| Live UI update (bell, list refresh) | `frappe.publish_realtime()` |
| Doosre system ko pata hona chahiye ke event hua | Webhook DocType |
| Hundredon recipients ko bulk mail | `frappe.enqueue` + `sendmail` |
| Ek shakhs ko one-off email | Document share karein + comment — koi code nahi |

## Aam ghaltiyan

- **`validate` mein `frappe.sendmail`.** Mail jaane ke baad bhi save
  fail ho sakta hai. `on_submit` / `on_update` se bhejein.
- **Production mein `now=True`.** Yeh request ko rokta hai aur, v16
  par, commit nahi karta. Mail ko queue karein aur scheduler ko bhejne
  dein.
- **Koi Email Account jis mein outgoing enabled ho.** `sendmail` mail
  ko queue karta hai, queue kabhi bhejti nahi, aur kisi ko ek hafte tak
  pata nahi chalta.
- **Busy DocType par bina condition ke Notification.** Har Sales Order
  ke har save par poori team ko email jati hai.
- **Webhook URL ya Notification mein secrets.** Keys
  `site_config.json` mein ya Password field mein hoti hain (Lesson 15),
  kabhi URL mein nahi.
- **External call par koi timeout nahi.** Hung supplier API aapke worker
  ko hang kar deta hai. Hamesha `timeout=30`, try/except,
  `frappe.log_error`.
- **Request ke andar webhook process karna.** Verify karein, enqueue
  karein, return karein. Sender retry karta hai agar aap slow hon, aur
  aap usay do baar process karte hain.

## Agla

[13 — Testing](13-testing.md) — code kaam karta hai yeh prove karna,
is se pehle ke client ko pata chale ke nahi karta: unit tests, test
data, aur UI tests.
