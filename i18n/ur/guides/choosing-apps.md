# Apps Chunna — Kab Install Karna Hai aur Kab Khud Banana Hai

Har app jo aap install karte hain, woh ek dependency hai jo aap ko har upgrade par saath le kar chalni hogi.
Aik app jo aaj do din bacha le aur agle upgrade par toot jaye, woh do hafte kha jati hai. Yeh guide woh decision process hai jo NexTash kisi bhi
`bench get-app` se pehle use karta hai — client project par ho ya apni sites par.

## 5 sawal — kuch bhi install karne se pehle pooch lein

Koi app install nahi hogi jab tak paanchon ke jawab, likh kar, project note par na hon:

1. **Kya yeh kisi real project ka real masla hal karti hai?** "Lagta hai useful hai" nahi — aik named client, aik named takleef, is mahine. Aik app jo
   "baad ke liye" install ki gayi ho, woh aik dependency hai jis ka koi owner nahi.
2. **Kya yeh maintained hai?** Repo check karein: pichle 6 mahine mein aik release,
   open issues ke jawab mil rahe hon, stars sirf aik rough signal hain. Aik repo jis mein
   aik saal se koi commit na ho, woh aik marti hui app hai — aap us ke maintainer ban jayenge.
3. **Kya yeh aap ke Frappe / ERPNext version se match karti hai?** Us ke paas aap ke version ke liye branch honi chahiye —
   `version-14`, `version-15`, `version-16` — ya README mein likha ho. "v15 par chalti hai" ka matlab "v16 par chalti hai" nahi hai.
4. **Kya is se bahar nikalne ka rasta hai?** Kya aap data export kar ke cleanly uninstall kar sakte hain? Agar is ko hatane ka matlab data khona ya database ko haath se edit karna hai, to data aap ka nahi hai — app ka hai.
5. **Jab yeh toot jaye to is ka owner kaun hai?** Aik named shakhs, "team" nahi. Agar
   koi owner nahi hai, to yeh client ke sab se busy din tootegi aur kisi ko pata nahi hoga ke yeh kis ka kaam hai.

Aik "mujhe nahi pata" theek hai — staging par test karein aur pata laga lein. Do ya
zyada "mujhe nahi pata" ka matlab hai abhi install na karein.

## Install karein — jab kisi aur ne pehle se behtar hal kar diya ho

Install karein jab masla aik poora module ho, app official ya well-maintained ho, aur khud banana hafton ka kaam ho:

