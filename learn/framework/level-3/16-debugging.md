# 16 — Debugging

## What it is

Debugging is not guessing. It is: reproduce it, read what the system
already told you, isolate the cause, fix it, prove it. Frappe tells you a
lot — a traceback, an Error Log row, a worker log line — but only if you
look in the right place instead of changing random code and hoping.

**Read a traceback bottom-up.** The last frame is where it failed; the
frames above it are how it got there. The exception type on the last line
is the diagnosis — `DoesNotExistError` and `ValidationError` are
different problems with different fixes.

## Minimal working example — walking a real traceback

A user submits a Gate Pass and gets a 500 error. The Error Log shows:

```
Traceback (most recent call last):
  File "apps/frappe/frappe/model/document.py", line 1123, in submit
    self._submit()
  File "apps/my_app/my_app/my_module/doctype/gate_pass/gate_pass.py", line 42, in on_submit
    approver = frappe.get_doc("User", self.approved_by)
frappe.exceptions.DoesNotExistError: User HR-EMP-0042 does not exist
```

Read it bottom-up:

1. **Last line first** — `DoesNotExistError: User HR-EMP-0042 does not
   exist`. The code asked for a User that isn't there.
2. **Your file, not Frappe's** — `gate_pass.py`, line 42, in `on_submit`.
   The framework frames above it are just the call path.
3. **The cause** — `approved_by` holds an employee ID, not a user email.
   The field was linked to the wrong DocType, or filled with the wrong
   value.
4. **The fix** — validate the link (or use `frappe.db.exists("User",
   self.approved_by)` before `get_doc`), and fix the bad data.

## Where the evidence lives

| Place | Shows |
|---|---|
| **Error Log** (Desk) | Every unhandled exception, with the full traceback |
| **Activity Log** (Desk) | Who did what, when — for "it worked yesterday" |
| `bench --site <site> console` | A live Python shell on the site — inspect any doc, run any function |
| `logs/` in the bench folder | `web.log`, `worker.log`, `scheduler.log`, `bench.log` |
| `bench doctor` | Are the workers and scheduler alive? (Lesson 11) |
| `bench --site <site> execute <dotted.path>` | Run one function by hand, outside any request |

```bash
# reproduce it in the console — faster than clicking through the form
bench --site mysite console
>>> doc = frappe.get_doc("Gate Pass", "GP-0007")
>>> doc.approved_by
'HR-EMP-0042'
>>> frappe.db.exists("User", "HR-EMP-0042")   # None — there it is
```

Log properly when you add logging. `print()` goes to a worker log nobody
reads and vanishes on Frappe Cloud. Use the Error Log:

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

## Common errors and their real causes

| Error | Real cause | Fix |
|---|---|---|
| `DoesNotExistError` (404) | `get_doc` on a missing record, or a wrong API path | `frappe.db.exists()` first; check `/api/method/dotted.path` |
| `ValidationError` (417) | A `frappe.throw` ran | Fix the input or the rule — the message says which |
| `PermissionError` (403) | Missing `@frappe.whitelist()`, role, or User Permission | Add the decorator / role / permission (Lesson 09) |
| `DuplicateEntryError` (409) | Unique / naming clash | Check exists first; fix `autoname` / naming series |
| `LinkValidationError` | A Link points to a record that doesn't exist | Create or validate the target |
| `LinkExistsError` | Delete blocked by linked documents | Show the links; cancel/delete dependents first |
| `TimestampMismatchError` | Document changed since it was loaded | Reload — `doc.reload()` / `frm.reload_doc()` |
| `MandatoryError` | A required field is empty | Set it before insert/save |
| `ImportError: __import__ not found` | `import` in a Server Script | Use `frappe.utils.*` (Lesson 05) |
| `CSRFTokenError` | Raw `fetch` call / stale session | Use `frappe.call()` |
| `AttributeError: module has no attribute` | Wrong dotted path in hooks.py | Match the function name and path exactly |
| Change not visible | Cache / assets / migrate | `clear-cache`, `bench build --app <app>`, `migrate` |
| Job never runs | Worker or scheduler off | `bench doctor`, `enable-scheduler` |

## Asking for help — what to paste

When you ask someone (or an AI) for help, paste these four things —
nothing else is needed, and without them nobody can help:

1. **The full traceback as text** — not a screenshot, not "it shows an
   error". Copy it from the Error Log.
2. **What you were doing** — "submitting Gate Pass GP-0007", one line.
3. **What you already tried** — "checked `approved_by`, it's an employee
   ID, not a user".
4. **Versions** — `bench version` output: Frappe, ERPNext, your app.

"My code doesn't work" with no traceback gets you guesses. A traceback
with versions gets you an answer.

## When to use — and when not to

| Situation | Use |
|---|---|
| Something broke | Reproduce it first — then read the traceback |
| "It worked yesterday" | Activity Log + `git log` — what changed? |
| A value looks wrong | `bench console` — inspect the live document |
| A job failed | Error Log + Scheduler Log (Lesson 11) |
| A user reports an error | Ask for the exact steps + the Error Log row |
| You have a theory | Test it in the console before editing code |

## Common mistakes

- **Guessing instead of reproducing.** Changing code before you can
  make the error happen on demand. Reproduce first, always.
- **Reading the traceback top-down.** The top is framework internals.
  The answer is at the bottom, in your file.
- **`print()` debugging in production.** It goes nowhere useful. Use
  `frappe.log_error` with the traceback.
- **Fixing the data, not the bug.** Deleting the bad Gate Pass hides
  the error for a week. Fix the link field that let it in.
- **Editing a submitted document to "fix" it.** Cancel and amend
  (Lesson: guides/common-mistakes.md) — an edited submitted document
  and its ledger disagree forever.
- **Pasting a screenshot of a traceback.** Text can be searched and
  copied. A screenshot can't.
- **Changing three things at once.** You won't know which one fixed it
  — or which one broke the next thing.

## Next

You have finished Level 3. You can schedule work and run it in the
background, notify people and other systems, test what you built, make
it fast, keep it secure, and find out why it broke when it breaks.

Level 4 starts with the no-code side of v16 — Studio and Flow:
[17 — Studio & Flow](../level-4/17-studio-flow.md).
