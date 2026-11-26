# 20 — Upgrades

## Yeh kya hai

Ek upgrade ek live site ko ek major version se agle par le jata hai — v14 → v15 → v16. Yeh ek project hai, ek command nahi: code badalta hai, schema badalta hai, aur har custom app, Server Script, Workflow aur print format woh cheez hai jo toot sakti hai. Yeh lesson short version hai — rules, tarteeb, aur kya test karna hai. Poori tables, commands aur checklists deep reference mein hain:
[Upgrade guide — v14 → v15 → v16](../../../guides/upgrade-v14-v15-v16.md).

## Rules

1. **Ek waqt mein ek major version.** v14 → v15, verify karein, phir v15 → v16. v15 ko kabhi skip na karein — v16 patches assume karte hain ke v15 schema pehle se mojood hai.
2. **Staging pehle, hamesha.** Poora upgrade production data ki copy par chalta hai.
3. **Ek backup jo kabhi restore nahi hua, woh backup nahi hai.** Restore ko pehle staging par test karein.
4. **Har custom app ko target version ke liye ek branch chahiye** — warna use pehle remove kar dein.

## Minimal working example — upgrade, end to end

```bash
# 1. Know what you are upgrading from
grep __version__ apps/frappe/frappe/__init__.py apps/erpnext/erpnext/__init__.py
bench version

# 2. Backup — and prove it restores on staging
bench --site <site> backup --with-files --compress
bench --site staging restore <backup.sql> \
  --with-public-files <public.tar> --with-private-files <private.tar>

# 3. Runtime floor for the target (v16: Python 3.14+, Node 24+, MariaDB 10.6+)
# 4. Switch branches together, in dependency order, then migrate
cd ~/frappe-bench
bench switch-to-branch version-16 frappe erpnext hrms
bench --site <site> migrate
```

Frappe Cloud par koi bench commands nahi hain — version site dashboard mein switch hoti hai — lekin rules wahi hain.

## Breaking changes — jo sab se zyada takleef dete hain

| Change | Action |
|---|---|
| `has_permission` hooks | Explicit `True` return karna lazmi hai — `None` ab access deny karta hai (v16) |
| DB commit inside document hooks | Allowed nahi — framework commit karta hai |
| `frappe.sendmail(now=True)` | Ab commit nahi karta (v16) |
| PDF | Chrome renderer — wkhtmltopdf deprecated, v17 mein removed |
| `/app` URL | `/desk` — bookmarks aur hardcoded links theek karein |
| Legacy ERPNext CRM | v17 mein removal ke liye scheduled — abhi Frappe CRM par move karein |
| Server Scripts | v15+ par by default disabled — `bench set-config -g server_script_enabled 1` se dobara enable karein |

Poori v14→v15 aur v15→v16 tables, upgrade scan (`/frappe-upgrade-check` in frappe_core_skills), patch handling (`never_skip_patches`, `bench migrate --skip-failing`), aur mukammal checklists [upgrade guide](../../../guides/upgrade-v14-v15-v16.md) mein hain.

## Upgrade ke baad kya test karein

Staging par, haath se, umeed par nahi: Desk load hota hai aur `/desk` kaam karta hai; har DocType ke liye jise upgrade ne chhua — create, save, submit, cancel, print, ek list-view filter; app tests chalayein (`bench --site <test_site> run-tests --app <app>`); har whitelisted method, Workflow aur scheduled job dobara check karein; client ki asal invoice Chrome renderer par kholein; Email Queue draining check karein aur ek integration end to end. Sirf jab staging pass ho jaye, tab production ko date milti hai — aur rollback plan pehle se agree hota hai: agar migrate fail ho jaye aur do ghante mein fix na ho sake, to pre-upgrade backup ko purane code par restore karein.

## Kab istemal karein — aur kab nahi

| Situation | Use |
|---|---|
| Ek version support se bahar hai, ya kisi feature ko naya version chahiye | Upgrade plan karein — staging pehle |
| "Bas Friday ko bench update chala do" | Staging ke baghair production par kabhi nahi |
| Ek patch release (v16.60 → v16.61) | Staging par `bench update`, quick smoke test, phir live |
| Ek custom app jiska target ke liye koi branch nahi | Pehle use remove karein, ya port karein — uske aas-paas migrate na karein |
| Client pooche "kya hum v15 skip kar sakte hain?" | Nahi. Ek waqt mein ek major. |

## Common mistakes

- **Seedha production par upgrade karna.** Staging copy is liye mojood hai taake failure wahin ho.
- **Ek backup jo kabhi restore nahi hua.** Restore test hi backup hai.
- **Ek failed patch skip karna.** Ek skipped patch ek kamyabi nahi, ek debt entry hai — data fix karein, migrate dobara chalayein.
- **Patch ko done dikhane ke liye database ko haath se edit karna.** Agla migrate us jhoot par bharosa karta hai.
- **Apps bhool jana.** HRMS, Frappe CRM, Helpdesk aur Payments alag apps hain — har ek ko apni version branch chahiye.
- **Koi rollback plan nahi.** Agar aap staging par ek ghante se kam mein restore nahi kar sakte, to aap production ke liye tayyar nahi hain.

## Next

[21 — Ops](21-ops.md) — ek production site ko zinda rakhna: backups, monitoring, multi-site benches, aur Frappe Cloud vs self-hosted.
