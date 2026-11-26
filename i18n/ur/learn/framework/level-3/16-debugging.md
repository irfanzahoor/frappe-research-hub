# 16 — Debugging

## Yeh kya hai

Debugging andaza lagana nahi hai. Yeh hai: usay reproduce karein, jo
system ne pehle se bata diya hai usay padhein, wajah ko isolate karein,
usay fix karein, prove karein. Frappe aapko bohat kuch batata hai — ek
traceback, Error Log ki row, worker log ki line — lekin sirf tab jab aap
random code badal kar umeed karne ke bajaye sahi jagah dekhein.

**Traceback ko neeche se upar padhein.** Aakhri frame woh hai jahan woh
fail hua; us ke upar wale frames batate hain ke woh wahan kaise pahuncha.
Aakhri line par exception type hi diagnosis hai — `DoesNotExistError`
aur `ValidationError` alag problems hain jin ke alag fixes hain.

## Minimal working example — asal traceback par chalna

Ek user Gate Pass submit karta hai aur 500 error milti hai. Error Log
dikhati hai:

```
Traceback (most recent call last):
  File "apps/frappe/frappe/model/document.py", line 1123, in submit
    self._submit()
  File "apps/my_app/my_app/my_module/doctype/gate_pass/gate_pass.py", line 42, in on_submit
    approver = frappe.get_doc("User", self.approved_by)
frappe.exceptions.DoesNotExistError: User HR-EMP-0042 does not exist
```

Usay neeche se upar padhein:

1. **Pehle aakhri line** — `DoesNotExistError: User HR-EMP-0042 does not
   exist`. Code ne aisa User manga jo hai hi nahi.
2. **Aapki file, Frappe ki nahi** — `gate_pass.py`, line 42, `on_submit`
   mein. Us ke upar wale framework frames sirf call path hain.
3. **Wajah** — `approved_by` mein user email ke bajaye employee ID hai.
   Field ghalat DocType se link tha, ya us mein ghalat value bhari gayi
   thi.
4. **Fix** — link ko validate karein (ya `get_doc` se pehle
   `frappe.db.exists("User", self.approved_by)` use karein), aur ghalat
   data ko fix karein.

## Evidence kahan rehta hai

| Jagah | Kya dikhati hai |
|---|---|
| **Error Log** (Desk) | Har unhandled exception, poore traceback ke saath |
| **Activity Log** (Desk) | Kis ne kab kya kiya — "kal tak kaam kar raha tha" ke liye |
| `bench --site <site> console` | Site par live Python shell — koi bhi doc inspect karein, koi bhi function chalyein |
| Bench folder mein `logs/` | `web.log`, `worker.log`, `scheduler.log`, `bench.log` |
| `bench doctor` | Kya workers aur scheduler zinda hain? (Lesson 11) |
| `bench --site <site> execute <dotted.path>` | Kisi request ke bahar ek function haath se chalyein |

```bash
# reproduce it in the console — faster than clicking through the form
bench --site mysite console
>>> doc = frappe.get_doc("Gate Pass", "GP-0007")
>>> doc.approved_by
'HR-EMP-0042'
>>> frappe.db.exists("User", "HR-EMP-0042")   # None — there it is
```

Jab logging add karein to theek se log karein. `print()` aise worker log
mein jata hai jisay koi nahi padhta aur Frappe Cloud par ghaib ho jata
hai. Error Log use karein:

```python
try:
    sync_supplier_stock()
except Exception:
    frappe.log_error(
        title="Supplier stock sync failed",
        message=frappe.get_traceback(),
    )
    raise
```

## Aam errors aur un ki asal wajah

