# 15 — Security

## What it is

Assume every input is hostile: form fields, URL parameters, file
uploads, webhook payloads, imported rows. The framework gives you safe
APIs — use them, don't work around them. Most security bugs in Frappe
apps are not exotic attacks; they are a developer passing
`ignore_permissions=True` "to make it work" and leaving it there.

## Minimal working example — a search endpoint, wrong and right

A customer portal needs to search items by name. The first version
works — and lets anyone read any table:

```python
# ❌ SQL injection + no permission check
@frappe.whitelist()
def search_items(q):
    return frappe.db.sql(
        f"SELECT name, item_name FROM `tabItem` WHERE item_name LIKE '%{q}%'"
    )
```

```python
# ✅ parameterised, permission-checked, user-facing read
@frappe.whitelist()
def search_items(q):
    frappe.has_permission("Item", "read", throw=True)
    return frappe.get_list("Item",
        filters={"item_name": ("like", f"%{q}%")},
        fields=["name", "item_name"],
        limit_page_length=20)
```

Three fixes in one: the query is parameterised (`frappe.get_list`
builds the SQL for you), the method checks the caller's permission
**before** returning data, and the result is limited. Whitelisting does
**not** check permissions for you — every `@frappe.whitelist()` method
must do it itself.

SQL injection, stated plainly — never build SQL from user input:

| Wrong | Right |
|---|---|
| `frappe.db.sql(f"... where name='{user}'")` | `frappe.db.sql("... where name=%s", user)` |
| `"... where name='" + name + "'"` | `frappe.qb.from_("User").select("*").where(Field("name") == name)` |

Placeholders work for values only. A table or column name from input
can't be a placeholder — validate it against a fixed allowlist first.

## XSS — Jinja does not autoescape

Frappe renders Jinja in a sandbox, but it does **not** escape HTML.
`{{ doc.remarks }}` in a print format, email, or web template renders
raw HTML — including a `<script>` a user typed into a remarks field.

| Wrong | Right |
|---|---|
| `{{ doc.remarks }}` in a print format | `{{ doc.remarks \| e }}` |
| `{{ html \| safe }}` on user content | `\|safe` only on HTML your own code generated |
| `$(el).html(frm.doc.notes)` in JS | `$(el).text(frm.doc.notes)` |

## Permissions — the rules that get broken

- **`ignore_permissions=True` only with a comment** explaining why —
  for example, a system-generated document in a method that already
  checked a business rule. Without the comment, the next developer
  copies it everywhere.
- **`allow_guest=True` only for truly public endpoints** (signup, public
  page data). A guest method must never return private data or accept
  writes without its own validation. Rate-limit guest endpoints with
  `@frappe.rate_limit`.
- **`frappe.get_list` is permission-aware; `frappe.get_all` is not.**
  User-facing reads use `get_list` (Lesson 14).
- **Don't trust request parameters for identity.** Use
  `frappe.session.user`, never a `user` value from `frappe.form_dict`.
- **Hiding a field in JS is not security.** Anyone can read it through
  the API. Use permlevel (field-level permission, Lesson 09).

## Secrets and API keys

| Wrong | Right |
|---|---|
| API key in code, fixtures, or a committed JSON | `bench set-config <key> <value>` — site_config.json is not in git |
| Password in a Data field | `Password` fieldtype — encrypted at rest; read with `frappe.utils.password.get_decrypted_password` |
| Token in a Client Script / JS | Keep it server-side; expose only via a whitelisted method that checks permission |

Read site config with `frappe.get_site_config()` / `frappe.conf`. Never
log secrets, never put them in error messages or test data. A leaked
secret must be **rotated** immediately — deleting the file doesn't remove
it from git history.

API access: create a **dedicated API user** with minimal roles, never use
Administrator keys. Calls authenticate with
`Authorization: token <api_key>:<api_secret>`. Rotate keys when someone
leaves; a key that never expires is a key that never stops working.

## Files and audit

Uploads attached to documents are `File` docs with `is_private`. Private
files need a logged-in user with permission on the attached document to
download. Don't serve user files from `public/`, don't link a private
file's `file_url` on a guest page, and validate uploads server-side
before saving.

For audit: turn on **Track Changes** on sensitive DocTypes — every change
is kept as a Version you can review. The **Activity Log** shows who did
what and when. When something goes wrong, the first question is always
"who changed this, and when?" — the logs must be able to answer it.

## When to use — and when not to

| Situation | Use |
|---|---|
| User input in a query | Placeholders / `frappe.qb` / `get_list` filters |
| User text in a template | `\| e` escape; `\|safe` never on user content |
| A system action the user can't do | `ignore_permissions=True` + a comment, after a check |
| A public page or form | `allow_guest`, validate every input, show no internal data |
| A secret, key, or token | site_config or a Password field — never code or JS |
| An external system calling in | Dedicated API user, minimal roles, rotate keys |

## Common mistakes

- **F-string SQL.** The single most dangerous line in a Frappe app.
  One `f"..."` with user input and the whole database is readable.
- **`ignore_permissions=True` without a comment.** It spreads. The
  next developer copies it because "it worked last time".
- **`allow_guest=True` on a method that writes.** Guest endpoints are
  public. Anyone on the internet can call them.
- **Administrator API keys in an integration.** One leaked key is full
  control. Dedicated user, minimal roles, rotated keys.
- **Secrets in git.** A key committed once lives in history forever.
  Rotate it, then remove it — in that order.
- **Private files linked from a guest page.** `is_private` means
  nothing if you hand out the URL.
- **"Hidden" fields as security.** JS hiding and hidden fields are UX.
  The API returns what the DocType allows — use permlevel.

## Next

[16 — Debugging](16-debugging.md) — when it breaks anyway: reading a
traceback, the logs, `bench console`, and the errors every Frappe
developer meets.