| Zaroorat | Install karein | Kyun |
|---|---|---|
| CRM | [Frappe CRM](https://github.com/frappe/crm) — `bench get-app https://github.com/frappe/crm` | Official, actively developed, web forms + pipeline. [CRM lesson](../learn/erpnext/people/10-crm.md) dekhein. |
| Support desk | [Frappe Helpdesk](https://github.com/frappe/helpdesk) | Official, SLAs + portal + knowledge base. [Helpdesk lesson](../learn/erpnext/people/11-helpdesk.md) dekhein. |
| HR | Frappe HRMS (hrms app) | Official HR: leave, attendance, payroll. [HR lesson](../learn/erpnext/people/09-hr.md) dekhein. |
| Chat | Raven (official, github.com/frappe/raven) | Desk ke andar team chat; v3 current version hai. |
| POS | [POSNext](https://github.com/BrainWise-DEV/POSNext) (v15+, offline mode) ya [POS Prime](https://github.com/ravindu2012/pos-prime) (v14/v15/v16, zero core changes) | POS aik product hai, feature nahi — is ko kabhi scratch se na banayein. |
| Dashboards | [Frappe Insights](https://github.com/frappe/insights) | Live data par official BI. Note: v3.50 ne v2 hata diya — pehle v2 dashboards migrate karein. |
| WhatsApp | [Frappe WhatsApp Suite](https://github.com/shridarpatil/frappe_whatsapp) (+ chat UI + chatbot) ya official [WABA Integration](https://github.com/frappe/waba_integration) | Woh channel jo Pakistan mein clients asal mein parhte hain. |

Rule of thumb: **agar app official Frappe code hai, to pehle install karein aur behes baad mein karein.** Official apps ko version branches, upgrade patches aur aik
migration path milta hai — woh teen cheezein jo upgrade ke waqt aap ko mehngi parti hain.

## Khud banayein — jab gap chhota aur specific ho

Banayein jab zaroorat aik register, aik form, aik chhota workflow ho — poora module nahi:

- **Aik gate-pass register, aik sample tracker, aik visitor log.** Aik Studio
  mini-app, jo aik analyst visually aik din mein bana le (dekhein
  [Studio, Flow & Insights](../learn/erpnext/v16/13-studio-flow-insights.md)).
  Aik register ke liye poori app install karna aise hai jaise tap theek karne ke liye poori company hire kar lein.
- **Kisi existing DocType par aik extra field ya aik chhota rule.** Aik Custom
  Field (fixture ke tor par) ya aik Server Script — app nahi, fork nahi.
  [Server Scripts](../learn/framework/level-2/05-server-scripts-events.md) dekhein.
- **Aik gap jo kisi ne abhi tak nahi banaya.** Pakistan payments asal example hain:
  koi free public Easypaisa / JazzCash app nahi hai — catalog ka
  sab se bara gap. Yeh aik build hai (Payment Core par,
  github.com/aerele/payment-core), aur yeh aik product opportunity hai, sirf
  aik project task nahi.

Agar build Studio mein aik din se kam ya code mein aik hafte se kam ka hai, to bana lein. Agar
yeh aik mahine se zyada ka hai, to dobara app dhoondein — ya client se build ke paise honestly lein, aik product ke tor par, favour ke tor par nahi.

## Extend karein — beech ka rasta

Zyada tar asal kaam na install hai na build — woh woh hai jo pehle se hai us ko extend karna, apni app se:

- Custom Fields aur Property Setters, fixtures ke tor par export kiye hue.
- Aik quick rule ke liye Server Scripts (dekhein
  [Server Scripts](../learn/framework/level-2/05-server-scripts-events.md)).
- `doc_events` hooks.py mein, jo aap ki app mein aik override file ki taraf point karein.
- Aik whitelisted method + `frappe.call`, aik button ke liye jo server ka kaam kare.

Aur sakht rule, hamesha: **kabhi kisi aur app ka code edit na karein.** Aik line bhi nahi, "sirf is dafa" bhi nahi. Agla `bench update` us ko mita dega, aur
client ko Monday ko pata chalega. Apni app se extend karein, ya na karein.
([Common mistakes](common-mistakes.md) §2 dekhein.)

## Red flags — door hat jayein

- **Abandoned.** Aakhri commit aik saal se purana, issues ke jawab nahi. TailPOS
  (aakhri activity Oct 2022) aur ALYF Banking (repo Archived flag hai)
  catalog ke examples hain — sirf staging test ke liye, kabhi promise na karein.
- **Yeh core DocTypes ko fork karti hai.** Aik app jo Sales
  Order / Stock Entry ko replace ya rewrite karti hai, woh agle ERPNext update par toot jayegi. Install karne se pehle check karein ke yeh kya override karti hai.
- **Aap ke Frappe version ke liye koi version branch nahi.** v16
  site par "v15 par chalti hai" aik staging-test failure hai jo hone wala hai.
- **Is ko chalne ke liye Administrator chahiye.** Aik app jo sirf Administrator ke tor par kaam karti hai, us ka permission model hai "sab admin hain". Is ko
  client site par na lagayein.
- **Paid, bina trial ke.** Bina staging par test karne ke tareeqe ke aik price aik
  sales call hai, product nahi. Pehle staging licence maangein.
- **Koi uninstall story nahi.** Agar README mein is ko hatane ke baare mein kuch nahi likha, to maan lein ke data phansa hua hai.

## Worked example — aik client, teen zarooratein

Aik spice manufacturer (fmc demo client) teen cheezein maangta hai. Wahi
framework, teen mukhtalif jawab:

**(a) CRM — install karein.** Real masla (leads WhatsApp mein rehte hain), official
app (Frappe CRM, github.com/frappe/crm), version-16 branch, data
exportable, owner: sales lead. **Decision: `bench get-app` Frappe
CRM.** Client ko kabhi legacy ERPNext CRM par start na karein — woh v17 mein removal ke liye scheduled hai.

**(b) Gate-pass register — khud banayein.** Aik form, aik list, aik approval.
Catalog mein koi app sirf yeh nahi karti, aur aik register ke liye poori app
aik dependency hai jis ka koi faida nahi. **Decision: Studio mein aik din mein bana lein**
— form, list view, approval step — Desktop par publish karein. (Yeh
[Studio example](../learn/erpnext/v16/13-studio-flow-insights.md) hai.)

**(c) WhatsApp notifications — install karein.** Real masla (customers kabhi
email nahi parhte), maintained app, version branch mojood hai. **Decision: Frappe WhatsApp Suite install karein** (Business Cloud API + in-Desk chat + chatbot)
— ya official WABA Integration agar client sirf Frappe-maintained
code chahta hai. Order aur invoice alerts document events par bahar jayenge; 
chat UI us shared phone ki jagah le lega jo sales team aapas mein pass karti hai.

## Maintenance cost — har app aik upgrade dependency hai

Install ki hui app install day ke baad free nahi hoti. Har upgrade par, har
app aik aur branch hai jo check karni hai, aik aur `migrate` jo fail ho sakta hai, aik
aur staging test. Agle upgrade se pehle, har installed app ki list banayein
aur 5 sawal dobara poochein — aik app jo pichle saal sahi thi, is saal
abandoned ho sakti hai. Poora upgrade process
[Upgrade guide](upgrade-v14-v15-v16.md) mein hai.

## `bench get-app` se pehle — checklist

- [ ] Aik real project par aik real masla, likh kar named
- [ ] Repo check kiya: recent release, issues ke jawab, aap ke Frappe version ke liye version branch
- [ ] Pehle staging par uninstall + data export test kiya
- [ ] Jab yeh toot jaye to us ke liye aik owner named
- [ ] Staging par install kiya, real user accounts se test kiya (Administrator se nahi)
- [ ] Upgrade impact note kiya: upgrade checklist par aik aur app

## Sources

App facts [Apps Catalog](../research/apps-catalog.md) se (66 apps,
11 categories, Nov 2026 mein verified) aur [ERPNext lessons](../learn/erpnext/README.md) se.
Decision rules asal NexTash projects se; upgrade cost
[Upgrade guide](upgrade-v14-v15-v16.md) se.
