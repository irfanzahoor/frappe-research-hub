# 06 — Client Scripts

## Yeh kya hai

**Client Script** JavaScript hai jo user ke browser mein, form par chalti hai.
Yeh behaviour aur experience control karti hai: field show ya hide karna, field
mandatory banana, Link ko filter karna, button add karna, value fetch karke
dikhana. Yeh **sirf UX** hai — yeh security nahi hai aur validation bhi nahi.
Browser jo kuch kar sakta hai, API usay skip kar sakti hai.

Apni app ke DocType ke liye, script DocType ke saath rehti hai:

```text
my_app/doctype/gate_pass/gate_pass.js   # form behaviour for Gate Pass
```

Doosri app ke DocType (Sales Order, Delivery Note) ke liye, Desk mein
**Client Script** DocType use karein, ya hooks.py mein `doctype_js` use karein
jo `public/js/` ki file ki taraf ishara kare. Ek DocType ke liye wohi
`frappe.ui.form.on` block kabhi duplicate na karein — maujooda handler ko
extend karein.

## Chhoti si working example — Gate Pass form

```js
// gate_pass.js
frappe.ui.form.on("Gate Pass", {
    setup(frm) {
        // set_query belongs here — it runs once per form load
        frm.set_query("company", () => ({ filters: { disabled: 0 } }));
    },

    refresh(frm) {
        // Items are mandatory for Delivery / Pickup, optional for Visit
        frm.toggle_reqd("items", ["Delivery", "Pickup"].includes(frm.doc.purpose));
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__("Mark Returned"), () => {
                frappe.call({
                    method: "my_app.gate_pass.api.mark_returned",
                    args: { name: frm.doc.name },
                    callback() { frm.reload_doc(); },
                });
            }, __("Actions"));
        }
    },

    purpose(frm) {
        // Runs whenever the Purpose field changes
        frm.toggle_reqd("items", ["Delivery", "Pickup"].includes(frm.doc.purpose));
        frm.refresh_field("items");
    },

    validate(frm) {
        // A UX hint only — the server re-checks this in validate() (Lesson 05)
        if (["Delivery", "Pickup"].includes(frm.doc.purpose) && !frm.doc.items.length) {
            frappe.msgprint(__("Add at least one item for a Delivery or Pickup pass"));
        }
    },
});
```

Button ko jo server side chahiye (poora pattern Lesson 07 mein hai):

```python
# my_app/gate_pass/api.py
import frappe


@frappe.whitelist()
def mark_returned(name):
    doc = frappe.get_doc("Gate Pass", name)
    doc.check_permission("write")
    doc.db_set("status", "Returned")
```

> Is ke kaam karne ke liye Gate Pass ko `status` field chahiye — Lesson 03
> wale DocType mein ek Select add karein (`Open` / `Returned`, default `Open`).

## Form events jo aap sab se zyada use karein ge

| Event | Kab chalta hai |
|---|---|
| `setup(frm)` | Har form load par ek dafa — `set_query` yahin jata hai |
| `onload(frm)` | Form load hone par (setup ke baad) |
| `refresh(frm)` | Form har dafa re-render ho to — buttons aur visibility yahin jati hai |
| `fieldname(frm)` | Jab ek field badle (masalan `purpose(frm)`) |
| `validate(frm)` | Save se pehle — sirf UX hint, asal check kabhi nahi |
| `after_save(frm)` | Kaamyab save ke baad |

Child table rows ka apna block hota hai, **parent ki** file mein:

```js
frappe.ui.form.on("Gate Pass Item", {
    qty(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        if (row.qty <= 0) {
            frappe.msgprint(__("Row {0}: Qty must be greater than 0", [row.idx]));
        }
    },
    items_remove(frm) {
        frappe.show_alert({ message: __("Item removed"), indicator: "orange" }, 3);
    },
});
```

## Kab use karein — aur kab nahi

| Situation | Use karein |
|---|---|
| Field show/hide karna, mandatory banana | Client Script (`toggle_display`, `toggle_reqd`) |
| Link field ke options filter karna | `setup` mein `frm.set_query` |
| Linked document se field copy karna | DocType mein field par **Fetch From** — JS nahi |
| Static visibility / mandatory rules | DocType mein **Depends On / Mandatory Depends On** — JS nahi |
| Button jo server ka kaam kare | `frm.add_custom_button` + whitelisted method par `frappe.call` |
| Rule jo lazmi qaim rehna chahiye | Server `validate()` (Lesson 05) — JS sirf is ki taraf ishara kar sakti hai |
| Data parhna jo kabhi kabhi badalta hai | `onload` mein ek dafa load karein — `refresh` se server call na karein |

## Aam ghaltiyan

- **Validation sirf JS mein.** API form ko poori tarah bypass kar deti hai.
  Har rule jo matter karta hai, controller mein rehta hai.
- **`refresh` ya field event mein `set_query`.** Yeh har render par chalta
  hai. Isay `setup` mein rakhein.
- **Field ko JS mein hide karke "secure" karna.** Koi bhi field ko API ke
  zariye parh sakta hai. Permlevel use karein — Lesson 09.
- **`cur_frm`.** Event jo `frm` argument deta hai, wohi use karein.
- **Ek file mein ek hi DocType ke liye do `frappe.ui.form.on` blocks.**
  Ek handler ko extend karein.
- **Direct DOM manipulation** (form fields par `$(...)`) jab `frm.*`
  API maujood ho (`set_value`, `set_df_property`, `toggle_display`).
- **Synchronous server calls** (`async: false`). Promises (`.then`)
  ya `async/await` use karein.
- **Khule hue form ke liye API se save karna.** `frm.set_value` use
  karein, phir `frm.save()` — khule hue form par kabhi
  `frappe.client.set_value` na use karein.

## Agla

[07 — APIs](07-apis.md) — `frappe.call`, whitelisted methods, aur REST
API. Browser, doosre systems, aur aap ka apna code server se kaise baat
karte hain.
