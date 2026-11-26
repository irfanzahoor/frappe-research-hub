# Cheat Sheets — Frappe & ERPNext Quick Reference

Ye woh pages hain jo kaam karte waqt khulay rakhnay chahiye. Koi lambi
wazahat nahi — sirf command, hook, ya call, aur aik line ke yeh kya
karta hai. Agar "kyun" jan'na ho to linked lesson parh lein. `<site>`
ka matlab hai aap ki site ka naam, masalan `erp.local`.

---

## 1. Bench commands

Ye commands apni bench directory (`~/frappe-bench`) ke andar se
chalayein. `bench --site <site> <command>` aik site ko target karta
hai; aik dafa `bench use <site>` chala lein to us ke baad
`--site <site>` likhnay ki zaroorat nahi.

| Command | Kya karta hai |
|---|---|
| `bench --version` | Bench CLI ka version dikhata hai |
| `bench version` | Bench par mojood har app ka version dikhata hai |
| `bench init <name>` | Nayi bench banata hai (home directory se chalao) |
| `bench new-site <site>` | Nayi site banata hai |
| `bench use <site>` | `<site>` ko default bana deta hai, to `--site` likhna zaroori nahi |
| `bench get-app <app>` | App ko `apps/` mein download karta hai (naam ya git URL) |
| `bench --site <site> install-app <app>` | Site par app install karta hai |
| `bench --site <site> uninstall-app <app>` | Site se app hata deta hai |
| `bench --site <site> list-apps` | Site par installed apps ki list dikhata hai |
| `bench start` | Dev server chalata hai (foreground mein — `Ctrl+C` se band hota hai) |
| `bench restart` | Bench ki tamam services restart karta hai (workers, scheduler, web) |
| `bench --site <site> migrate` | Site ke liye database migrations / patches chalata hai |
| `bench build` | Tamam apps ke JS + CSS assets dobara banata hai |
| `bench build --app <app>` | Sirf aik app ke assets dobara banata hai |
| `bench update` | Sab kuch aik saath — pull + migrate + build + restart |
| `bench --site <site> backup` | Site ke database ka backup leta hai |
| `bench --site <site> backup --with-files` | Database + public aur private files ka backup |
| `bench --site <site> restore <file>` | Backup file se site restore karta hai |
| `bench --site <site> clear-cache` | Site ka cache saaf karta hai (purani lists, puranay values) |
| `bench --site <site> console` | Python console, Frappe loaded — cheezein live try karo |
| `bench --site <site> mariadb` | Site ke liye MariaDB console kholta hai |
| `bench doctor` | Health check: scheduler, workers, Redis, Socket.IO |
| `bench --site <site> enable-scheduler` | Site ke liye scheduler on karta hai |
| `bench --site <site> disable-scheduler` | Site ke liye scheduler off karta hai |
| `bench --site <site> set-config <key> <value>` | `site_config.json` mein value set karta hai |
| `bench --site <site> show-config` | Site ki current config dikhata hai |
| `bench --site <site> execute <dotted.path>` | Aik Python function chalata hai, masalan `bench --site <site> execute frappe.utils.scheduler.enqueue_scheduler_events` |
| `bench drop-site <site>` | Site delete karta hai (khatarnak — pehle backup lein) |

!!! warning "`bench update` ya `bench restore` se pehle"
    Pehle backup lein: `bench --site <site> backup`. Jo update wapas
    li ja sakti hai, wohi update try ki ja sakti hai. Agar update
    aadhi mein fail ho jaye to [Troubleshooting](troubleshooting.md)
    dekhein.

---

## 2. Hooks (`hooks.py`)

Ye sab aap ki app ki `hooks.py` mein likhay jatay hain. Har aik ki aik
line — shape copy karein, naam badal lein.

