# Studio, Flow & Insights in Desk (v16.60+)

## Ye kya karta hai

v16.60 (17 Nov 2026) ne teen cheezein core Desk experience mein la di hain. **Studio** — drag-and-drop app builder — Framework mein merge ho gaya, is liye chhoti apps baghair code ke visually banti hain. **Frappe Flow** (beta) Desk ke andar AI harness hai: aik LLM jo aap ke data ko analyse karta hai aur forms bharta hai, permission-aware, aap ki apni AI keys istemal kar ke. **Insights** dashboards ab Desk mein embed hote hain, is liye managers live charts wahin dekhte hain jahan wo kaam karte hain, Excel mein export karne ke bajaye. Mil kar ye badal dete hain ke "customisation" kya hai: developer ke kaam se aik aisi cheez jo aik analyst aik din mein bana sakta hai.

## Core pieces

| Piece | Ye kya hai |
|---|---|
| Studio | Aik mini-app visually banao: pages, layouts, data sources, CRUD — baghair code ke. Apps andar se standard Frappe apps hoti hain. |
| Frappe Flow | Desk mein AI harness (beta): apne data se sawal poocho, documents draft karo, forms bharo — AI sirf wohi dekhta hai jo user dekh sakta hai. |
| Insights Dashboard | Desk mein aik live dashboard: ERP data se charts aur numbers, kholne par refresh. |
| Insights Workbook | Mutaliq queries aur charts ka aik set, live data ki spreadsheet ki tarah jis par kaam kiya jaye. |
| Insights Query | Data ke khilaf aik sawal (SQL ya visual builder). |
| Insights Data Source | Woh jagah jahan se query parhti hai: aik DocType, aik table, ya aik external database. |
| Insights Chart | Query se bana hua aik chart. |

Studio apps banata hai; Flow aap ke data ke baaray mein baat karta hai; Insights isay dikhata hai. In mein se koi bhi modules ko replace nahi karta — ye un ke upar baithte hain.

## Shuru se akhir tak ka flow

```text
Build:   Studio → new mini-app (e.g. gate pass, sample tracking) → publish to Desktop
Ask:     Flow → "which customers are overdue?" → answer from live data, permission-aware
See:     Insights Dashboard → sales, stock, finance charts embedded in Desk
Act:     dashboard number → drill into the document → fix it there
```

- **Studio** us chhoti app ke liye hai jo developer ko justify nahi karti: visitor register, gate pass, sample tracking, asset check-in. Isay visually banao, Desktop par publish karo, aur ye kisi bhi doosri app ki tarah behave karti hai.
- **Flow** design se hi permission-aware hai: ye sirf wohi dekh sakta hai jo signed-in user dekh sakta hai. Ye permissions ko bypass nahi karta, aur ye aap ki apni AI keys istemal karta hai — data aap ke AI provider ke paas jata hai, Frappe ke paas nahi.
- Desk mein **Insights** ka matlab hai ke dashboard wahin hai jahan kaam hota hai. Query aik dafa banao, chart ko dashboard par lagao, aur manager Desk khol kar isay dekh leta hai — na export, na purani spreadsheet.
- v16.61 ne **Flow public agents** aur aik AI assistant add kiya jo images dekh sakta hai — naye monthly release train par harness har mahine barh raha hai.

## Amli misaal — aik din mein aik gate pass app

Aik factory ka gate pass aik kagaz ki slip hai: kis ne kya bahar le jaya, guard ke dastakhat ke saath:

1. **Studio** mein, aik analyst "Gate Pass" mini-app banata hai: aik form (item, qty, vehicle, driver, purpose), aik list view, aur aik approval step.
2. App Desktop par publish ho jati hai. Guard phone par isay khol kar har pass log karta hai; store manager Desk se approve karta hai.
3. Manager **Flow** se poochta hai: "how many gate passes this week, and for which items?" — jawab live data se aata hai, numbers ke saath.
4. Aik **Insights Dashboard** rozana passes aur gate se nikalne wali top items dikhata hai — pilferage pattern ki pehli nishani, kisi report ko chalaye baghair nazar aa jati hai.

## Asli use case

Aik client ke quality head ko aik sample-tracking register chahiye tha — labs ko bhejay gaye samples, wapas aane walay results, expiry dates. Coded app ke tor par ye do hafton ka kaam tha; Studio mein ye aik analyst ne aik din mein bana liya, lab results aik form se enter hote thay jisay lab technician istemal kar sakta tha. Client ko app usi hafte mil gayi jis hafte unhon ne manga tha — aur unhon ne do aur mangi.

**Hum isay kaise istemal kar sakte hain:** Studio se bani mini-apps ko aik nayi service line ke tor par offer karo — fixed-price, dinon mein bani hui, har app ke hisab se billed. Aik NexTash analyst ko Studio par train karo taake chhoti apps developer ka waqt lena band kar dein. Flow ko aik dostana client ko test site par pilot ke tor par offer karo ("ask your ERP" un ke apne data par) isay wasee paimane par bechne se pehle.

## Aam ghaltiyan

- **Studio mein woh banana jo module mein hona chahiye.** Agar app asal mein Manufacturing ya HR hai, to module istemal karo. Studio modules ke aas-paas ke gap ke liye hai, un ki jagah lene ke liye nahi.
- **Flow ke jawab par check kiye baghair bharosa karna.** Flow data ko analyse karta hai; ye isay ghalat samajh sakta hai. Jawab aik shuruaat hai — report se verify karo.
- **Dashboards jinhein koi nahi kholta.** Aik dashboard jo teen clicks ki gehrai mein daba ho, woh decoration hai. Woh aik number jo ahem hai, Desktop par lagao.
- **AI keys aise logon ko dena jo un ke malik nahi.** Flow aap ki apni AI keys istemal karta hai — faisla karo ke ye kis ke account aur budget ki hain, pilot se pehle, bill ke baad nahi.
- **Permission check chhor dena.** Flow permissions ka ehtaram karta hai, lekin pehle andar walay roles sahi hone chahiye — aik over-permissioned user AI ko over-informed bana deta hai.

## Agla

[14 — Cross-Module Flows](14-cross-module-flows.md) — forecast → MPS → MRP, sales → stock → accounts.
