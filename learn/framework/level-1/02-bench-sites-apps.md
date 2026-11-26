# 02 — Bench, Sites & Apps

## What it is

**bench** is the command-line tool that creates and manages everything: the
bench folder, the apps inside it, and the sites that run on it.

- A **bench** is a folder. It holds `apps/`, `sites/`, `config/` and `env/`.
- A **site** is one database plus its files. One bench can hold many sites.
- An **app** is a package of DocTypes, Python/JS code and fixtures. Apps live
  in `apps/` and are *installed* on a site before they do anything.

## Prerequisites (v16)

| Item | Version |
|---|---|
| Python | 3.14 |
| Node.js | 24+ (plus Yarn 1.22+) |
| MariaDB | 11.8 documented (10.6 works in practice) |
| Redis | required — caching, queues, realtime |

Install bench itself with `uv` (the current official method):

```bash
uv tool install frappe-bench
bench --version
```

## Minimal working example — from zero to a running site

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

What each command did:

| Command | What it does |
|---|---|
| `bench init` | Creates the bench folder, installs Frappe into it |
| `bench get-app` | Downloads an app into `apps/` — does **not** install it anywhere yet |
| `bench new-site` | Creates a new database + site folder; `--install-app` installs the app right away |
| `bench new-app` | Scaffolds a new custom app in `apps/` |
| `bench --site X install-app` | Activates an app on one site (creates its tables) |
| `bench start` | Runs the web server, workers and scheduler for development |

Useful everyday commands:

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

## When to use which command

- **New project** → `bench init`, then `bench new-app`, then a site.
- **New client site on an existing bench** → `bench new-site` only.
- **Add ERPNext / HRMS / CRM to a site** → `bench get-app` (once per bench),
  then `bench --site … install-app` (once per site).
- **You changed a DocType, a patch or a fixture** → `bench migrate`.
- **You changed public JS/CSS** → `bench build --app my_app`.
- **You changed hooks.py** → `bench clear-cache`.

## Common mistakes

- **Running bench as root.** Use a dedicated `frappe` user. Never `sudo bench`.
- **Mixing major versions.** Frappe v16 + ERPNext v15 (or the reverse) breaks.
  Pin both with `--branch version-16`.
- **Forgetting `migrate`.** DocType JSON, patches and fixtures only apply on
  `bench --site … migrate`. If your new field is missing, migrate first.
- **Deleting an app folder by hand.** Use `bench remove-app` — it also removes
  the database tables. A hand-deleted folder leaves a broken site.
- **No backup before update / migrate / restore.** Back up first, and test a
  restore on a staging site at least once — a backup you never restored is
  not a backup.
- **One bench, one site, forever.** Benches are cheap. Keep dev, staging and
  production on separate benches (or separate servers), never on one site.
- **Running production on `bench start`.** That is the development server.
  Production uses nginx + supervisor (`bench setup production`) or Docker.

## Check yourself

After the example above you should be able to answer: which apps are on the
bench, which are installed on `mysite.local`, and what `bench start` printed.
If the site does not open, check the terminal output first — the error is
usually a wrong MariaDB password or a port already in use.

## Next

[03 — Your first DocType](03-first-doctype.md) — define a record type with
fields, types and a clean layout.
