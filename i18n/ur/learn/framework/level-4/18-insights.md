# 18 — Insights

## Yeh kya hai

Insights live ERP data ko dashboards mein badal deta hai — bina exports ke, bina stale spreadsheets ke. v16.60 se dashboards Desk mein embed hote hain, jahan managers pehle se kaam karte hain. Chaar hisse, tarteeb se:

| Piece | What it is |
|---|---|
| **Data Source** | Data kahan rehta hai: ek DocType table, ya ek external database (MySQL, PostgreSQL, DuckDB, BigQuery) |
| **Query** | Data ke khilaf ek sawal — visually banaya gaya (Source, Join, Filter, Group & Summarise) ya SQL mein |
| **Chart** | Ek query ki ek visualisation: Number, Bar, Line, Row, Table, Pie |
| **Dashboard** | Grid par arrange kiye gaye charts, filters ke saath — woh page jo manager kholta hai |
| **Workbook** | Woh folder jisme queries, charts aur dashboards ka ek set hota hai, apni permissions ke saath |

## Minimal working example — Desk mein ek sales dashboard

Desk mein **Insights** kholein. Neeche sab kuch ek hi Workbook ke andar hota hai.

**1. Workbook.** **+ New Workbook** par click karein, iska naam `Sales Overview` rakhein.

**2. Query.** Ek naya workbook ek query se shuru hota hai — source table `Sales Invoice` chunein. Phir tarteeb se operations add karein:

```text
Source:  Sales Invoice
Filter:  docstatus = 1  AND  posting_date is this month
Group:   by customer, Sum of grand_total
```

Query ko `Monthly Sales by Customer` ke naam se save karein. Ek query reusable hoti hai — neeche har chart usi se parhta hai, is liye logic ek hi jagah rehti hai.

**3. Charts.** **+ New Chart** par do dafa click karein:

- **Number chart** "Revenue this month": query se `grand_total` ka Sum — upar wala ek number.
- **Bar chart** "Revenue by customer": ek axis par customer, doosre par `grand_total`.

**4. Dashboard.** **+ New Dashboard** par click karein, iska naam `Sales Overview` rakhein. Left panel se dono charts ko grid par drag karein — Number pehli row par, Bar uske neeche. **Filter** par click karein, `company` par ek filter add karein, taake do companies wala manager ek waqt mein ek ko dekhe.

Dashboard ko kal kholein to numbers current honge — Insights queries live data ke khilaf chalti hain, kisi copy ke khilaf nahi. Dashboard ko wahan rakhein jahan se woh khola jaye: Desktop se ya Selling workspace se link karein.

## Kab istemal karein — aur kab nahi

| Situation | Use |
|---|---|
| "Is mahine hum kaisa kar rahe hain?" | Desk mein Insights dashboard |
| Ek sawal, kayi views | Ek query, kayi charts |
| Ek number jo owner roz check karta hai | Pehli row par Number chart |
| Ek user ke liye ek one-off sawal | Report Builder ya ek saved list filter — dashboard nahi |
| Ek printed document (invoice, gate pass) | Print Format (Lesson 08), Insights nahi |
| Data jo month end par freeze hona chahiye | File mein export ki gayi report — live dashboard badalta rehta hai |

## Common mistakes

- **Dashboards jinhein koi kholta hi nahi.** Teen clicks ki gehrai mein daba hua dashboard sirf decoration hai. Woh ek number jo matter karta hai, wahan rakhein jahan log dekhte hain.
- **Har chart ke liye ek query.** Query ek dafa banayein, use kayi tareeqon se chart karein. Usi logic ki das copies alag-alag ho jati hain.
- **Multi-company dashboard par koi filter nahi.** Har chart saari companies ko mila kar dikhata hai. Company filter add karein.
- **Har sawal ke liye ek chart.** Paanch charts jo ek sawal ka jawab dete hain, jawab ko chhupa dete hain. Ek chart, ek sawal.
- **Workbook ko sab ke saath share karna.** Workbooks ki apni permissions hoti hain — un roles ke saath share karein jo data dekh sakte hain, poori site ke saath nahi.
- **Query check kiye baghair chart par bharosa karna.** Ek ghalat filter ek confident lagne wala ghalat number bana deta hai. Pehle query parhein.

## Next

[19 — Website & Portal](19-website-portal.md) — Frappe ka public side: web pages, Web Forms, aur customer portal.
