# Helpdesk — Tickets, SLAs, Support Workflow

## Ye kya karta hai

Helpdesk support ki afra-tafri ko aik queue bana deta hai: har request aik **HD Ticket** ban jati hai jis mein type, priority, owner aur aik clock hoti hai. Clock hai **Service Level Agreement** — first response aur resolution targets jin ke khilaf team ko naapa jata hai. Tickets email, customer portal ya form se aate hain; agents aik team mein un par kaam karte hain; aur knowledge base (**HD Article**) sawal ka jawab ticket banne se pehle hi de deta hai. Frappe Helpdesk aik alag app hai (`bench get-app helpdesk`), November 2026 mein v16.x par renumber hua — unlimited agents, koi per-seat fee nahi.

## Core DocTypes

| DocType | Ye kya hai |
|---|---|
| HD Ticket | Aik request: customer, subject, type, priority, status, agent, SLA. |
| HD Agent | Aik support agent: jisay tickets assign kiye ja sakte hain. |
| HD Team | Agents ka aik group (masalan "ERP Support", "Billing"). |
| HD Service Level Agreement | Har priority aur customer ke liye response aur resolution targets. |
| HD Service Level Priority | SLA ke andar aik priority ke targets (masalan Urgent: 1 hr response). |
| HD Ticket Type | Request ki qism: Bug, Question, Feature Request. |
| HD Ticket Priority | Urgent, High, Medium, Low. |
| HD Ticket Status | Open, Replied, Resolved, Closed. |
| HD Customer | Helpdesk mein aik customer, jo un ke ERPNext Customer se linked hai. |
| HD Article | Knowledge base ka aik article, aik category mein. |
| HD Article Category | Knowledge base ka aik hissa (Getting Started, Billing). |
| HD Saved Reply | Aik aam jawab ke liye tayyar-shuda response. |
| HD Ticket Template | Ticket raise karne ke liye aik form template (har type ke liye fields). |

## Shuru se akhir tak ka flow

```text
Raise:    email / portal / form → HD Ticket (auto-created, type + priority set)
Assign:   ticket → HD Team → HD Agent (round-robin or manual)
Work:     agent replies, ticket moves Open → Replied → Resolved
Clock:    SLA measures first response and resolution against targets
Close:    customer confirms → Closed; feedback requested
Learn:    repeated questions → HD Article → fewer tickets next month
Check:   ticket ageing, SLA breach, first-response time reports
```

- Aik ticket ka **aik waqt mein aik hi owner** hota hai. Aik ticket jisay assign nahi kiya gaya, woh ticket hai jis par koi kaam nahi kar raha — queue view isay wazeh kar deta hai.
- **SLA clock** us waqt shuru hoti hai jab ticket banaya jata hai aur ruk jati hai jab agent customer ka intezar karta hai. Breaches woh report hain jo support lead har subah check karta hai.
- **HD Article** sab se sasti support hai: har sawal ka aik dafa knowledge base mein jawab de diya jaye, to woh ticket kabhi nahi aata.
- Aik **Saved Reply** jawabon ko consistent rakhta hai — aik hi sawal ka aik hi sahi jawab milta hai, chahe shift par koi bhi ho.

## Amli misaal — NexTash support, aik hafta

Aik client ki user Purchase Receipt post nahi kar sakti:

1. Wo support ko email karti hai. Aik **HD Ticket** khud-ba-khud ban jata hai: type Question, priority High, customer un ke ERPNext Customer se linked.
2. Ticket **"ERP Support" team** ki queue mein aata hai aur aik agent ko assign ho jata hai. SLA kehta hai pehla response 4 hours ke andar.
3. Agent wajah dhoond leta hai — Purchase Receipt DocType par aik missing permission — aur fix ke saath jawab deta hai. Status → Replied.
4. Client confirm karta hai ke kaam ho gaya. Status → Resolved → Closed.
5. Wohi sawal doosray client se aata hai. Agent aik **HD Article** likhta hai ("Why you cannot submit a Purchase Receipt") aur aik **Saved Reply** jo us ki taraf ishara karta hai. Teesri dafa, jawab mein 30 seconds lagte hain.

## Asli use case

Aik software company shared inbox se support chalati thi. Aik hi sawal ke paanch mukhtalif tareeqon se jawab diye jate thay, urgent requests routine wali requests ke peechay pari rehti theen, aur kisi ko nahi pata tha ke kitne tickets khule hue hain. Helpdesk ke baad, queue ne asli workload dikhaya, SLA report ne dikhaya ke first-response time aik din se gir kar do ghantay ho gaya, aur knowledge base ne repeat tickets aik tihai kam kar diye.

**Hum isay kaise istemal kar sakte hain:** NexTash ki apni client support Helpdesk par chalao — ye demo aur tool aik saath hai. Phir ye har us client ko becho jis ki support shared inbox ya WhatsApp par chalti hai: SLA report hi pitch hai ("aap ke customers ko pata hoga ke aap dinon mein nahi, ghanton mein jawab dete hain"), aur knowledge base phase-2 ki sale hai.

## Aam ghaltiyan

- **Koi SLA nahi.** Targets ke baghair, "urgent" aik raay hai aur response time wohi hai jo ho gaya. SLA pehle din set karo.
- **Tickets jin ka koi owner nahi.** Queue mein unassigned tickets numayan nazar aane chahiye — warna wo sar jate hain.
- **Confirm kiye baghair resolve karna.** Aik ticket jo customer ki tasdeeq se pehle band kar diya jaye, woh ticket hai jo zyada gusse ke saath dobara khul jata hai.
- **Koi knowledge base nahi.** Aik hi sawal ka das dafa jawab dena das tickets hain jinay aik article rok sakta tha.
- **Shared inbox mein support.** Email mein na queue hai, na owner, na clock. Yehi woh cheez hai jisay Helpdesk replace karta hai.

## Agla

[12 — Support & Portal](12-support-portal.md) — customer portal, communication, portal users.
