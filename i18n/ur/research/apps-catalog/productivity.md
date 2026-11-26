# Productivity — Frappe / ERPNext Apps

> [Apps Catalog](../apps-catalog.md) ka hissa — is category mein 8 apps hain. Har app mukhtasar hai: ye kya karta hai, kyun faida deta hai, NexTash ke kaam ke liye ek **Hum isay kaise istemal kar sakte hain** line, aur GitHub link + install command. Pehle staging par test karein.


### Frappe Learning — LMS / academy inside Frappe (official Frappe)
- **What/why:** ERP ke andar courses, lessons aur quizzes — staff aur clients ki training ke liye.
- **Hum isay kaise istemal kar sakte hain:** client training academy isi par banayein — naye users ke liye onboarding courses, progress tracked ke saath. NexTash ki apni onboarding ke liye bhi use karein.
- **GitHub:** https://github.com/frappe/learning — `bench get-app https://github.com/frappe/learning` (verify exact bench command in the repo README)

### Frappe Insights — BI dashboards (official Frappe)
- **What/why:** Frappe/ERPNext ke liye official BI tool — live data par dashboards, managers ke liye self-service.
- **Hum isay kaise istemal kar sakte hain:** har go-live ke baad Insights dashboard package ko phase-2 sale ke tor par bechein — sales, stock aur finance dashboards, Excel exports ki zaroorat nahi. Note: v3.50 (Nov 2026) removed v2 — migrate v2 dashboards before upgrading.
- **GitHub:** https://github.com/frappe/insights — `bench get-app https://github.com/frappe/insights` (free MIT)

### Frappe Drive — file management + Google Docs clone (official Frappe)
- **What/why:** Frappe ke andar file storage aur collaborative docs — same system mein Google Drive/Docs ka replacement.
- **Hum isay kaise istemal kar sakte hain:** un clients ko offer karein jo sirf shared files ke liye Google Workspace/SharePoint ke paise de rahe hain — ye documents ko ERP ke andar rakhta hai.
- **GitHub:** https://github.com/frappe/drive — `bench get-app https://github.com/frappe/drive`

### Frappe Gameplan — project management inside Frappe (official Frappe)
- **What/why:** Frappe ke andar project planning aur tracking — un clients ke liye jo projects alag tool mein chalate hain.
- **Hum isay kaise istemal kar sakte hain:** service/project clients ko unke alag project tool ki jagah offer karein — do systems ke bajaye ek system.
- **GitHub:** https://github.com/frappe/gameplan — `bench get-app https://github.com/frappe/gameplan`

### Frappe Wiki — wiki / knowledge base (official Frappe)
- **What/why:** Frappe ke andar ek wiki — documentation aur SOPs wahin jahan team pehle se kaam karti hai.
- **Hum isay kaise istemal kar sakte hain:** implementation ke doran client ki SOP library isi par banayein — ye handover ka hissa ban jati hai aur support calls kam kar deti hai.
- **GitHub:** https://github.com/frappe/wiki — `bench get-app https://github.com/frappe/wiki`

### Frappe Email Flow — visual email automation builder
- **What/why:** email flows ka visual builder — welcome sequences, reminders, follow-ups — server scripts likhe baghair.
- **Hum isay kaise istemal kar sakte hain:** un sales/service clients ko offer karein jo har roz wahi emails haath se bhejte hain — ye repetitive follow-ups automate kar deta hai.
- **GitHub:** https://github.com/Alex-Yablonsky/frappe-email-flow — `bench get-app https://github.com/Alex-Yablonsky/frappe-email-flow`

### Frappe Builder — no-code website & page builder (official Frappe)
- **What/why:** marketing pages aur customer portals visually banayein — frappe.io khud isi se bana hai; editor mein AI assistant "Bob" (Nov 2026); v1.31.0 se MIT licence.
- **Hum isay kaise istemal kar sakte hain:** client marketing pages aur portals ko kisi bhi implementation ke saath fixed-price add-on ke tor par deliver karein — alag website project ki zaroorat nahi.
- **GitHub:** https://github.com/frappe/builder — `bench get-app https://github.com/frappe/builder`

### Frappe Cloud 2.0 — hosting rebuild (Pilot / Atlas / Central)
- **What/why:** naya Frappe Cloud — root/SSH wale VMs, one-click apps, Object Storage, LLMs; public beta 24 Nov 2026, target Jan 2027; Bench archived.
- **Hum isay kaise istemal kar sakte hain:** hosting-migration clients ko Cloud 2.0 VMs par move karein jab ye live ho — isolated VMs downtime complaints ka jawab hain. "Bench to Cloud 2.0" migration ko ek service ke tor par offer karein.
- **GitHub:** no repo — Frappe Cloud product, https://discuss.frappe.io/t/frappe-cloud-2-0-is-in-public-beta/165969

---
