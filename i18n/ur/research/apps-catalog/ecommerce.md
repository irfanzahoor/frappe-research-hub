# E-commerce — Frappe / ERPNext Apps

> [Apps Catalog](../apps-catalog.md) ka hissa — is category mein 3 apps hain. Har app mukhtasar hai: ye kya karta hai, kyun faida deta hai, NexTash ke kaam ke liye ek **Hum isay kaise istemal kar sakte hain** line, aur GitHub link + install command. Pehle staging par test karein.


### Ecommerce Integrations — Shopify / Amazon / Unicommerce (official Frappe)
- **What/why:** official connectors — Shopify ke orders Sales Orders ban kar aa jate hain, stock Shopify se sync hota hai, items drafts ke tor par upload hote hain; ERPNext hi source of truth rehta hai.
- **Hum isay kaise istemal kar sakte hain:** kisi bhi client ke liye standard jawab hai jiski Shopify store hai; un e-commerce sellers ko offer karein jo aaj Shopify aur ERPNext ko haath se mila rahe hain.
- **GitHub:** https://github.com/frappe/ecommerce_integrations — `bench get-app https://github.com/frappe/ecommerce_integrations`

### CAZ WooSync — real-time two-way WooCommerce ↔ ERPNext sync
- **What/why:** products, orders, customers, inventory, prices, invoices, refunds, coupons ka two-way sync — real-time webhooks, polling fallback ke saath, multi-store, queue dashboard. Ye khaali jagah bharta hai (v15/v16 ke liye koi maintained Frappe WooCommerce connector nahi hai).
- **Hum isay kaise istemal kar sakte hain:** har us client ko offer karein jo WooCommerce store chala raha hai; sync-health dashboard se hum isay theek se support kar sakte hain.
- **GitHub:** https://github.com/codeatozcom/CAZ_WOOSYNC — `bench get-app https://github.com/codeatozcom/CAZ_WOOSYNC` (v14–v16, free MIT)

### WooCommerce Connector — WooCommerce sync (Libracore)
- **What/why:** lamba arsa chalne wala alternative WooCommerce connector — client ko commit karne se pehle CAZ WooSync se compare karna chahiye.
- **Hum isay kaise istemal kar sakte hain:** staging store par dono connectors test karein aur woh chunein jo client ke order volume aur product count ke hisab se fit baithta hai.
- **GitHub:** https://github.com/libracore/WooCommerceConnector — `bench get-app https://github.com/libracore/WooCommerceConnector`

---