| Hook | Chhoti si misaal |
|---|---|
| `doc_events` | `doc_events = {"Sales Order": {"on_submit": "my_app.api.on_sales_order_submit"}}` |
| `before_insert` | `"Sales Order": {"before_insert": "my_app.api.set_defaults"}` — pehli save se pehle chalta hai |
| `validate` | `"Sales Order": {"validate": "my_app.api.check_credit_limit"}` — har save par chalta hai, insert/update se pehle |
| `on_submit` | `"Sales Order": {"on_submit": "my_app.api.create_gate_pass"}` — jab document submit hota hai |
| `on_cancel` | `"Sales Order": {"on_cancel": "my_app.api.reverse_gate_pass"}` — jab submitted document cancel hota hai |
| `after_migrate` | `after_migrate = "my_app.setup.after_migrate"` — har `bench migrate` ke baad aik dafa chalta hai |
| `fixtures` | `fixtures = ["Custom Field", "Property Setter"]` — ye DocTypes app ke saath export hoti hain |
| `scheduler_events` | `scheduler_events = {"daily": ["my_app.tasks.send_daily_report"], "hourly": ["my_app.tasks.sync_stock"], "cron": {"0 9 * * *": ["my_app.tasks.morning_job"]}, "all": ["my_app.tasks.every_minute"]}` |
| `override_doctype_class` | `override_doctype_class = {"Sales Order": "my_app.overrides.CustomSalesOrder"}` |
| `permission_query_conditions` | `permission_query_conditions = {"Sales Order": "my_app.permissions.sales_order_condition"}` |
| `get_permission_query_conditions` | `get_permission_query_conditions = {"Sales Order": "my_app.permissions.sales_order_condition"}` — isi hook ki nayi form |
| `jinja` | `jinja = {"methods": ["my_app.utils.format_amount"], "filters": ["my_app.utils.to_words"]}` |
| `page_js` | `page_js = {"sales-order": "public/js/sales_order_list.js"}` — aik Desk page par JS |
| `app_include_js` | `app_include_js = "/assets/my_app/js/my_app.js"` — har Desk page par JS |
| `app_include_css` | `app_include_css = "/assets/my_app/css/my_app.css"` — har Desk page par CSS |
| `website_route_rules` | `website_route_rules = [{"from_route": "/track/<order_id>", "to_route": "track-order"}]` |
| `notification_config` | `notification_config = "my_app.notifications.get_notification_config"` |

!!! tip "Doc events vs `validate`"
    `validate` **har** save par chalta hai; `before_insert` sirf pehli
    save par; `on_submit` / `on_cancel` sirf submitted documents par.
    Jo event sab se chhota ho aur kaam aa jaye, wohi chun lein —
    Lesson 05 dekhein.

---

## 3. Server Script / API essentials

```python
# Parhna (Read)
doc = frappe.get_doc("Sales Order", "SO-0001")      # aik document, naam se
docs = frappe.get_list("Sales Order",
    filters={"status": "To Deliver"}, fields=["name", "customer"])
rows = frappe.get_all("Item", filters={"is_stock_item": 1},
    fields=["item_code", "item_name"])              # get_list jaisa, permissions ke baghair
value = frappe.db.get_value("Customer", "CUST-001", "customer_name")

# Banana / badalna (Create / change)
doc = frappe.new_doc("Gate Pass")
doc.visitor_name = "Ahmed"
doc.insert()                                        # draft ke tor par save
doc.submit()                                        # submit karein (submittable DocType chahiye)
frappe.db.set_value("Sales Order", "SO-0001", "status", "Closed")

# SQL — hamesha parameterised, kabhi string formatting nahi
frappe.db.sql(
    "select name from `tabSales Order` where customer=%s and status=%s",
    ("CUST-001", "To Deliver"))

# User se baat karna
frappe.msgprint("Gate Pass created")                # sabz (green) message
frappe.throw("Credit limit exceeded")               # laal error, save ruk jata hai
```

!!! danger "SQL kabhi f-strings se na banayein"
    `frappe.db.sql(f"... where customer='{name}'")` SQL injection ka
    rasta kholta hai. Values hamesha doosri argument ke tor par dein,
    `%s` placeholders ke saath — jaisa upar dikhaya gaya hai.

```python
# Function ko browser ke liye khol dein
@frappe.whitelist()
def create_gate_pass(sales_order):
    ...
```

```javascript
// Client Script se call karein
frappe.call({
    method: "my_app.api.create_gate_pass",
    args: { sales_order: frm.doc.name },
    callback: function(r) {
        frappe.msgprint(r.message);
    }
});
```

```javascript
// Client Script ka skeleton — frm form hai, cur_frm nahi
frappe.ui.form.on("Sales Order", {
    refresh: function(frm) {
        // form khulnay ya refresh honay par har dafa chalta hai
    },
    customer: function(frm) {
        // jab customer field badlay
    },
    validate: function(frm) {
        // save se pehle chalta hai — yahan frappe.throw() save rok deta hai
    }
});
```

!!! tip "`frm` vs `cur_frm`"
    `frm` woh form object hai jo aap ke function ko milta hai — isi
    ko use karein. `cur_frm` purana global hai jo us form ki taraf
    ishara karta hai jo us waqt khula ho. Naye code mein hamesha `frm`
    use karein.

