# Integrations — Frappe / ERPNext Apps

> [Apps Catalog](../apps-catalog.md) ka hissa — is category mein 11 apps hain. Har app mukhtasar hai: ye kya karta hai, kyun faida deta hai, NexTash ke kaam ke liye ek **Hum isay kaise istemal kar sakte hain** line, aur GitHub link + install command. Pehle staging par test karein.


### Frappe WhatsApp Suite — WhatsApp Business API + chat UI + chatbot (3 apps)
- **What/why:** teen free apps jo mil kar kaam karti hain — WhatsApp Business Cloud API (direct Meta se, koi middleman nahi), Desk ke andar chat UI, aur keyword triggers aur AI fallback wala chatbot.
- **Hum isay kaise istemal kar sakte hain:** isay apni standard WhatsApp offer bana lein — order updates, invoice alerts aur support chats ERPNext ke andar se, koi paid middleman nahi. Trading/distribution clients ko Desk ke andar wali chat UI demo karein; ye woh shared phone replace kar deta hai jo unki sales team aapas mein ghumati hai.
- **GitHub:** https://github.com/shridarpatil/frappe_whatsapp · https://github.com/shridarpatil/whatsapp_chat · https://github.com/shridarpatil/frappe_whatsapp_chatbot — `bench get-app` each repo (all three on Frappe Cloud Marketplace)

### WABA Integration — WhatsApp Business Cloud API (official Frappe)
- **What/why:** official Frappe WhatsApp tareeqa — conservative choice jab client Frappe-maintained code chahta hai.
- **Hum isay kaise istemal kar sakte hain:** jab client official code par zor de to ye propose karein; jab unhein chat UI aur chatbot bhi chahiye to upar wali community suite use karein.
- **GitHub:** https://github.com/frappe/waba_integration — `bench get-app https://github.com/frappe/waba_integration`

### Payment Core — provider-neutral payment layer (Aerele)
- **What/why:** payment integrations ke liye shared foundation — references, transaction lifecycle, settlement, payment pages, idempotency — taake checkout/webhook code har gateway ke liye dobara na likhna pare.
- **Hum isay kaise istemal kar sakte hain:** har payment integration jo hum banayein, uski foundation ke tor par isay adopt karein — payment ka kaam har client ke liye custom hone ke bajaye repeatable ban jayega.
- **GitHub:** https://github.com/aerele/payment-core — `bench get-app https://github.com/aerele/payment-core --branch develop` (Frappe/ERPNext v16, free MIT)

### Stripe Payment — Stripe gateway on Payment Core (Aerele)
- **What/why:** hosted checkout, 3D Secure, subscriptions, signed webhooks — Frappe/ERPNext ke liye modern Stripe tareeqa.
- **Hum isay kaise istemal kar sakte hain:** un clients ko offer karein jo Stripe ke through international payments/subscriptions lete hain. Note: Stripe Pakistan mein locally available nahi hai, is liye ye exporters aur Gulf/UK/US-facing businesses ke liye fit hai, local PKR collection ke liye nahi.
- **GitHub:** https://github.com/aerele/stripe-payment — `bench get-app https://github.com/aerele/stripe-payment --branch develop` (requires Payment Core, free MIT)

### Razorpay Integration — Razorpay payments (official Frappe)
- **What/why:** Indian clients ke liye standard gateway — UPI/cards Razorpay ke through, ERPNext Payment Requests se wired.
- **Hum isay kaise istemal kar sakte hain:** Indian clients ko offer karein (ya Pakistani exporters jo India mein bechte hain) jo online payments lete hain.
- **GitHub:** https://github.com/frappe/razorpay_integration — `bench get-app https://github.com/frappe/razorpay_integration`

### Multi Payment Gateway — payment-choice page for the Webshop
- **What/why:** Webshop checkout par har enabled gateway (Razorpay, Stripe, PayPal, Braintree, Paytm, GoCardless, Cashfree, PayU, COD, bank transfer) list karta hai, ek par majboor karne ke bajaye.
- **Hum isay kaise istemal kar sakte hain:** har Webshop build mein add karein jahan client ek se zyada payment option dena chahta hai — chhota add-on jo checkout ki asli rukawat khatam kar deta hai.
- **GitHub:** https://github.com/Kalvyai-erpnext/ki_erp_multi_payment — `bench get-app https://github.com/Kalvyai-erpnext/ki_erp_multi_payment --branch version-16` (ERPNext 16 only, free MIT)

### ERPNext Shipping — Packlink / LetMeShip / SendCloud shipping
- **What/why:** delivery notes ko labels aur rates ke saath booked shipments mein badal deta hai, alag shipping portal ke bajaye.
- **Hum isay kaise istemal kar sakte hain:** un e-commerce/retail clients ko offer karein jo aaj shipments alag portal mein book karte hain — ye selling aur dispatch ke darmiyan ka loop band kar deta hai.
- **GitHub:** https://github.com/frappe/erpnext-shipping — `bench get-app https://github.com/frappe/erpnext-shipping`

### Twilio Integration — SMS/voice/WhatsApp via Twilio (official Frappe)
- **What/why:** OTPs, order alerts aur reminders ke liye established SMS tareeqa, jab WhatsApp akela kaafi na ho.
- **Hum isay kaise istemal kar sakte hain:** OTPs aur delivery confirmations ke liye use karein jahan SMS abhi bhi chahiye; Twilio har message par charge karta hai, is liye isay client ke running costs mein shamil karke price karein.
- **GitHub:** https://github.com/frappe/twilio-integration — `bench get-app https://github.com/frappe/twilio-integration`

### MSG91 Integration — MSG91 SMS gateway
- **What/why:** MSG91 ke liye direct gateway app, jo India mein widely used SMS provider hai.
- **Hum isay kaise istemal kar sakte hain:** un Indian clients ko offer karein jo pehle se MSG91 par hain — unke existing provider aur rates par SMS alerts.
- **GitHub:** https://github.com/dhwani-ris/frappe_msg91_integration — `bench get-app https://github.com/dhwani-ris/frappe_msg91_integration`

### Frappe Microsoft 365 — Outlook / Teams / OneDrive sync
- **What/why:** two-way Outlook calendar sync, Frappe Events se Teams meetings, transcripts/recordings, OAuth par Outlook mail, Microsoft sign-in.
- **Hum isay kaise istemal kar sakte hain:** un corporate clients ko offer karein jo Outlook/Teams mein rehte hain — calendar aur mail sync "ERP alag island hai" wali objection khatam kar deta hai.
- **GitHub:** https://github.com/Bizmap-Technologies-Pvt-Ltd/frappe_microsoft365 — `bench get-app https://github.com/Bizmap-Technologies-Pvt-Ltd/frappe_microsoft365` (Frappe v15/v16)

### ALYF Banking — bank integration & reconciliation (EBICS)
- **What/why:** EBICS ke through bank feeds aur modern Bank Reconciliation tool — manual statement imports se behtar hai.
- **Hum isay kaise istemal kar sakte hain:** sirf iski status verify karne ke baad — Awesome Frappe is repo ko "Archived" flag karta hai, is liye pehle staging par test karein aur client ko promise na karein jab tak working confirm na ho jaye.
- **GitHub:** https://github.com/alyf-de/banking — `bench get-app https://github.com/alyf-de/banking`

---
