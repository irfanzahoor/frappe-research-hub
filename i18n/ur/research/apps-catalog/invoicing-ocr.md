# Invoicing & OCR — Frappe / ERPNext Apps

> [Apps Catalog](../apps-catalog.md) ka hissa — is category mein 2 apps hain. Har app mukhtasar hai: ye kya karta hai, kyun faida-mand hai, NexTash ke kaam ke liye ek **Hum isay kaise istemal kar sakte hain** line, aur GitHub link + install command. Pehle staging par test karein.


### ERPNext OCR — Tesseract OCR inside Frappe (Monogramm)
- **What/why:** free, self-hosted OCR building block — na AI vendor, na per-page fee.
- **Hum isay kaise istemal kar sakte hain:** custom builds ke andar free OCR layer ke tor par use karein (scanned delivery notes, CNIC copies) price-sensitive Pakistani clients ke liye.
- **GitHub:** https://github.com/Monogramm/erpnext_ocr — `bench get-app https://github.com/Monogramm/erpnext_ocr`

### ERP OCR Integration — AI invoice import via Drive / email / upload
- **What/why:** supplier invoices (PDF/photo) AI se parhe jate hain — supplier, lines, amounts, VAT extract aur match ho jata hai — Drive, email ya upload se aate hain, kuch bhi auto-post nahi hota.
- **Hum isay kaise istemal kar sakte hain:** supplier bills mein doobi hui accounts teams ko paid AP-automation add-on ke tor par bechein; accountant control mein rehta hai kyun ke kuch bhi automatically post nahi hota.
- **GitHub:** https://github.com/wphamman/erpocr_integration — no `bench get-app` stated in source; see the repo README / OCR Quick Start Guide.

---
