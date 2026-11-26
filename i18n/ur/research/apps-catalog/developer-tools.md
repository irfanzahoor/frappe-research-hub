# Developer tools — Frappe / ERPNext Apps

> [Apps Catalog](../apps-catalog.md) ka hissa — is category mein 8 apps hain. Har app mukhtasar hai: ye kya karta hai, kyun faida deta hai, NexTash ke kaam ke liye ek **Hum isay kaise istemal kar sakte hain** line, aur GitHub link + install command. Pehle staging par test karein.


### Print Designer — drag-and-drop print format designer (frappe v14/v15 only)
- **What/why:** visual print format builder — invoices aur reports ke liye HTML/Jinja coding ki zaroorat nahi.
- **Hum isay kaise istemal kar sakte hain:** v14/v15 clients par invoice/quotation formats jaldi design karne ke liye use karein. v16 ke liye built-in print format designer (v16.50+) use karein — Print Designer ki v16 compatibility unconfirmed hai, pehle staging par verify karein.
- **GitHub:** https://github.com/frappe/print_designer — `bench get-app https://github.com/frappe/print_designer`

### Bench Companion — VS Code extension for bench
- **What/why:** VS Code se bench sites aur development manage karta hai — team ke liye kam terminal work.
- **Hum isay kaise istemal kar sakte hain:** har NexTash developer ke liye install karein — ye standardise karta hai ke team bench sites ke saath kaise kaam karti hai.
- **GitHub:** https://github.com/vineetjacob/bench-companion — VS Code extension, not a bench app.

### Frappe VS Code — Frappe extension for VS Code (official Frappe)
- **What/why:** Frappe development ke liye official VS Code tooling.
- **Hum isay kaise istemal kar sakte hain:** team ka editor setup isi par standardise karein — har developer ek hi tareeqe se kaam kare.
- **GitHub:** https://github.com/frappe/vscode — VS Code extension, not a bench app.

### Frappe S3 Attachment — store attachments on S3
- **What/why:** attachments ko S3 par move kar deta hai, local disk bachata hai aur backups clean rakhta hai.
- **Hum isay kaise istemal kar sakte hain:** un clients ke liye use karein jinke attachments heavy hain (photos, PDFs) — ye unke servers ko lean rakhta hai aur hamari hosting setup ka standard hissa hai.
- **GitHub:** https://github.com/frappe/s3-attachment — `bench get-app https://github.com/frappe/s3-attachment`

### ERPNext Excel — Excel as a low-code layer
- **What/why:** users ko data Excel mein manage aur analyse karne deta hai, jabke ERPNext source of truth rehta hai.
- **Hum isay kaise istemal kar sakte hain:** un finance teams ko offer karein jo Excel mein rehti hain — woh apna workflow rakhte hain, hum data ERPNext mein rakhte hain.
- **GitHub:** https://github.com/frankmoney/erpnext_excel — `bench get-app https://github.com/frankmoney/erpnext_excel`

### ERPNext Import Tool — import via Excel + S3 (paid)
- **What/why:** bulk data migration ke liye guided import tool — un teams ke liye jo built-in Data Import se struggle karti hain.
- **Hum isay kaise istemal kar sakte hain:** un migrations par use karein jahan client ka data messy spreadsheets mein hai — ye ek hi go-live mein apni cost nikal leta hai.
- **GitHub:** no public repo verified — Marketplace only (search "ERPNext Import Tool" on https://cloud.frappe.io/marketplace)

### Frappe Manager — local Docker-based Frappe development
- **What/why:** full bench install ke baghair Docker-based local development — naye developers ki onboarding tez hoti hai.
- **Hum isay kaise istemal kar sakte hain:** naye NexTash developers ko fast onboard karne ke liye use karein — bench setup ke ek din ke bajaye minutes mein working local site.
- **GitHub:** https://github.com/rtcamp/Frappe-Manager — not a bench app; local development tool.

### ERPNext Admin Tools — bulk delete + cache controls for admins
- **What/why:** support work ke liye admin utilities (bulk delete, cache clearing).
- **Hum isay kaise istemal kar sakte hain:** client support calls par internally use karein — custom scripts ke baghair bulk cleanup.
- **GitHub:** https://github.com/brianlam38/erpnext-admin-tools — `bench get-app https://github.com/brianlam38/erpnext-admin-tools`

---
