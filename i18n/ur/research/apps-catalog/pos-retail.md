# POS & Retail — Frappe / ERPNext Apps

> [Apps Catalog](../apps-catalog.md) ka hissa — is category mein 5 apps hain. Har app mukhtasar hai: ye kya karta hai, kyun faida-mand hai, NexTash ke kaam ke liye ek **Hum isay kaise istemal kar sakte hain** line, aur GitHub link + install command. Pehle staging par test karein.


### POSNext — modern offline POS for ERPNext (Vue 3)
- **What/why:** tez billing, multiple payments, discounts, offline mode, touchscreen UI, split payments, coupons/gift cards, shift cash reconciliation — sab se credible built-in POS replacement.
- **Hum isay kaise istemal kar sakte hain:** retail aur pharmacy clients ke liye isay hamara default POS offer banayein — offline mode un jagah par khud bik jata hai jahan internet unreliable hai, aur shift reconciliation se manual till counting khatam ho jati hai.
- **GitHub:** https://github.com/BrainWise-DEV/POSNext — `bench get-app https://github.com/BrainWise-DEV/POSNext` (ERPNext v15+, free AGPL-3.0)

### POS Prime — modern POS, zero ERPNext modifications (v14/v15/v16)
- **What/why:** modern Vue 3 POS jo sirf standard DocTypes use karta hai — na custom fields, na DocTypes, install/uninstall saaf tareeqe se hota hai, is liye upgrades saaf rehte hain.
- **Hum isay kaise istemal kar sakte hain:** risk-averse clients aur abhi bhi v14 par chalne wale clients ko propose karein — "zero core changes" woh line hai jo upgrade breakage se pareshan owners se haan karwa leti hai.
- **GitHub:** https://github.com/ravindu2012/pos-prime — `bench get-app https://github.com/ravindu2012/pos-prime` (v14/v15/v16, free)

### POS Awesome — open-source POS (Vue.js + Vuetify)
- **What/why:** established community POS — widely deployed, is liye client teams isay pehle se janti hain.
- **Hum isay kaise istemal kar sakte hain:** jab kisi client ya unke staff ko POS Awesome pehle se kisi site se pata ho to isay use karein — koi retraining nahi. v15 sites ke liye V15 fork use karein.
- **GitHub:** https://github.com/yrestom/POS-Awesome — `bench get-app https://github.com/yrestom/POS-Awesome` · V15 fork: https://github.com/defendicon/POS-Awesome-V15

### TailPOS — offline-first POS
- **What/why:** un shops ke liye simple offline-first POS jahan internet unreliable hai.
- **Hum isay kaise istemal kar sakte hain:** chhoti shops ke liye fallback ke tor par rakhein jahan POSNext zyada heavy lagay — lekin pehle verify karein: last activity Oct 2022 note hui thi, ho sakta hai unmaintained ho. Sirf staging test ke baad propose karein.
- **GitHub:** https://github.com/bailabs/tailpos — `bench get-app https://github.com/bailabs/tailpos`

### X POS — offline-first POS, web / PWA / Electron
- **What/why:** tez, keyboard-driven, mukammal offline POS, desktop (Electron) app ke tor par bhi deploy ho sakta hai.
- **Hum isay kaise istemal kar sakte hain:** retail/restaurant counters ko offer karein jo browser tab ki bajaye asli desktop till app chahte hain.
- **GitHub:** https://github.com/kodlyft/xpos — `bench get-app https://github.com/kodlyft/xpos.git`

---