| Error | Asal wajah | Fix |
|---|---|---|
| `DoesNotExistError` (404) | Missing record par `get_doc`, ya ghalat API path | Pehle `frappe.db.exists()`; `/api/method/dotted.path` check karein |
| `ValidationError` (417) | Koi `frappe.throw` chala | Input ya rule ko fix karein — message batata hai ke kaunsa |
| `PermissionError` (403) | Missing `@frappe.whitelist()`, role, ya User Permission | Decorator / role / permission add karein (Lesson 09) |
| `DuplicateEntryError` (409) | Unique / naming clash | Pehle exists check karein; `autoname` / naming series fix karein |
| `LinkValidationError` | Link aise record ki taraf hai jo hai hi nahi | Target banayein ya validate karein |
| `LinkExistsError` | Linked documents ki wajah se delete blocked hai | Links dikhayein; pehle dependents ko cancel/delete karein |
| `TimestampMismatchError` | Document load hone ke baad se badal gaya hai | Reload karein — `doc.reload()` / `frm.reload_doc()` |
| `MandatoryError` | Required field khaali hai | Insert/save se pehle usay set karein |
| `ImportError: __import__ not found` | Server Script mein `import` | `frappe.utils.*` use karein (Lesson 05) |
| `CSRFTokenError` | Raw `fetch` call / stale session | `frappe.call()` use karein |
| `AttributeError: module has no attribute` | hooks.py mein ghalat dotted path | Function ka naam aur path bilkul match karein |
| Change nazar nahi aati | Cache / assets / migrate | `clear-cache`, `bench build --app <app>`, `migrate` |
| Job kabhi nahi chalta | Worker ya scheduler band hai | `bench doctor`, `enable-scheduler` |

## Madad mangna — kya paste karein

Jab aap kisi se (ya AI se) madad mangein, to yeh chaar cheezein paste
karein — bas yahi chahiye, aur in ke baghair koi madad nahi kar sakta:

1. **Poora traceback text ke taur par** — screenshot nahi, "error dikh
   raha hai" nahi. Usay Error Log se copy karein.
2. **Aap kya kar rahe the** — "Gate Pass GP-0007 submit kar raha tha",
   ek line.
3. **Aap ne pehle se kya try kiya** — "`approved_by` check kiya, woh
   user nahi, employee ID hai".
4. **Versions** — `bench version` output: Frappe, ERPNext, aapki app.

Bina traceback ke "mera code kaam nahi kar raha" par aap ko andaze
milte hain. Versions ke saath traceback par jawab milta hai.

## Kab use karein — aur kab nahi

| Situation | Use karein |
|---|---|
| Kuch toot gaya | Pehle reproduce karein — phir traceback padhein |
| "Kal tak kaam kar raha tha" | Activity Log + `git log` — kya badla? |
| Koi value ghalat lagti hai | `bench console` — live document inspect karein |
| Koi job fail hui | Error Log + Scheduler Log (Lesson 11) |
| User error report karta hai | Exact steps + Error Log row mangein |
| Aap ke paas theory hai | Code edit karne se pehle console mein test karein |

## Aam ghaltiyan

- **Reproduce karne ke bajaye andaza lagana.** Error ko on demand
  laane se pehle code badalna. Pehle reproduce karein, hamesha.
- **Traceback ko upar se neeche padhna.** Upar framework internals
  hain. Jawab neeche hai, aapki file mein.
- **Production mein `print()` debugging.** Yeh kahin useful nahi jata.
  Traceback ke saath `frappe.log_error` use karein.
- **Bug ko nahi, data ko fix karna.** Ghalat Gate Pass delete karne se
  error ek hafte ke liye chhup jata hai. Us link field ko fix karein jis
  ne usay andar aane diya.
- **"Fix" karne ke liye submitted document edit karna.** Cancel aur
  amend karein (Lesson: guides/common-mistakes.md) — edit kiya hua
  submitted document aur us ka ledger hamesha ke liye disagree karte
  hain.
- **Traceback ka screenshot paste karna.** Text ko search aur copy kiya
  ja sakta hai. Screenshot ko nahi.
- **Ek saath teen cheezein badalna.** Aap ko pata nahi chalega ke kis
  ne fix kiya — ya kis ne agla masla paida kiya.

## Agla

Aap ne Level 3 mukammal kar liya hai. Aap kaam schedule kar sakte hain
aur usay background mein chala sakte hain, logon aur doosre systems ko
notify kar sakte hain, jo banaya hai usay test kar sakte hain, usay tez
bana sakte hain, secure rakh sakte hain, aur jab toot jaye to pata laga
sakte hain ke kyun toota.

Level 4 v16 ke no-code side se shuru hota hai — Studio aur Flow:
[17 — Studio & Flow](../level-4/17-studio-flow.md).
