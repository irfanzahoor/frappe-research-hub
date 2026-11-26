# Upgrade Guide — v14 → v15 → v16

Upgrade aik project hai, sirf command nahi. Neeche diya gaya har rule
kisi aise upgrade se aaya hai jo ghalat ho gaya tha — aam tor par is
liye ke kisi ne seedha production par chala diya tha.

## Usool

1. **Aik waqt mein aik major version.** v14 → v15, verify karein,
   phir v15 → v16. Kabhi v15 skip na karein — v16 ke patches pehle se
   maan kar chalte hain ke v15 ka schema pehle se maujood hai.
2. **Hamesha pehle staging.** Poora upgrade production data ki copy
   par chalta hai.
3. **Jo backup kabhi restore nahi kiya gaya, woh backup nahi hai.**
   Pehle staging par restore test karein.
4. **Har custom app ke liye target version ki branch chahiye** — warna
   use pehle hata diya jata hai.

## 1. Readiness check

Pehle ye tay karein ke aap kis version se upgrade kar rahe hain — andaze
se nahi, asal source se:

```bash
grep __version__ apps/frappe/frappe/__init__.py apps/erpnext/erpnext/__init__.py
bench version
```

Phir [frappe_core_skills](https://github.com/irfanzahoor/frappe_core_skills)
se upgrade scan chalaiyein (`/frappe-upgrade-check`): ye aap ki apps mein
neeche wali tables mein di gayi har removed ya changed API ko dhoondhta
hai aur files ki list deta hai. Pehle in hits ko fix karein — staging
par mile to delay hoti hai, production par outage.

Target version ke liye minimum runtime (frappe-upgrade skill se):
v15 ko Python 3.10–3.11 aur Node 18/20 chahiye; v16 ko Python **3.14+**
(purane versions SyntaxError dete hain) aur Node **24+** chahiye.
MariaDB 10.6+ dono par; v16 ke liye Ubuntu 24.04 recommended hai.

Shuru karne se pehle, kagaz par list bana lein: har custom app, Server
Script, Workflow, print format aur integration (payment gateway,
WhatsApp, email). Har aik toot sakta hai, aur har aik ka aik owner hona
chahiye.

## 2. Backup — aur sabit karein ke restore hota hai

```bash
bench --site <site> backup --with-files --compress
```

Phir us backup ko staging site par restore karein aur confirm karein ke
site khulti hai aur aik document banaya ja sakta hai. Server ka snapshot
bhi lein (VM snapshot, ya Frappe Cloud backup), aur backup files ko
upgrade ke kam az kam aik hafte baad tak sambhal kar rakhein — upgrade
wale din unhein delete karna hi woh tareeqa hai jis se aik kharab
upgrade disaster ban jata hai.

```bash
bench --site staging restore <backup.sql> --with-public-files <public.tar> --with-private-files <private.tar>
```

## 3. Upgrade order

Pehle Framework, phir ERPNext, phir alag apps, phir aap ki custom apps.
Branches dependency ki tarteeb mein aik saath switch ki jati hain:

```bash
cd ~/frappe-bench
bench switch-to-branch version-15 frappe erpnext hrms  # v14 -> v15
bench --site <site> migrate
bench switch-to-branch version-16 frappe erpnext hrms  # v15 -> v16
bench --site <site> migrate
```

`bench migrate` har app ke patches dependency ki tarteeb mein chalata
hai. HRMS, Frappe CRM, Helpdesk aur Payments alag apps hain — har aik ko
apni version-15 / version-16 branch chahiye. Jis custom app ki koi branch
nahi, use migrate fail hone ke baad nahi, pehle hata diya jata hai.

Frappe Cloud par koi bench commands nahi hain — version site dashboard
mein switch kiya jata hai — lekin usool wohi hain. Jump ke baad, monthly
patches `bench update` se aate hain (v16.61.0 aur us jaisi versions ab
monthly hain — dekhein [history](../research/history-2024-2026.md)).

## 4. Breaking changes — v14 → v15

Upgrade scan ko aksar ye hits milti hain:

| Purana / hataya gaya | Iski jagah use karein |
|---|---|
| `frappe.db.set()` | `doc.db_set()` |
| `frappe.db.update()` | `frappe.db.set_value()` |
| `frappe.db.set_value()` on Singles | `frappe.db.set_single_value()` |
| `frappe.db.set_temp` / `get_temp` | `frappe.cache` |
| JS `window.get_today` / `show_alert` / `user` / `roles` | `frappe.datetime.get_today`, `frappe.show_alert`, `frappe.session.user`, `frappe.user_roles` |
| `this` in Client Scripts | `frm` / `cur_frm` |

Is ke ilawa: **Server Scripts v15+ par by default disabled hain** —
dobara enable karne ke liye
`bench set-config -g server_script_enabled 1` chalaiyein. Event Streaming
apni alag app mein chala gaya hai, aur frontend Vue 3 hai — custom Vue 2
components ko dobara likhna hoga; staging par check karein, live par
nahi.

## 5. Breaking changes — v15 → v16

| Change | Kya karein |
|---|---|
| `has_permission` hooks | Explicit `True` return karna lazmi hai — `None` return karne par ab access deny ho jata hai |
| DB commit inside document hooks | Allowed nahi hai — framework khud commit karta hai |
| Default list sort | `creation` (pehle `modified` tha) — jahan order matter karta ho, wahan `order_by` explicitly pass karein |
| `frappe.get_doc(dt, name, field=val)` | Ab values set nahi karta |
| `frappe.sendmail(now=True)` | Ab commit nahi karta |
| State-changing API methods | Sirf POST (`logout`, `upload_file`, `send_login_link`) |
| PDF | Chrome renderer — **wkhtmltopdf deprecated hai**, v17 mein remove ho jayega |
| Classic print formats | Deprecated hain — v17 mein kaam karna band kar dein ge, abhi naye print designer par dobara banayein |
| `/app` URL | `/desk` — bookmarks aur hardcoded links fix karein |
| Blog, Newsletter, Energy Points, Offsite backups | Alag apps (offsite backups: `frappe/offsite_backups`) |

Do app moves hain jin ki planning karni hai, upgrade ke waqt discover
nahi karna: **legacy ERPNext CRM v17 mein remove hone wala hai** — client
ko Frappe CRM app par abhi, v16 upgrade ke dauraan, shift karein. Aur
**standard workspace customisations upgrade par reset ho jati hain** —
unhein apni app mein fixtures ke tor par rakhein, kabhi Desk edits ke
tor par nahi.

## 6. Patches — aur aik failed patch

Schema aur data ki tabdeeliyan `patches/` mein hoti hain, aur
`patches.txt` mein un ki entry hoti hai — har change ke liye aik patch,
jahan mumkin ho idempotent. Jo patches kabhi skip nahi karne, woh
`hooks.py` mein
`never_skip_patches = ["my_app.patches.v16_0.critical_data_fix"]` ke tor
par list hote hain.

Agar koi patch fail ho jaye, to migration ruk jati hai. Traceback
parhein — woh patch aur row ka naam batata hai. Staging par **data** fix
karein (aik ghalat value, aik duplicate, aik missing master), patch ko
nahi. Database ko haath se edit kar ke patch ko done dikhana kabhi na
karein — agli migrate us jhoot par bharosa karegi. Dobara
`bench --site <site> migrate` chalaiyein; ye failed patch se dobara
shuru hoti hai. `bench migrate --skip-failing` sirf non-critical
failures ke liye hai — aik skipped patch debt ki entry hai, kamyabi
nahi.

Aik spice-factory client ke paas aik dafa duplicate batch number par
patch fail hua tha. Fix ye tha ke staging par duplicates ko merge kiya
gaya, phir migrate dobara chalayi gayi — das minute. Patch skip karne se
production stock mein aik number wale do batches reh jate.

## 7. Test the upgrade on the staging copy

Production backup ko staging par restore karein, wahan poora upgrade
chalaiyein, phir test karein — haath se, umeed par nahi: Desk load hota
hai aur `/desk` kaam karta hai; har us DocType ke liye jise upgrade ne
chhua ho, create, save, submit, cancel, print, aur aik list-view filter
karein; app tests
`bench --site <test_site> run-tests --app <app>` se chalaiyein; har
whitelisted method, workflow aur scheduled job dobara check karein;
client ka asal invoice Chrome renderer par kholein. Sirf jab staging
pass ho, tab production ki date di jati hai.

**Rollback plan:** agar migrate beech mein fail ho jaye, to **pre-upgrade
backup ko purane code par restore karein** (git checkout se purani
branches, DB + files restore karein). Agar aap ye staging par aik ghante
se kam mein nahi kar sakte, to aap production upgrade ke liye tayyar
nahi hain. Pehle se client se agree kar lein: "agar migrate fail ho
jaye aur do ghante mein fix na ho sake, to hum restore karte hain."

## 8. Checklists

**Upgrade se pehle:**

- [ ] Maujooda versions record ki gayi hain; upgrade scan chalaya gaya, hits fix ki gayi hain
- [ ] Runtime target version ke mutabiq hai (Python, Node, MariaDB, OS)
- [ ] Backup `--with-files --compress` ke saath liya gaya, restore test kiya gaya
- [ ] Har app ke paas target version ki branch hai (ya use hata diya gaya hai)
- [ ] Server Scripts, workflows, print formats, integrations list ki gayi hain, har aik ka aik owner hai
- [ ] Poora upgrade production data ki staging copy par rehearsal kiya gaya
- [ ] Staging tests pass hain (create/save/submit/cancel/print, run-tests)
- [ ] Rollback plan client se agree kiya gaya, restore rehearsal kiya gaya

**Upgrade ke baad:**

- [ ] Desk load hota hai, `/desk` URL, workspaces theek hain
- [ ] Reports khulti hain (General Ledger, Stock Balance, Trial Balance)
- [ ] Print formats Chrome PDF par render hote hain — asal invoice check kiya gaya
- [ ] Scheduled jobs chal rahe hain (Scheduler, Background Jobs)
- [ ] Email Queue drain ho rahi hai, email sending kaam karti hai
- [ ] Integrations end-to-end test ki gayi hain (payment gateway, WhatsApp, webhooks)
- [ ] Permissions: `has_permission` hooks `True` return karte hain, roles asal users se test kiye gaye, Administrator se nahi
- [ ] Dashboards: upgraded sites classic dashboards tab tak rakhte hain jab tak change na kiye jayein — Insights par sirf har aik ko check karne ke baad switch karein
- [ ] Offsite backups app installed hai (v16 — ab built in nahi hai)
- [ ] Upgrade ke baad backup liya gaya

## Sources

Deep reference: [frappe-upgrade skill](https://github.com/irfanzahoor/frappe_core_skills/tree/develop/skills/frappe-upgrade)
(breaking-change tables, runtime, checklist) and the v16 release notes
([history](../research/history-2024-2026.md)). Lessons: [05 — Server Scripts](../learn/framework/level-2/05-server-scripts-events.md), [09 — Permissions & Roles](../learn/framework/level-2/09-permissions-roles.md), [13 — Testing](../learn/framework/level-3/13-testing.md).
