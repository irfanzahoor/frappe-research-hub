# 13 — Testing

## Yeh kya hai

Ek test prove karta hai ke koi rule kaam karta hai — aur har baar prove
karta rehta hai jab koi baad mein code badalta hai. Frappe tests Python
`unittest` tests hain jo ek real site aur real database ke khilaf chalte
hain. Har test ek transaction ke andar chalta hai jo **baad mein rollback
ho jata hai**, is liye tests kabhi data peeche nahi chhodte.

Test files us DocType ke paas hoti hain jisay woh test karte hain, aur
file ka naam **lazmi `test_` se shuru** hona chahiye warna runner usay
ignore kar deta hai:

```
my_app/my_module/doctype/gate_pass/
    gate_pass.py
    test_gate_pass.py        # <-- tests live here
    test_records.json        # <-- optional test data
```

| Version | DB chahiye? | Base class |
|---|---|---|
| v15+ | nahi (pure logic) | `from frappe.tests.classes import UnitTestCase` |
| v15+ | haan | `from frappe.tests.classes import IntegrationTestCase` |
| v14 | koi bhi | `from frappe.tests.utils import FrappeTestCase` |

## Minimal working example — Gate Pass rule ko test karna

Lesson 05 ne Gate Pass controller mein ek rule daala tha: Delivery/Pickup
pass mein kam se kam ek item hona chahiye, aur har row mein `qty > 0`
hona chahiye. Usay test karein:

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

**Behaviour** ko test karein, internals ko nahi: validations throw
karti hain, totals compute hote hain, submit/cancel kaam karte hain,
permissions mana karte hain. Aisa test jo kisi private helper ki return
value check karta hai, usi lamhe toot jata hai jab koi refactor kare; aisa
test jo check karta hai ke "ghalat pass save nahi ho sakta" bach jata hai.

## Test data aur permissions

Data test ke andar hi banayein (jaisa upar hai), ya usay DocType ke paas
`test_records.json` mein daalein — runner tests chalne se pehle usay load
kar leta hai. Kabhi production data par depend na karein: aisa test jo
aapki machine par pass ho aur client ki machine par fail ho, woh bina
test ke hone se bhi bura hai.

Permissions ko usi tarah check karein jaise user un se takrayega:

```python
def test_warehouse_user_cannot_submit(self):
    frappe.set_user("warehouse.user@example.com")
    doc = frappe.get_doc("Gate Pass", "GP-0001")
    self.assertRaises(frappe.PermissionError, doc.submit)
    frappe.set_user("Administrator")   # always restore
```

External HTTP calls ko `unittest.mock.patch` se mock karein. Aisa test jo
real supplier API ko call karta hai, slow hota hai, flaky hota hai, aur
real paise kharch karta hai.

## Tests chalana

```bash
bench --site test.local set-config allow_tests true   # once, on the test site
bench --site test.local run-tests --app my_app
bench --site test.local run-tests --doctype "Gate Pass"
bench --site test.local run-tests --doctype "Gate Pass" --test test_zero_qty_is_rejected
bench --site test.local run-tests --app my_app --failfast
```

**Alag test site** use karein, kabhi production nahi. `bench new-app`
scaffold ek GitHub Actions workflow (`.github/workflows/ci.yml`)
banata hai jo test site banata hai, app install karta hai, aur har push
par tests chalata hai — ek baar wire up karein aur tests khud chalne
lagte hain.

## UI tests

Python tests server logic ko prove karte hain. UI tests prove karte hain
ke form us tarah kaam karta hai jaise user usay use karta hai — button
nazar aata hai, field mandatory ho jata hai, list load hoti hai. Frappe
**Cypress** use karta hai: `cypress/integration` mein `.js` specs
likhein aur unhe running test site ke khilaf chalyein:

```bash
bench --site test.local run-ui-tests my_app            # opens the Cypress runner
bench --site test.local run-ui-tests my_app --headless  # CI mode
```

UI tests slow hote hain aur unhe browser chahiye hota hai. Unhe sirf un
chand flows ke liye rakhein jo kabhi nahi tootne chahiye (login, Sales
Order banana, Quality Inspection submit karna) — baaki sab Python test
mein hona chahiye.

## Kab use karein — aur kab nahi

| Situation | Use karein |
|---|---|
| Validation, total, status change | Python test, `IntegrationTestCase` |
| Bina database ke pure logic | `UnitTestCase` (v15+) — fast |
| "Kya yeh role yeh kar sakta hai?" | `frappe.set_user` ke saath Python test |
| Critical user flow end to end | Cypress UI test |
| Rule jis mein aap ne abhi bug fix kiya hai | Aisa test jo fix ke baghair fail ho — pehle |
| "Kya button theek lag raha hai?" | Usay dekhein. Har cheez ko test ki zaroorat nahi |

## Aam ghaltiyan

- **Test ke andar `frappe.db.commit()`.** Har test rollback hota hai. Ek
  commit isolation tod deta hai aur data ko agle test mein leak kar deta
  hai.
- **Production data par depend karna.** Test aapke laptop par pass hota
  hai, CI aur client par fail hota hai. Data test mein banayein.
- **Production site par tests chalana.** Tests documents insert, submit,
  aur cancel karte hain. Disposable test site use karein.
- **Test file ka naam `test_` se shuru na hona.** Runner usay khamoshi
  se skip kar deta hai — zero tests chalte hain, zero failures, ghalat
  confidence.
- **Tests mein real external APIs call karna.** Unhe mock karein. Supplier
  API ka down hona aapki test suite ko fail nahi karna chahiye.
- **User ko restore karna bhool jana.** `frappe.set_user(...)` bina
  Administrator par restore kiye ghalat user ko baad wale tests mein leak
  kar deta hai.
- **Sirf happy path test karna.** Bug hamesha us case mein hota hai jo
  aap ne test nahi kiya: zero qty, missing customer, cancelled document.

## Agla

[14 — Performance](14-performance.md) — woh report jo 30 seconds leti
hai aur woh submit jo timeout ho jata hai: N+1 queries, indexes, aur
caching.
