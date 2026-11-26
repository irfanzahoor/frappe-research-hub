# 15 — Security

## Yeh kya hai

Maan lein ke har input hostile hai: form fields, URL parameters, file
uploads, webhook payloads, imported rows. Framework aapko safe APIs deta
hai — unhe use karein, un ke gird rasta na dhoondhein. Frappe apps mein
ziyada tar security bugs koi exotic attack nahi hote; woh developer hota
hai jo `ignore_permissions=True` "kaam chalane ke liye" pass karta hai aur
usay wahin chhod deta hai.

## Minimal working example — search endpoint, ghalat aur sahi

Customer portal ko naam se items search karne hain. Pehla version kaam
karta hai — aur kisi ko bhi koi bhi table padhne deta hai:

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

Ek mein teen fixes: query parameterised hai (`frappe.get_list` SQL
aapke liye banata hai), method data return karne se **pehle** caller ki
permission check karta hai, aur result limited hai. Whitelisting aapke
liye permissions check **nahi** karta — har `@frappe.whitelist()` method
ko khud yeh karna hota hai.

SQL injection, saaf lafzon mein — kabhi user input se SQL na banayein:

| Ghalat | Sahi |
|---|---|
| `frappe.db.sql(f"... where name='{user}'")` | `frappe.db.sql("... where name=%s", user)` |
| `"... where name='" + name + "'"` | `frappe.qb.from_("User").select("*").where(Field("name") == name)` |

Placeholders sirf values ke liye kaam karte hain. Input se aane wala
table ya column naam placeholder nahi ho sakta — pehle usay fixed
allowlist ke khilaf validate karein.

## XSS — Jinja autoescape nahi karta

Frappe Jinja ko sandbox mein render karta hai, lekin HTML ko escape
**nahi** karta. Print format, email, ya web template mein
`{{ doc.remarks }}` raw HTML render karta hai — us `<script>` samet jo
user ne remarks field mein type kiya ho.

| Ghalat | Sahi |
|---|---|
| Print format mein `{{ doc.remarks }}` | `{{ doc.remarks \| e }}` |
| User content par `{{ html \| safe }}` | `\|safe` sirf us HTML par jo aapke apne code ne banaya ho |
| JS mein `$(el).html(frm.doc.notes)` | `$(el).text(frm.doc.notes)` |

## Permissions — woh rules jo toote hain

- **`ignore_permissions=True` sirf comment ke saath** jo bataye ke
  kyun — misaal ke taur par, aise method mein system-generated document
  jis ne pehle se business rule check kar liya ho. Comment ke baghair,
  agla developer usay har jagah copy karta hai.
- **`allow_guest=True` sirf waqai public endpoints ke liye** (signup,
  public page data). Guest method ko kabhi private data return nahi karna
  chahiye aur na hi apni validation ke baghair writes accept karni
  chahiye. Guest endpoints ko `@frappe.rate_limit` se rate-limit karein.
- **`frappe.get_list` permission-aware hai; `frappe.get_all` nahi hai.**
  User-facing reads `get_list` use karte hain (Lesson 14).
- **Identity ke liye request parameters par bharosa na karein.**
  `frappe.form_dict` se aane wale `user` value ke bajaye
  `frappe.session.user` use karein.
- **Field ko JS mein chhupana security nahi hai.** Koi bhi usay API ke
  zariye padh sakta hai. Permlevel use karein (field-level permission,
  Lesson 09).

## Secrets aur API keys

| Ghalat | Sahi |
|---|---|
| Code, fixtures, ya committed JSON mein API key | `bench set-config <key> <value>` — site_config.json git mein nahi hoti |
| Data field mein password | `Password` fieldtype — rest par encrypted; `frappe.utils.password.get_decrypted_password` se padhein |
| Client Script / JS mein token | Usay server-side rakhein; sirf whitelisted method se expose karein jo permission check kare |

Site config ko `frappe.get_site_config()` / `frappe.conf` se padhein.
Kabhi secrets ko log na karein, kabhi unhe error messages ya test data
mein na daalein. Leaked secret ko **foran rotate** karna hota hai —
file delete karne se woh git history se nahi nikalta.

API access: minimal roles ke saath **dedicated API user** banayein, kabhi
Administrator keys use na karein. Calls is se authenticate hoti hain:
`Authorization: token <api_key>:<api_secret>`. Jab koi chhod kar jaye to
keys rotate karein; aisi key jo kabhi expire nahi hoti, woh kabhi kaam
karna band nahi karti.

## Files aur audit

Documents se attached uploads `is_private` wale `File` docs hote hain.
Private files download karne ke liye logged-in user ko attached document
par permission chahiye hoti hai. User files ko `public/` se serve na
karein, private file ka `file_url` guest page par link na karein, aur
uploads ko save karne se pehle server-side validate karein.

Audit ke liye: sensitive DocTypes par **Track Changes** on karein — har
change ek Version ke taur par save rehti hai jisay aap review kar sakte
hain. **Activity Log** dikhata hai ke kis ne kab kya kiya. Jab kuch
ghalat ho, to pehla sawal hamesha yeh hota hai ke "kis ne yeh badla, aur
kab?" — logs ko is ka jawab dena chahiye.

## Kab use karein — aur kab nahi

| Situation | Use karein |
|---|---|
| Query mein user input | Placeholders / `frappe.qb` / `get_list` filters |
| Template mein user text | `\| e` escape; user content par kabhi `\|safe` nahi |
| Aisa system action jo user nahi kar sakta | Check ke baad comment ke saath `ignore_permissions=True` |
| Public page ya form | `allow_guest`, har input validate karein, koi internal data na dikhayein |
| Secret, key, ya token | site_config ya Password field — kabhi code ya JS nahi |
| External system jo andar call kar raha hai | Dedicated API user, minimal roles, keys rotate karein |

## Aam ghaltiyan

- **F-string SQL.** Frappe app mein sab se khatarnak line. User input
  ke saath ek `f"..."` aur poora database readable ho jata hai.
- **Bina comment ke `ignore_permissions=True`.** Yeh phailta hai. Agla
  developer usay copy karta hai kyunke "pichli baar kaam kar gaya tha".
- **Aise method par `allow_guest=True` jo likhta hai.** Guest endpoints
  public hote hain. Internet par koi bhi unhe call kar sakta hai.
- **Integration mein Administrator API keys.** Ek leaked key ka matlab
  poora control hai. Dedicated user, minimal roles, rotated keys.
- **Git mein secrets.** Ek baar commit hone wali key history mein
  hamesha rehti hai. Pehle usay rotate karein, phir remove karein — is
  order mein.
- **Guest page se linked private files.** `is_private` ka koi matlab
  nahi agar aap URL baant dein.
- **Security ke taur par "hidden" fields.** JS mein chhupana aur hidden
  fields UX hain. API wohi return karta hai jo DocType allow karta hai —
  permlevel use karein.

## Agla

[16 — Debugging](16-debugging.md) — jab phir bhi toot jaye: traceback
padhna, logs, `bench console`, aur woh errors jin se har Frappe
developer milta hai.
