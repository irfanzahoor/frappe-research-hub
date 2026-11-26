# 09 — Permissions & Roles

## What it is

Access is granted only when **every** layer allows it. Four layers, in
order — a failure at any one of them means "no":

1. **Role permission** — what a role may do on a DocType (read, write,
   create, submit, cancel, print, export, report…).
2. **User Permission** — which documents: a user restricted to one Company
   or Branch sees only that company's records.
3. **Sharing** — one document, shared with one user, as an exception.
4. **`has_permission` hook** — code that decides on one document.

Desk and `/api/resource/...` run the **same** checks. If it works in Desk
but fails from the API, the API user (the token owner) lacks the role.

## Minimal working example — Gate Pass access

**1. Role permissions** — Desk → **Role Permissions Manager**, DocType:
Gate Pass. Set **Is Submittable** on the DocType first (Lesson 05), then:

| Role | Read | Write | Create | Submit | Cancel |
|---|---|---|---|---|---|
| Gate Security | ✓ | ✓ | ✓ | — | — |
| Store Manager | ✓ | ✓ | ✓ | ✓ | ✓ |
| Auditor | ✓ | — | — | — | — |

A role with no read permission cannot open the DocType at all — sharing
one document does not fix that.

**2. Field-level permission (permlevel).** The `remarks` field holds
internal notes. Set its **Permlevel** to `1` on the DocType, then in Role
Permissions Manager give level 1 read only to Store Manager. Gate
Security sees the form — without the remarks field.

**3. User Permission** — one gate user sees only one company:

```python
frappe.permissions.add_user_permission("Company", "NexTash Pvt Ltd", "gate.security@example.com")
```

It filters lists, links and reports. A user who sees an empty list
usually has a User Permission hiding the documents, not a missing share.

**4. Sharing** — one document, one user, as an exception:

```python
frappe.share.add("Gate Pass", "GP-2026-0001", "auditor@example.com", read=1)
frappe.share.remove("Gate Pass", "GP-2026-0001", "auditor@example.com")
```

Sharing grants access to that one document only. It does **not** replace
the role permission — the user still needs read on the DocType. Routine
access belongs in roles, not in shares.

Check in code the same way the framework does:

```python
frappe.has_permission("Gate Pass", "read", doc, throw=True)
```

## When to use — and when not to

| Situation | Use |
|---|---|
| A whole team needs a DocType | Role permission (Role Permissions Manager) |
| One user must see only one Company / Branch | User Permission |
| One document for one outside person, once | Sharing |
| A rule code must decide ("only the owner, or a manager") | `has_permission` hook — on v16 it **must return an explicit `True`**; returning `None` denies access |
| Hiding a field from a role | permlevel — never JS |
| A report or page for one role only | Role Permission for Page and Report |

## Common mistakes

- **Hiding a field in JS is not security.** Anyone can read the field
  through the API. Use permlevel.
- **`ignore_permissions=True` without a reason.** If you pass it, write
  the reason in a comment next to it — otherwise the next developer
  copies it everywhere.
- **`allow_guest=True` on anything that writes.** Guest endpoints are
  read-only, rate-limited, and must validate every input.
- **`has_permission` returning `None` on v16.** On v14/v15 `None` meant
  "no opinion"; on v16 it denies access. Return `True` explicitly.
- **Sharing is not a role.** Sharing one document gives access to that
  one document only. The user still needs read on the DocType.
- **Whitelisted methods check permission last.** Check with
  `frappe.has_permission(..., throw=True)` *before* returning data, not
  after (Lesson 07).
- **`frappe.db.sql` for user-facing reads.** It bypasses every permission
  layer. Use `frappe.get_list` / `frappe.get_all`, which apply User
  Permissions automatically.

**403? Check in this order:** role permission on the DocType → User
Permission hiding the document → `has_permission` hook returning `None`
or False → whitelisted method missing the decorator or the check → the
API token's user lacking the role.

## Next

[10 — Workflows & Assignments](10-workflows-assignments.md) — approvals
and automatic routing. Who may move a document forward, and who it lands
with.
