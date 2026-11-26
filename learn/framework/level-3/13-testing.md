# 13 — Testing

## What it is

A test proves a rule works — and keeps proving it every time someone
changes the code later. Frappe tests are Python `unittest` tests that run
against a real site and a real database. Each test runs inside a
transaction that **rolls back afterwards**, so tests never leave data
behind.

Test files live next to the DocType they test, and the file **must start
with `test_`** or the runner ignores it:

```
my_app/my_module/doctype/gate_pass/
    gate_pass.py
    test_gate_pass.py        # <-- tests live here
    test_records.json        # <-- optional test data
```

| Version | Needs DB? | Base class |
|---|---|---|
| v15+ | no (pure logic) | `from frappe.tests.classes import UnitTestCase` |
| v15+ | yes | `from frappe.tests.classes import IntegrationTestCase` |
| v14 | any | `from frappe.tests.utils import FrappeTestCase` |

## Minimal working example — testing the Gate Pass rule

Lesson 05 put a rule in the Gate Pass controller: a Delivery/Pickup pass
needs at least one item, and every row needs `qty > 0`. Test it:

```python
# my_app/my_module/doctype/gate_pass/test_gate_pass.py
import frappe
from frappe.tests.classes import IntegrationTestCase


class TestGatePass(IntegrationTestCase):
    def test_delivery_pass_needs_items(self):
        doc = frappe.get_doc({
            "doctype": "Gate Pass",
            "purpose": "Delivery",
            "visitor_name": "Test Visitor",
            "items": [],
        })
        self.assertRaises(frappe.ValidationError, doc.insert)

    def test_zero_qty_is_rejected(self):
        doc = frappe.get_doc({
            "doctype": "Gate Pass",
            "purpose": "Delivery",
            "visitor_name": "Test Visitor",
            "items": [{"item_name": "Red Chilli Powder", "qty": 0}],
        })
        self.assertRaises(frappe.ValidationError, doc.insert)

    def test_valid_pass_saves_and_submits(self):
        doc = frappe.get_doc({
            "doctype": "Gate Pass",
            "purpose": "Delivery",
            "visitor_name": "Test Visitor",
            "items": [{"item_name": "Red Chilli Powder", "qty": 5}],
        })
        doc.insert()
        doc.submit()
        self.assertEqual(doc.docstatus, 1)
```

Test **behaviour**, not internals: validations throw, totals compute,
submit/cancel work, permissions deny. A test that checks a private
helper's return value breaks the moment someone refactors; a test that
checks "a bad pass cannot be saved" survives.

## Test data and permissions

Create the data inside the test (as above), or put it in
`test_records.json` next to the DocType — the runner loads it before the
tests run. Never depend on production data: a test that passes on your
machine and fails on the client's is worse than no test.

Check permissions the same way a user would hit them:

```python
def test_warehouse_user_cannot_submit(self):
    frappe.set_user("warehouse.user@example.com")
    doc = frappe.get_doc("Gate Pass", "GP-0001")
    self.assertRaises(frappe.PermissionError, doc.submit)
    frappe.set_user("Administrator")   # always restore
```

Mock external HTTP calls with `unittest.mock.patch`. A test that calls a
real supplier API is slow, flaky, and charges real money.

## Running tests

```bash
bench --site test.local set-config allow_tests true   # once, on the test site
bench --site test.local run-tests --app my_app
bench --site test.local run-tests --doctype "Gate Pass"
bench --site test.local run-tests --doctype "Gate Pass" --test test_zero_qty_is_rejected
bench --site test.local run-tests --app my_app --failfast
```

Use a **separate test site**, never production. The `bench new-app`
scaffold generates a GitHub Actions workflow (`.github/workflows/ci.yml`)
that creates a test site, installs the app, and runs the tests on every
push — wire it up once and the tests run themselves.

## UI tests

Python tests prove the server logic. UI tests prove the form works the
way a user uses it — a button appears, a field becomes mandatory, a list
loads. Frappe uses **Cypress**: write `.js` specs in `cypress/integration`
and run them against a running test site:

```bash
bench --site test.local run-ui-tests my_app            # opens the Cypress runner
bench --site test.local run-ui-tests my_app --headless  # CI mode
```

UI tests are slow and need a browser. Keep them for the handful of flows
that must never break (login, create Sales Order, submit Quality
Inspection) — everything else belongs in a Python test.

## When to use — and when not to

| Situation | Use |
|---|---|
| A validation, a total, a status change | Python test, `IntegrationTestCase` |
| Pure logic with no database | `UnitTestCase` (v15+) — fast |
| "Can this role do this?" | Python test with `frappe.set_user` |
| A critical user flow end to end | Cypress UI test |
| A rule you just fixed a bug in | A test that fails without the fix — first |
| "Does the button look right?" | Look at it. Not everything needs a test |

## Common mistakes

- **`frappe.db.commit()` inside a test.** Each test rolls back. A
  commit breaks isolation and leaks data into the next test.
- **Depending on production data.** The test passes on your laptop,
  fails on CI and on the client. Create data in the test.
- **Running tests on the production site.** Tests insert, submit, and
  cancel documents. Use a disposable test site.
- **A test file not starting with `test_`.** The runner silently skips
  it — zero tests run, zero failures, false confidence.
- **Calling real external APIs in tests.** Mock them. A supplier API
  being down must not fail your test suite.
- **Forgetting to restore the user.** `frappe.set_user(...)` without
  restoring to Administrator leaks the wrong user into later tests.
- **Only testing the happy path.** The bug is always in the case you
  did not test: zero qty, missing customer, cancelled document.

## Next

[14 — Performance](14-performance.md) — the report that takes 30 seconds
and the submit that times out: N+1 queries, indexes, and caching.
