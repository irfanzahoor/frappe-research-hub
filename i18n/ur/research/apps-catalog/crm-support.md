# CRM & Support — Frappe / ERPNext Apps

> [Apps Catalog](../apps-catalog.md) ka hissa — is category mein 4 apps hain. Har app mukhtasar hai: ye kya karta hai, kyun faida-mand hai, NexTash ke kaam ke liye ek **Hum isay kaise istemal kar sakte hain** line, aur GitHub link + install command. Pehle staging par test karein.


**Baselines:** **Frappe CRM** (official) — https://github.com/frappe/crm, `bench get-app https://github.com/frappe/crm` — leads/deals, Kanban pipeline, ERPNext invoicing link. **Frappe Helpdesk** (official) — https://github.com/frappe/helpdesk, `bench get-app https://github.com/frappe/helpdesk` (v14/v15/v16) — email tickets, SLAs, assignment rules, customer portal, knowledge base. **How we can use them:** CRM ko ERPNext ke legacy CRM module ki bajaye default sales app banayein, aur Helpdesk ko kisi bhi client ka default desk banayein jis ki support shared inbox par chalti hai (unlimited agents, no per-seat fee).

### WATI Integration — WhatsApp Business API via WATI, for CRM follow-ups
- **What/why:** ERPNext events (new/save/submit/change) par templates ke saath WhatsApp messages bhejta hai — woh channel jo Pakistan/India/Gulf ke clients asal mein parhte hain.
- **Hum isay kaise istemal kar sakte hain:** un sales teams ko offer karein jo leads ko WhatsApp par manually chase karti hain — lead/order events par follow-ups automatically chale jate hain.
- **GitHub:** https://github.com/bhavesh95863/wati_integration — `bench get-app https://github.com/bhavesh95863/wati_integration` (verify in repo README; also on Frappe Cloud Marketplace)

### IndiaMART Integration — IndiaMART enquiries → ERPNext Leads
- **What/why:** IndiaMART enquiries ko automatically ERPNext mein Leads ke tor par le aata hai — spreadsheets se dobara type karne ki zaroorat nahi.
- **Hum isay kaise istemal kar sakte hain:** Indian manufacturers/traders (aur IndiaMART par list karne wale Pakistani exporters) ko offer karein — enquiries khud CRM pipeline mein aa jati hain.
- **GitHub:** no public repo verified — Marketplace only (search "Indiamart ERPNext Integration" on https://cloud.frappe.io/marketplace)

### Mautic Integration — marketing automation (Dokos)
- **What/why:** contacts/leads Mautic ke saath sync hote hain campaigns, lead scoring aur nurture emails ke liye — ERPNext ke basic email tools ki bajaye asal marketing automation.
- **Hum isay kaise istemal kar sakte hain:** un B2B clients ko offer karein jin ki asal sales pipeline hai aur jo campaigns spreadsheet ya kisi alag tool se chalate hain.
- **GitHub:** https://github.com/dokos-io/mautic — `bench get-app https://github.com/dokos-io/mautic`

### GitHub Helpdesk Integration — GitHub issues/PRs ↔ Frappe Helpdesk
- **What/why:** GitHub issues, PRs, comments aur commits ko Helpdesk tickets ke saath link karta hai — helpdesk aur repo ke darmiyan copy-paste nahi.
- **Hum isay kaise istemal kar sakte hain:** NexTash ke apne support flow ke liye use karein aur un software-company clients ko offer karein jo Helpdesk chalate hain.
- **GitHub:** no public repo verified — Marketplace only (https://cloud.frappe.io/marketplace)

---