**Filters jo asal mein kaam aatay hain:** `{"status": "Open"}` (barabar),
`{"status": ["!=", "Cancelled"]}` (barabar nahi),
`{"creation": [">", "2026-01-01"]}` (comparison),
`{"name": ["in", ["SO-0001", "SO-0002"]]}` (list mein se),
`{"customer": ["like", "%Ahmed%"]}` (jazwi match).

---

## 4. DocType field types

| Type | Kab use karein |
|---|---|
| Data | Chhota aik line ka text — naam, code, phone number |
| Link | Kisi doosri DocType ka hawala (Customer, Item, Warehouse) |
| Select | Options ki fixed list, user aik chun le |
| Check | Haan/na ka checkbox |
| Date | Calendar ki tareekh, time ke baghair |
| Datetime | Tareekh + time (kab banaya gaya, kab scheduled hai) |
| Currency | Paisa — is ke saath hamesha currency field bhi rakhein |
| Float | Decimal number jo paisa na ho (rate, wazan) |
| Int | Poora number (quantity, count) |
| Text | Chand lines ka text — addresses, chhoti notes |
| Long Text | Lamba aazad text — descriptions, remarks |
| Table | Child table — line items, masalan Gate Pass Item |
| Attach | Aik file upload |
| HTML | Form par dikhaya janay wala formatted text (hidayat, banners) |
| Button | Click honay wala button jo code chalata hai |
| Section Break | Form par naya labelled section shuru karta hai |
| Column Break | Current section ko columns mein baant deta hai |
| Tab Break | Form par naya tab shuru karta hai |

!!! tip "Layout ka usool"
    Section Break → fields → Column Break → fields. Jis field ke
    upar Section Break na ho, woh ghalat jagah par aa jata hai.
    [Aam ghaltiyan](common-mistakes.md) dekhein.

---

## 5. Permissions & roles

| Role | Aam tor par kya control karta hai |
|---|---|
| Administrator | Sab kuch — built-in super user |
| System Manager | Setup, users, roles, customisations (data nahi) |
| Sales User / Sales Manager | Selling: Quotation, Sales Order, Delivery Note, Customer |
| Stock User / Stock Manager | Stock: Item, Warehouse, Stock Entry, Stock Ledger |
| Accounts User / Accounts Manager | Accounting: invoices, payments, journals, reports |
| HR User / HR Manager | Employee, Leave, Attendance, Payroll |
| Manufacturing User / Manufacturing Manager | BOM, Work Order, Production |
| Projects User / Projects Manager | Project, Task, Timesheet |
| Support Team | Issue, Helpdesk tickets |
| Customer / Supplier | Sirf portal access — apne orders, invoices, tickets |
| Guest | Sirf public website pages, Desk access nahi |
| All | Har logged-in user (ahtiyat se use karein — is ka matlab hai sab) |

Permissions **Role Permission Manager** mein milti hain (awesome bar
mein search karein): DocType chunein, role chunein, Read / Write /
Create / Submit / Cancel / Delete tick karein, aur field-level control
ke liye **permlevel** set karein. Print/export/share usi row par alag
checkboxes hain.

### Woh 3 permission ghaltiyan jo sab se zyada nuqsan deiti hain

1. **JS mein field chhupana security nahi hai.** Koi bhi field ko API
   ke zariye parh sakta hai. Ise permlevel se chhupayein, JavaScript
   se nahi.
2. **Baghair wajah `ignore_permissions=True`.** Agar aap ise pass
   karte hain to saath mein comment mein wajah likhein — warna agla
   developer ise har jagah copy kar lega.
3. **`allow_guest=True` kisi aisi cheez par jo likhti ho.** Guest
   endpoints sirf parhnay ke liye hain, rate-limited hain, aur unhein
   har input validate karna chahiye.

Mukammal lesson: [Lesson 09 — Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md).

---

## Aagay kya parhein

- Lesson 02 — [Bench, Sites & Apps](../learn/framework/level-1/02-bench-sites-apps.md) — bench setup ke liye
- Lesson 05 — [Server Scripts & Document Events](../learn/framework/level-2/05-server-scripts-events.md) — hooks aur server code ke liye
- Lesson 06 — [Client Scripts](../learn/framework/level-2/06-client-scripts.md) — `frappe.ui.form.on` ke liye
- Lesson 07 — [APIs](../learn/framework/level-2/07-apis.md) — `frappe.whitelist` aur `frappe.call` ke liye
- Lesson 09 — [Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md) — mukammal permissions model
- [Troubleshooting](troubleshooting.md) — jab upar wala koi command fail ho jaye
