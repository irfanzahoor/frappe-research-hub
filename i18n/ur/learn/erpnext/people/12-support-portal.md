# Support & Portal — Customer Portal, Communication, Portal Users

## Ye kya karta hai

Portal woh jagah hai jahan customers khud apni madad karte hain: wo log in karte hain aur apne orders, invoices, payments aur support tickets dekhte hain — kisi ko email kiye baghair. Aik **Portal User** aik contact hai jisay Customer se linked login diya gaya ho; portal unhain sirf un ke apne documents dikhata hai. Is ke peechay **communication** hai: document par har email, call aur comment us document par record hota hai, is liye aik customer ki poori history aik click ki doori par hoti hai. Portal "mera order kahan hai?" ko support ticket se aik aise page mein badal deta hai jo customer khud khol leta hai.

## Core DocTypes

| DocType | Ye kya hai |
|---|---|
| Portal User | Customer contact ke liye aik login: user, Customer, roles. Customer par woh child table jo portal access deti hai. |
| Customer | Master: portal is customer ke apne orders, invoices aur tickets dikhata hai. |
| Contact | Customer ke paas woh shakhs: email, phone — jab access di jaye to Portal User ban jata hai. |
| HD Customer | Customer ka Helpdesk wala pehlu: un ke tickets ko ERPNext Customer se link karta hai. |
| HD Ticket | Woh cheez jo customer portal mein raise karta hai aur track karta hai. |
| Web Form | Aik public form (lead capture, ticket raising, feedback) jo system mein likhta hai. |
| Website Settings | Portal pages ke peechay site configuration. |
| Issue | Legacy ERPNext support ticket (HD Ticket se replace ho raha hai). |
| Email / Comment | Document par record ki gayi communication — har guftagu ki history. |

## Shuru se akhir tak ka flow

```text
Setup:   Customer → Contact → Portal User (login + roles)
Visit:   customer logs in → sees their Sales Orders, Invoices, Payments
Ask:     customer raises an HD Ticket from the portal
Track:   ticket status visible in the portal; replies by email + portal
Pay:     customer sees outstanding invoices and pays (where configured)
Check:   portal usage, open tickets per customer, ageing receivables
```

- Aik Portal User sirf **apne Customer ke documents** dekhta hai — User Permissions isay enforce karte hain. Aik portal login jo doosray customer ki invoices dekh sakta ho, woh data leak hai; go-live se pehle isay aik asli portal account se test karo.
- Har email aur comment **us document par** store hota hai jis se is ka talluq hai. Jab customer call karta hai, to history un ke Sales Order ya ticket par hoti hai — kisi ko inbox mein dhoondna nahi parta.
- Aik **Web Form** public front door hai: lead form, ticket form, feedback form. Ye seedha system mein likhta hai, is liye kuch dobara type nahi karna parta.
- Aik behtar portal ke liye (custom pages, dashboards, document libraries), isay **Frappe Builder** se banao — website builder jo Frappe stack ke saath aata hai.

## Amli misaal — aik distributor, aik customer

Al-Noor Traders 200 retailers ko supply karta hai. Aik retailer, "Karachi Mart", baar baar call kar ke poochta hai ke us ki delivery kahan hai:

1. Customer par aik **Contact** (store manager) banaya jata hai aur usay **Portal User** login diya jata hai.
2. Wo log in karta hai aur apne **Sales Orders** (kya wada kiya gaya), **Delivery Notes** (kya ship hua, dates ke saath) aur **Sales Invoices** (kitna dena hai) dekhta hai.
3. Aik delivery kam hoti hai. Wo portal se aik **HD Ticket** raise karta hai — ye support queue mein aata hai, us ka Customer pehle se linked hota hai.
4. Agent jawab deta hai; jawab aur ticket status portal mein nazar aate hain. Agli "mera order kahan hai?" wali call kabhi nahi hoti.
5. Mahine ke akhir mein, store manager apni statement khud portal se download kar leta hai — Al-Noor mein kisi ko bhejni nahi parti.

## Asli use case

Aik supplier ki sales team roz aik ghanta "mera order kahan hai?" ka jawab dene aur statements email karne mein guzarti thi. Portal ke baad, customers ne khud orders check kiye, statements self-service ho gayin, aur support queue chhoti ho gayi — team ne woh ghanta bechne mein guzara. Portal aik barray customer ke rukne ki wajah bhi ban gaya: "aap ke competitors har cheez ke liye humein call karne par majboor karte hain."

**Hum isay kaise istemal kar sakte hain:** har B2B implementation mein portal ko self-service add-on ke tor par shamil karo — ye aik chhota setup hai (Portal Users + permissions) jis ka wazeh faida client ke customers mehsoos karte hain. Builder se bana hua custom portal page un clients ke liye fixed-price upsell hai jo standard pages se zyada chahte hain.

## Aam ghaltiyan

- **Permissions test kiye baghair portal access.** Hamesha aik asli portal user ke tor par log in karo aur check karo ke wo sirf apne documents dekhta hai.
- **Ghalat contacts ke liye Portal Users.** Sirf woh log jinhein account dekhna chahiye, login paate hain — account par mojood har email nahi.
- **System ke bahar communication.** WhatsApp par tay honay walay deals jo kabhi record na hon, woh deals hain jo agla shakhs nahi dekh sakta. Isay document par log karo.
- **Portal mein koi ticket form nahi.** Agar customers sirf email kar sakte hain, to portal aik display window hai, channel nahi. Form add karo.
- **Portal ko chhupana.** Aik portal jis ke baaray mein kisi ko bataya hi na jaye, woh portal hai jisay koi istemal nahi karta. Go-live par is ka elan karo, har customer ko logins bhej kar.

## Agla

[13 — Studio, Flow & Insights](../v16/13-studio-flow-insights.md) — Desk mein naye v16 tools.
