# 02 — Bench, Sites aur Apps

## Yeh kya hai

**bench** woh command-line tool hai jo sab kuch banata aur manage karta hai:
bench folder, us ke andar ki apps, aur un par chalne wali sites.

- Aik **bench** aik folder hai. Is mein `apps/`, `sites/`, `config/` aur
  `env/` hote hain.
- Aik **site** aik database plus us ki files hai. Aik bench mein kai sites
  ho sakti hain.
- Aik **app** DocTypes, Python/JS code aur fixtures ka aik package hai. Apps
  `apps/` mein rehti hain aur kuch karne se pehle site par *install* hoti
  hain.

## Prerequisites (v16)

| Item | Version |
|---|---|
| Python | 3.14 |
| Node.js | 24+ (plus Yarn 1.22+) |
| MariaDB | 11.8 documented (10.6 works in practice) |
| Redis | required — caching, queues, realtime |

bench khud `uv` se install karein (yeh current official tareeqa hai):

```bash
uv tool install frappe-bench
bench --version
```

## Chhoti si working misaal — zero se chalti hui site tak

```bash
# 1. Create a bench on the v16 branch
bench init --frappe-branch version-16 frappe-bench
cd frappe-bench

# 2. Download ERPNext (same major version as Frappe — never mix v15 and v16)
bench get-app --branch version-16 erpnext

# 3. Create a site and install ERPNext on it in one step
bench new-site mysite.local --install-app erpnext
#    (prompts for the MariaDB root password, then the Administrator password)

# 4. Create your own app
bench new-app my_app
#    (prompts for title, description, publisher, email, licence)

# 5. Install your app on the site
bench --site mysite.local install-app my_app

# 6. Start everything
bench start
#    Open http://mysite.local:8000 — sign in as Administrator
```

Har command ne kya kiya:

| Command | What it does |
|---|---|
| `bench init` | Bench folder banata hai, us mein Frappe install karta hai |
| `bench get-app` | App ko `apps/` mein download karta hai — abhi kahin install nahi karta |
| `bench new-site` | Naya database + site folder banata hai; `--install-app` app ko foran install kar deta hai |
| `bench new-app` | `apps/` mein nayi custom app ka scaffold banata hai |
| `bench --site X install-app` | App ko aik site par activate karta hai (us ki tables banata hai) |
| `bench start` | Development ke liye web server, workers aur scheduler chalata hai |

Roz ke kaam ke useful commands:

```bash
bench use mysite.local                 # make this the default site (skip --site)
bench list-apps                        # apps on the bench
bench --site mysite.local list-apps    # apps installed on one site
bench --site mysite.local migrate      # apply DocType / patch / fixture changes
bench --site mysite.local backup --with-files --compress
bench --site mysite.local console      # Python shell inside the site
bench --site mysite.local clear-cache  # after hooks.py changes
bench --site mysite.local enable-scheduler
```

## Kis command ko kab use karein

- **Naya project** → `bench init`, phir `bench new-app`, phir aik site.
- **Mojooda bench par nayi client site** → sirf `bench new-site`.
- **Site par ERPNext / HRMS / CRM add karna** → `bench get-app` (har bench
  par aik dafa), phir `bench --site … install-app` (har site par aik dafa).
- **Aap ne DocType, patch ya fixture change kiya** → `bench migrate`.
- **Aap ne public JS/CSS change kiya** → `bench build --app my_app`.
- **Aap ne hooks.py change kiya** → `bench clear-cache`.

## Aam ghaltiyan

- **bench ko root ke tor par chalana.** Aik dedicated `frappe` user use
  karein. Kabhi `sudo bench` na karein.
- **Major versions ko mila dena.** Frappe v16 + ERPNext v15 (ya ulta)
  toot jata hai. Dono ko `--branch version-16` se pin karein.
- **`migrate` bhool jana.** DocType JSON, patches aur fixtures sirf
  `bench --site … migrate` par apply hote hain. Agar aap ka naya field
  missing hai, to pehle migrate karein.
- **App folder ko haath se delete karna.** `bench remove-app` use karein —
  yeh database tables bhi remove karta hai. Haath se delete kiya hua folder
  aik tooti hui site chhor deta hai.
- **Update / migrate / restore se pehle backup na lena.** Pehle backup lein,
  aur kam se kam aik dafa staging site par restore test karein — aik backup
  jise aap ne kabhi restore nahi kiya, woh backup nahi hai.
- **Aik bench, aik site, hamesha ke liye.** Benches saste hain. Dev, staging
  aur production ko alag benches (ya alag servers) par rakhein, kabhi aik
  site par nahi.
- **Production ko `bench start` par chalana.** Yeh development server hai.
  Production mein nginx + supervisor (`bench setup production`) ya Docker
  use hota hai.

## Khud ko check karein

Upar wali misaal ke baad aap ko yeh jawab dena aana chahiye: bench par kaun
si apps hain, `mysite.local` par kaun si install hain, aur `bench start` ne
kya print kiya. Agar site nahi khulti, to pehle terminal output check karein
— ghalti aksar ghalat MariaDB password ya pehle se use ho raha port hoti hai.

## Next

[03 — Apna pehla DocType](03-first-doctype.md) — fields, types aur saaf
layout ke saath aik record type define karein.
