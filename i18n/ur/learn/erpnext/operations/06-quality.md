# Quality — Inspections, QC Quarantine / Release / Hold / Reject

## Ye kya karta hai

Quality faisla karta hai ke goods istemal, bechne ya ship karne ke qaabil
hain ya nahi — aur kharab goods ko stock se bahar rakhta hai. Ek
**Quality Inspection** receipt, production batch ya delivery ko ek
**Quality Inspection Template** (parameters ki list, acceptance values ke
saath) ke khilaaf check karta hai. Jo goods fail ho jayein, wo quarantine
warehouse mein jate hain, wapas sellable stock mein nahi. **Quality Goals**,
**Procedures** aur **Reviews** management side hain: targets, likha hua
process, aur regular check ke process kaam kar raha hai ya nahi.

## Core DocTypes

| DocType | Ye kya hai |
|---|---|
| Quality Inspection | Ek inspection: kya check hua, kis template ke khilaaf, pass ya fail. |
| Quality Inspection Template | Checklist: parameters, acceptance values, har item ya item group ke liye. |
| Quality Inspection Parameter | Ek measurable check (moisture %, colour, weight) jis ki value ya range hoti hai. |
| Quality Inspection Reading | Inspection ke dauraan record ki gayi ek measured value. |
| Quality Goal | Ek measurable target (masalan "rejection rate 2% se kam") jis ka owner hota hai. |
| Quality Procedure | Quality activity ke liye likha hua process. |
| Quality Action | Failure se uthaya gaya corrective ya preventive action. |
| Quality Review | Goals, actions aur inspection results ka periodic review. |
| Quality Feedback | Customer ya internal team ki taraf se quality ke baare mein feedback. |
| Quality Meeting | Meeting ka record: agenda, minutes, actions. |

Inspections Stock module mein rehte hain (ye receipts, deliveries aur
production se attach hote hain), jabke goals, procedures aur reviews un
ke gird quality management system hain.

## Shuru se akhir tak flow

```text
Setup:   Quality Inspection Templates per item → quarantine warehouse
In:      Purchase Receipt → Quality Inspection → Accepted / Rejected
Fail:    rejected qty → quarantine warehouse (never into sellable stock)
Fix:     Quality Action (return to supplier, rework, or scrap)
Make:    in-process inspection on the Work Order → out-going inspection
Check:   Quality Inspection report, rejection rate vs Quality Goal
```

- Inspection ek **reference document** se linked hoti hai — aam tor par
  Purchase Receipt, Delivery Note ya Stock Entry. Inspected qty us
  document par accepted ya rejected hoti hai.
- **Accepted** stock normal warehouse mein jata hai. **Rejected** stock
  quarantine warehouse mein jata hai (ya wapas kar diya jata hai). Ye
  kabhi chupke se sellable stock mein add nahi hota.
- **Quality Goal** inspection results ko aik number mein badal deta hai
  jis par owner nazar rakhta hai — rejection rate, on-time inspections,
  complaints per month.
- **Quality Action** wo hai jo failure ke baad hota hai: lot wapas karo,
  rework karo, supplier badlo, ya process badlo. Action ke baghair, wahi
  failure agle mahine dobara hota hai.

## Amli misaal — ek spice manufacturer, ek rejected lot

fmc demo client ([fmc](https://github.com/irfanzahoor/fmc)) ko 500 kg red
chilli milti hai:

1. **Purchase Receipt** — 500 kg aa gaye. Item ka Quality Inspection
   Template hai (moisture ≤ 10%, colour grade A, no stones).
2. **Quality Inspection** — lab moisture 13% measure karta hai. Lot fail
   ho jata hai.
3. 500 kg **quarantine warehouse** mein chale jate hain. 5 kg sample
   supplier dispute ke liye rakha jata hai; baaki istemal ke qaabil nahi
   hai.
4. **Quality Action** — supplier ko wapas karo, aur supplier ki terms mein
   pre-shipment moisture check add karo. Rejected lot kabhi production
   tak nahi pahunchta, is liye koi finished batch contaminate nahi hota.
5. **Quality Goal** "rejection rate 2% se kam" dikhata hai ke ye supplier
   quarter mein 8% par hai — suppliers badalne ka saboot.

## Asli use case

Ek food exporter ne aik container ship kiya jo buyer ne arrival par
moisture ki wajah se reject kar diya — poori shipment zaya ho gayi.
Receipt kabhi inspect nahi hui thi kyunke "supplier trusted hai". Quarantine
warehouse ke saath incoming inspections ke baad, kharab lots gate par hi
pakde jate hain, aur rejection report dikhati hai ke kaun se suppliers
paisa zaya karte hain — container ke sail karne se pehle.

**Hum isay kaise istemal kar sakte hain:** Quality ko har Manufacturing
aur Buying implementation ke saath bundle karo food aur pharma clients ke
liye — Purchase Receipt par incoming inspection aik din ka setup hai jo
client ki sab se mehngi failure (rejected shipment) ko rokta hai. Quality
Goal dashboard phase-2 ki sale hai.

## Aam ghaltiyan

- **Quarantine warehouse nahi hai.** Sellable stock mein mila hua rejected
  stock aik recall ka intezar hai.
- **Istemaal ke baad inspect karna.** Delivery Note par inspection bohat
  der se hoti hai — receipt par inspect karo, material ke production mein
  jaane se pehle.
- **Template jis mein numbers nahi hain.** "Looks fine" koi parameter
  nahi hai. Har check ki acceptance value honi chahiye (moisture ≤ 10%,
  "dry enough" nahi).
- **Failures jin ka koi Quality Action nahi.** Wahi lot agle mahine usi
  supplier se dobara fail hota hai. Action log karo, owner assign karo,
  close karo.
- **In-process inspection skip karna.** Finished pack stage par problem
  pakarna poora batch zaya karta hai — production ke dauraan check karo.

## Agla

[07 — Projects](07-projects.md) — tasks, timesheets, costing.
