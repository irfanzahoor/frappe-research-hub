# 17 — Studio & Flow

## Yeh kya hai

Do v16.60 features jo badal dete hain ke cheezein kaun banata hai:

- **Studio** ek visual app builder hai, jo Framework mein merge ho gaya hai. Aap blocks se pages assemble karte hain, unhein Frappe data se bind karte hain, aur publish kar dete hain — bina code ke. App database mein **Studio App** aur **Studio Page** records ke tor par rehti hai, aur git aur deployment ke liye ek standard Frappe app mein export ki ja sakti hai.
- **Flow** Desk ke andar ek AI assistant hai (beta, v16.60+). Aap saadi zabaan mein poochte hain aur woh aapki site par kaam karta hai — live data ke baare mein sawalon ke jawab deta hai, records banata hai, documents ka draft likhta hai. Woh us shakhs ki permissions ke saath kaam karta hai jo pooch raha hai, is liye woh us se zyada kabhi nahi dekh ya badal sakta jitna woh khud kar sakta hai. Yeh aapki apni AI provider keys istemal karta hai.

ERPNext path ke Lesson 13 mein dono ko feature level par introduce kiya gaya tha. Yeh lesson hands-on version hai: ek mini-app banayein, ek sawal poochein.

## Minimal working example — Studio mein ek Gate Pass mini-app

Data source ke tor par Lesson 03 wala Gate Pass DocType dobara istemal karein. Desk → search **Studio** → New **Studio App**:

| Field | Value |
|---|---|
| App Name | `gate-pass-app` |
| Title | Gate Pass |
| Route | `gate-pass` |
| Home Page | `passes` |

**Page 1 — list.** New **Studio Page**, route `passes`. DocType **Gate Pass** par type **Document List** ka ek data resource add karein, phir page par ek table block drag karein aur uski rows ko us resource se bind karein (columns: name, visitor, company, date). Yeh woh page hai jo guard phone par kholta hai.

**Page 2 — form.** New **Studio Page**, route `new-pass`. DocType **Gate Pass** par type **Document** ka ek data resource add karein (new document), phir uske fields se bound form blocks drag karein: visitor name, company, purpose, items. Ek submit button add karein jo document save karta hai.

Dono pages ko Studio toolbar se preview karein, layout theek karein, phir **Publish** karein. App aapki site par `/gate-pass` par live hai. Ise code ke tor par ship karne ke liye (git, doosri sites): developer mode on karein, app ko Studio mein kholein, **Export App** par click karein, **Enable App Export** on karein, apni Frappe app chunein, aur **Update** par click karein — Studio ise `apps/<your_app>/studio/<app_name>/` mein likh deta hai.

## Minimal working example — Flow se ek sawal

Pehle setup (sirf System Manager): apni site par `/flow` kholein, ek provider chunein (Anthropic, OpenAI, ya Ollama jaisa koi custom OpenAI-compatible server), uski API key paste karein, **Connect** par click karein, aur woh model chunein jis se naye chats shuru hon. Users ko **Flow User** role dein.

Phir, Desk mein kahin bhi, **Ctrl+I** (Mac par Cmd+I) dabayein aur poochein:

> "Which customers have overdue Sales Invoices, and how much is each
> one owed?"

Flow live data parh kar numbers ke saath jawab deta hai — aur sirf woh customers jo signed-in user ko dekhne ki ijazat hai. Use action lene ko kahein, aur woh offer karega: *"Create a ToDo for the sales manager listing the three
oldest overdue invoices."* Approve karne se pehle parh lein ke woh kya karne wala hai — Flow data ko ghalat samajh sakta hai, aur ek approved action ek asal action hota hai (beta).

## Kab istemal karein — aur kab nahi

| Situation | Use |
|---|---|
| Ek chhoti app jiske liye developer justify nahi hota | Studio — visitor register, sample tracking, gate pass |
| Ek analyst ko ek din mein form + list chahiye | Studio |
| Live data ke baare mein sawal ("kaun se orders late hain?") | Flow |
| Kisi document ka draft ya kisi record ka pehla version | Flow, phir verify karein |
| Ek poora module (Manufacturing, HR, Accounting) | Module — Studio modules ke aas-paas ke gap ke liye hai, unka replacement nahi |
| Ek rule jo hamesha hold karna chahiye | Controller code (Lesson 05), kabhi Flow nahi |
| Live data par production change | Ek insaan, backup ke saath — Flow draft banata hai, log faisla karte hain |

## Common mistakes

- **Studio mein woh banana jo module mein hona chahiye.** Agar app asal mein Manufacturing ya HR hai, to module istemal karein.
- **Flow ke jawab par bina check kiye bharosa karna.** Us par amal karne se pehle numbers ko report se verify karein.
- **AI keys ka koi owner nahi.** Flow aapki apni provider keys istemal karta hai — pilot se pehle faisla karein ke woh kis ke account aur budget ki hain, bill aane ke baad nahi.
- **Permission check skip karna.** Flow permissions ka ehtaram karta hai, lekin pehle underlying roles theek hone chahiye — ek over-permissioned user AI ko bhi over-informed bana deta hai.
- **Ek Studio app jo kisi ko milti hi nahi.** Ise publish karein, phir ise wahan rakhein jahan log dekhte hain: Desktop par, ya us module se ek link jahan se iska talluq hai.
- **App ko kabhi export na karna.** Sirf database mein rehne wali app git par ya doosri site par nahi ja sakti. Jab woh kaam karne lage to ise export karein.

## Next

[18 — Insights](18-insights.md) — live data par dashboards, Desk mein banaye gaye: data source, query, chart, dashboard.
