# Projects — Tasks, Timesheets, Costing, Profitability

## Ye kya karta hai

Projects "client ke liye ye kaam karo" ko measurable bana deta hai: aik
**Project** jis mein **Tasks** hon, time **Timesheets** par book ho, costs
timesheets, expenses aur purchases se jama hon — aur akhir mein aik profit
number. Is ke baghair, services business apni revenue janta hai aur cost
ka andaza lagata hai. Is ke saath, har project dikhata hai ke us ne paisa
banaya ya gawaya, jabke abhi bhi waqt hai ke use theek kiya ja sake.

## Core DocTypes

| DocType | Ye kya hai |
|---|---|
| Project | Kaam: client, dates, expected dates, costing, billing status. |
| Task | Project mein kaam ka ek hissa, jis ka owner, dates aur dependencies hon. |
| Timesheet | Project / task ke khilaaf book kiya gaya time, billable aur costing rates ke saath. |
| Timesheet Detail | Ek time entry: hours, activity type, billable ya nahi. |
| Activity Type | Kaam ki qisam (Development, Consulting, Support) jis ka costing aur billing rate hota hai. |
| Activity Cost | Har employee ke liye Activity Type ka cost rate. |
| Project Template | Standard kaam ke liye reusable task list (masalan "ERPNext go-live"). |
| Project Type | Grouping aur reporting ke liye category (Internal, External, Support). |
| Project Update | Project par status note, team ke saath share ki jati hai. |

## Shuru se akhir tak flow

```text
Setup:   Activity Types + rates → Project Template for the standard job
Plan:    Project → Tasks (with dependencies) → assign owners
Work:    Timesheet entries against tasks (billable / non-billable)
Cost:    timesheets + Expense Claims + Purchase Invoices roll into the project
Bill:    Timesheet → Sales Invoice (time billed to the client)
Check:   Project Profitability report — revenue vs cost, per project
```

- Ek Task dusre Task par depend kar sakta hai — wo tab tak shuru nahi ho
  sakta jab tak pehla mukammal na ho. Dependencies hi plan ko honest
  banati hain.
- Timesheet entry ke do rates hote hain: **costing rate** (hour ki cost
  kya hai) aur **billing rate** (aap kya charge karte hain). Profit in ke
  darmiyan ka farq hai.
- **Billable** hours client invoice par jate hain; **non-billable** hours
  phir bhi cost hain — wo sirf kamate nahi hain. Sab kuch billable mark
  karna asal margin chhupa deta hai.
- **Project Profitability** report wo aik number hai jo owner check karta
  hai: revenue booked minus cost incurred, har project ke liye.

## Amli misaal — ERPNext implementation, aik project

NexTash Lahore ke aik distributor ke liye ERPNext implementation leta hai:

1. **Project** "Al-Noor ERPNext Go-Live", type External, "ERPNext go-live"
   **Project Template** se: setup → data import → training → go-live,
   dependencies tarteeb se.
2. **Tasks** assign hui: Irfaan (setup, data import), aik colleague
   (training).
3. Har hafte team **Timesheets** book karti hai: 30 hrs Development
   (billable), 6 hrs internal meetings (non-billable).
4. Travel aur aik test server **Expense Claims** aur aik **Purchase
   Invoice** ke tor par project ke khilaaf aate hain.
5. Mahine ke akhir mein, **Sales Invoice** 30 hours agreed rate par bill
   karta hai. Project Profitability report dikhati hai revenue 450,000,
   cost 280,000 — project on track hai, aur 6 non-billable hours nazar aa
   rahe hain, chhupe hue nahi.

## Asli use case

Aik services company mahine ke akhir mein clients ko yaad se bill karti
thi — hours bhool jate thay, aur kisi ko pata nahi tha ke kaun sa client
profitable hai. Projects + Timesheets ke baad, har invoice booked time se
aati hai, aur profitability report ne dikhaya ke aik "bara" client asal
mein loss-making tha jab internal hours count kiye gaye. Unhon ne us
client ko report ko saboot bana kar reprice kiya.

**Hum isay kaise istemal kar sakte hain:** NexTash ka apna client kaam
Projects mein chalao — ye hamara internal tool bhi hai aur demo bhi hai.
Jab client poochhe "aap hamara project kaise track karte hain?", to unhein
live project dikhao: tasks, timesheets, profitability. Ye demo module ko
kisi bhi slide se behtar bechta hai.

## Aam ghaltiyan

- **Timesheets mahine ke akhir mein bharna.** Yaad koi time record nahi
  hai. Time daily book karo, warna billable hours aik andaza hain.
- **Costing rate nahi hai.** Agar sirf billing rate set hai, to project
  profitable lagta hai jab tak salaries count na hon.
- **Sab kuch billable mark karna.** Client ko bill kiya gaya internal
  kaam aik dispute ka intezar hai — aur ye asal cost chhupa deta hai.
- **Tasks jin ka koi owner aur koi dates nahi.** Owners ke baghair task
  list aik wish list hai. Har task ka aik owner aur aik due date honi
  chahiye.
- **Profitability report ko ignore karna.** Report is liye hai ke losing
  project ko jaldi pakra ja sake. Isay hafte mein aik dafa check karo,
  akhir mein nahi.

## Agla

[08 — Assets](08-assets.md) — asset lifecycle, depreciation, maintenance.
