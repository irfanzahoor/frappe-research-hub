# Assets — Lifecycle, Depreciation, Maintenance

## Ye kya karta hai

Assets un cheezon ko track karta hai jo business ke paas hain aur aik saal
se zyada chalti hain — machines, vehicles, computers, furniture — purchase
se disposal tak. Ek **Asset** Purchase Invoice se banta hai, schedule par
depreciate hota hai taake books us ki girti hui value dikhayein, plan par
maintain hota hai taake wo kharab na ho, locations ke darmiyan move hota
hai taake wo gum na ho, aur akhir mein scrap ya sell ho jata hai. Is ke
baghair, business ke paas cheezein hoti hain jinhein wo dhoond nahi sakta
aur wo cheezein depreciate karta hai jo us ke paas ab hain hi nahi.

## Core DocTypes

| DocType | Ye kya hai |
|---|---|
| Asset | Ek owned item: value, location, custodian, status, depreciation schedule. |
| Asset Category | Group (Plant & Machinery, Vehicles, IT Equipment) jis ke accounts aur depreciation defaults hon. |
| Asset Depreciation Schedule | Har finance book ke liye depreciation plan: method, rate, dates, amounts. |
| Asset Maintenance | Asset ka maintenance plan: tasks aur un ki frequency. |
| Asset Maintenance Task | Maintenance plan mein aik recurring task (oil change har 3 mahine mein). |
| Asset Maintenance Log | Aik completed maintenance event, cost ke saath. |
| Asset Movement | Asset ko locations ya custodians ke darmiyan move karna. |
| Asset Repair | Aik repair job: kya kharab hua, kitni cost aayi, kab theek hua. |
| Asset Value Adjustment | Asset ki value upar ya neeche karna (revaluation ya impairment). |
| Asset Capitalization | Stock items ya services ko asset mein capitalise karna (masalan parts se machine banana). |
| Location | Assets kahan rehte hain: aik tree (Factory → Hall A → Line 1). |

## Shuru se akhir tak flow

```text
Setup:   Asset Categories (accounts + method) → Locations
Buy:     Purchase Invoice → Asset created (or capitalised from stock)
Value:   Asset Depreciation Schedule runs → depreciation posts to the ledger
Use:     Asset Movement when it changes location or custodian
Care:    Asset Maintenance plan → Asset Maintenance Log per visit
Fix:     Asset Repair when it breaks
End:     sell or scrap → Asset Value Adjustment / disposal, ledger updated
Check:   Fixed Asset Register, Asset Depreciation report
```

- Depreciation methods: **Straight Line** (har period mein same amount),
  **Written Down Value** (baqi value ka aik %), **Double Declining
  Balance**, ya **Manual**. Har category ke liye choose karo, har asset
  ke liye nahi, aur isay mid-life mein change mat karo.
- **Fixed Asset Register** "hamare paas kya hai?" ka audit jawab hai:
  har asset, us ki location, us ka custodian, us ki book value.
- **Asset Movement** wo control hai jo assets ko chale jaane se rokta
  hai — Movement entry ke baghair move ki gayi machine wo machine hai
  jise register dhoond nahi sakta.

## Amli misaal — aik factory, aik machine

Aik spice factory Rs 1,200,000 ka grinder khareedti hai:

1. **Purchase Invoice** — grinder book ho gaya. Is se aik **Asset** bana,
   category "Plant & Machinery", location "Factory → Hall A",
   custodian production supervisor.
2. **Asset Depreciation Schedule** — Straight Line, 10% per year, 10 saal.
   Har mahine Rs 10,000 depreciation automatically ledger mein post
   hoti hai.
3. **Asset Maintenance** — oil change har 3 mahine mein, belt check har
   6 mahine mein. Har visit **Asset Maintenance Log** mein cost ke saath
   log hoti hai.
4. Saal 3 mein, motor jal jata hai. **Asset Repair** — Rs 85,000, do din
   downtime. Repair cost asset ke khilaaf nazar aati hai, general
   expenses mein chhupi hui nahi.
5. Saal 8 mein, grinder Rs 300,000 mein bech diya jata hai. Book value Rs
   240,000 hai — disposal par Rs 60,000 ka gain book hota hai, aur asset
   register se nikal jata hai.

## Asli use case

Aik manufacturer ke paas do halls mein 40 machines thi aur koi register
nahi tha. Jab auditor ne fixed asset list maangi, to accountant ne purani
invoices se andaza lagaya — jin mein wo machines bhi thi jo saalon pehle
bech di gayi thi. Assets ke baad, Fixed Asset Register floor se match
karta tha, depreciation manual journals ke baghair har mahine post hoti
thi, aur maintenance log dikhata tha ke kis machine ki repairs par sab
se zyada kharcha aaya — use replace karne ka case.

**Hum isay kaise istemal kar sakte hain:** Fixed Asset Register ko har
manufacturing implementation mein audit-ready deliverable ke tor par offer
karo — auditors isay naam se maangte hain, aur jis client ke paas ye hai
wo wapas nahi jayega. Maintenance plans un clients ke liye phase-2 ki
sale hain jin ke paas plant and machinery hai.

## Aam ghaltiyan

- **Assets expenses ke tor par book karna.** "General Expense" mein Rs
  1,200,000 ki machine balance sheet aur tax return kharab kar deti hai.
  Isay capitalise karo.
- **Depreciation manual journals se.** Mahine ke manual journals drift
  karte hain aur bhool jate hain. Schedule istemal karo — wo khud post
  hota hai.
- **Koi Location ya custodian nahi.** Jis asset ki koi location nahi, wo
  asset dhoonda nahi ja sakta. Dono creation par set karo.
- **Repairs expenses mein chhupi hui.** Agar repair cost asset par nahi
  hai, to aap dekh nahi sakte ke kaun si machine paisa kha rahi hai.
- **Mid-life mein depreciation method badalna.** Ye book value ki history
  dobara likh deta hai. Setup par decide karo, har category ke liye.

## Agla

[09 — HR](../people/09-hr.md) — employees, leave, payroll, attendance.
