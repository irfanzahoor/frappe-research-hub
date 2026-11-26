# CRM — Leads, Deals, Web Forms (Frappe CRM)

## Ye kya karta hai

CRM ajnabi logon ko customer bana deta hai: aik **Lead** capture karo, usay qualify karo, usay stages se guzar kar aik **Deal** ke tor par kaam karo, aur phir close kar do. **Frappe CRM istemal karo — alag app — ERPNext ke andar wala legacy CRM nahi.** Legacy module (ERPNext core mein Lead, Opportunity) ko deprecate karne ka faisla ho chuka hai aur version 17 mein ye poori tarah hata diya jayega, aur Frappe CRM wohi jagah hai jahan tamam nayi development ho rahi hai: lead capture ke liye web forms, deal pipelines, enrichment, aur workflow automations. November 2026 mein isay Framework scheme ke mutabiq renumber kiya gaya (v16.x, Frappe v16 ko target karta hai) aur ye ~2,500 paid sites par chal raha hai.

## Core DocTypes

| DocType | Ye kya hai |
|---|---|
| CRM Lead | Aik prospect: naam, contact, source, status. Funnel ka sab se upar wala hissa. |
| CRM Deal | Aik opportunity: value, stage, probability, expected close date. |
| CRM Organization | Woh company jis se lead ya deal ka talluq hai. |
| CRM Task | Aik follow-up: call, visit, quote bhejna — due date aur owner ke saath. |
| CRM Call Log | Aik call: kis se, kab, kya kaha gaya, agla step kya hai. |
| FCRM Note | Lead ya deal par aik note. |
| CRM Lead Status / CRM Deal Status | Pipeline stages (New, Contacted, Qualified, Won, Lost). |
| CRM Service Level Agreement | Leads ke liye response-time targets (pehla reply X hours ke andar). |
| CRM Form Script | CRM ke web forms ke liye scripting (validation, defaults). |

Isay `bench get-app crm` se install karo — ye aik alag app hai, ERPNext core ka hissa nahi. Website par capture honay walay leads CRM ke web forms se aate hain; aik lead tab deal ban jata hai jab wo qualify ho jaye, aur aik deal tab ERPNext mein Customer + Quotation ban jata hai jab wo won ho jaye.

## Shuru se akhir tak ka flow

```text
Capture:  web form / email / manual → CRM Lead
Qualify:  Lead → contact, understand the need → convert to CRM Deal
Work:     CRM Deal through stages → CRM Task + CRM Call Log per step
Close:    Won → Customer + Quotation in ERPNext → Sales Order
Lose:     Lost → CRM Lost Reason recorded (the data that fixes the funnel)
Check:   CRM dashboard — pipeline value, conversion rate, ageing deals
```

- Aik **Lead** ghair-qualify shuda dilchaspi hai; aik **Deal** aik qualify shuda opportunity hai jis ki value hoti hai. Bohat jaldi convert karne se pipeline mein shor bhar jata hai; bohat der se convert karne ka matlab hai ke koi follow-up nahi karta.
- Har deal ko aik **next step** chahiye — aik CRM Task, date aur owner ke saath. Aik deal jis ka koi next step nahi, woh deal hai jo chup chap mar jati hai.
- **Lost Reason** CRM ka sab se qeemti field hai. Lagatar das dafa "Too expensive" ka matlab pricing ka masla hai, sales ka masla nahi.
- CRM ka apna **Service Level Agreement** hai: muqarar waqt ke andar pehla response. Jin leads ka jawab der se diya jaye, wo leads competitor ke paas chale jate hain.

## Amli misaal — NexTash, aik lead se aik project tak

Aik food manufacturer NexTash ki site par "Get a quote" form bharta hai:

1. Web form se **CRM Lead** khud-ba-khud ban jata hai: company, contact, "ERPNext for spice factory", source Website.
2. Irfaan usi din call karta hai. **CRM Call Log**: "wants Manufacturing + Quality, 40 users, currently on Excel". Lead status → Qualified.
3. **CRM Deal** ban jata hai: value Rs 1,800,000, stage "Proposal", close date aglay mahine. **CRM Tasks**: proposal bhejna (Tue), follow-up call (Fri).
4. Client maan jata hai. Deal → Won. ERPNext mein aik **Customer** aur **Quotation** ban jate hain, aur kaam aik **Project** ke tor par shuru ho jata hai (lesson 07 dekhein).
5. Dashboard funnel dikhata hai: is mahine 12 leads, 5 qualified, 2 won — aur haaray hue deals kehte hain "no budget this quarter", jo aglay quarter ke liye follow-up list hai, dead end nahi.

## Asli use case

Aik distributor ki sales team leads ko apni personal WhatsApp chats mein rakhti thi. Jab aik salesperson chala jata, to leads bhi us ke saath chale jate. Frappe CRM ke baad, har lead system mein hai, owner aur next step ke saath, manager poori pipeline aik dashboard mein dekhta hai, aur aik lead jis ka 24 hours mein jawab nahi diya gaya, nazar aa jata hai — aik mahine baad pata nahi chalta.

**Hum isay kaise istemal kar sakte hain:** pehle NexTash ki apni pipeline ke liye Frappe CRM istemal karo — ye woh demo hai jis se har sales call shuru hoti hai. Phir ye har us client ko becho jis ki sales WhatsApp aur yaad-dasht par chalti hai: unlimited agents, koi per-seat fee nahi, aur web form un ki website ko lead machine bana deta hai. Naye projects par hamesha Frappe CRM install karo; kisi client ko legacy ERPNext CRM par kabhi shuru na karo.

## Aam ghaltiyan

- **Legacy ERPNext CRM istemal karna.** Ye v17 mein hata diya jayega. Nayi implementations Frappe CRM par hongi, bas.
- **Leads jin ka koi owner aur koi next step nahi.** Aik lead jis ka koi owner nahi, woh khoya hua lead hai. Har lead ko usi din aik owner chahiye jis din wo aaye.
- **Koi Lost Reason nahi.** Aik haara hua deal baghair wajah ke kuch nahi sikhata. Har dafa isay record karo.
- **Deals jo hafton tak aik hi stage par atke hon.** Aik purana deal aik mara hua deal hai jis ka stage khula reh gaya hai. Pipeline ko haftawar review karo aur close karo ya dobara date do.
- **Koi web form nahi.** Agar leads sirf phone se aate hain, to website kuch nahi kar rahi. Form aik ghantay ka setup hai.

## Agla

[11 — Helpdesk](11-helpdesk.md) — tickets, SLAs, support workflow.
