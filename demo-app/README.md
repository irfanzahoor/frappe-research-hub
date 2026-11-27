# Demo app — Lal Mirch Foods

The practice-project guide (`guides/practice-project.md`) is text.
This folder is the code: a real, minimal Frappe app with the Gate Pass
DocType from Lesson 03, its controller, the client script, and the
hooks. Use it the right way: build the Gate Pass yourself first, step
by step, then compare what you built with this code — and keep
practising until you can build it without the guide. Installing it
gives you a working starting point to check against, not a substitute
for doing the work.

## What is in it

```text
lal_mirch_foods/
├── pyproject.toml                 # app metadata (flit, as `bench new-app` writes it)
├── README.md                      # short app readme
└── lal_mirch_foods/               # the Python package
    ├── __init__.py                # __version__ = "0.0.1"
    ├── hooks.py                   # doc_events (Gate Pass validate) + daily scheduler job
    ├── api.py                     # validate_gate_pass — server-side item check
    ├── tasks.py                   # daily — ToDo reminders for stale draft Delivery passes
    ├── modules.txt                # Lal Mirch Foods
    ├── patches.txt                # empty — no patches yet
    ├── public/.gitkeep            # so bench build symlinks the app's assets
    └── lal_mirch_foods/           # the module (same name as the app, as `bench new-app` makes it)
        ├── .frappe                # module marker
        └── doctype/
            ├── gate_pass/         # Gate Pass: gate_pass.json, gate_pass.py, gate_pass.js, test_gate_pass.py
            └── gate_pass_item/    # Gate Pass Item (child table): gate_pass_item.json, gate_pass_item.py
```

## Install

`bench get-app` cannot install this directly — it lives in a subfolder
of the hub repo, not in its own repo. Copy it into your bench instead:

```bash
cd ~/frappe-bench
cp -r /path/to/frappe-research-hub/demo-app/lal_mirch_foods apps/
bench --site spice.local install-app lal_mirch_foods
bench --site spice.local migrate
```

Then open Desk: the Gate Pass DocType is there, with the fields from
Lesson 03. Create a pass, submit it, and continue the guide at Phase 3.

Run the tests with:

```bash
bench --site spice.local run-tests --app lal_mirch_foods
```

## What is NOT in it

- **The rest of the practice project.** BOMs, Work Orders, the
  Order-to-Cash report and the print format stay as guide steps — type
  those yourself, that is where the learning is.
- **A print-format file.** The invoice print format from Phase 7 is
  Jinja you paste into Desk (Print Format, type Jinja) — see the guide.
  Print formats ship as database records, not app files, unless
  exported as fixtures.
- **An email in `hooks.py` / `pyproject.toml`.** No email address is on
  file for the app author — add your own if you publish the app.

## Notes

- The client script lives in the DocType folder
  (`doctype/gate_pass/gate_pass.js`), where Frappe auto-loads it —
  not in `public/js/`. A file in `public/js/` would never run for the
  form unless wired up with a `doctype_js` hook.
- The `Gatekeeper` role in `gate_pass.json` takes effect once you
  create that role (Phase 8 of the guide); until then only
  System Manager can use the DocType.
- Layout follows `bench new-app` exactly: the module folder has the
  same name as the app, so the DocType path is three segments deep
  (`lal_mirch_foods/lal_mirch_foods/lal_mirch_foods/doctype/...`).
  The DocType JSON structure itself is modelled on the real Frappe v16
  `ToDo`, `DocField` and `DocType Link` files.
