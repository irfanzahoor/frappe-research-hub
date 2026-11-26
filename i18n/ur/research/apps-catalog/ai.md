# AI Tools — Frappe / ERPNext Apps

> [Apps Catalog](../apps-catalog.md) ka hissa — is category mein 8 apps hain. Har app mukhtasar hai: ye kya karta hai, kyun faida-mand hai, NexTash ke kaam ke liye ek **Hum isay kaise istemal kar sakte hain** line, aur GitHub link + install command. Pehle staging par test karein.


### ERPSmith — AI dev copilot for ERPNext (MCP)
- **What/why:** Claude (ya kisi bhi MCP client) ko aapki site par customizations banane aur debug karne deta hai, har change user ki approval se hota hai — haath se likha hua boilerplate kam ho jata hai.
- **Hum isay kaise istemal kar sakte hain:** client projects par DocType aur script ka kaam Claude se karwayein, approval gate hamara review step ban jaye; "AI-assisted customization" ko ek tez fixed-price service ke tor par offer karein.
- **GitHub:** https://github.com/abhinavprakash1992/erpsmith — `bench get-app https://github.com/abhinavprakash1992/erpsmith` (Frappe v15/v16, free MIT)

### Ask ALYF — in-Desk AI assistant
- **What/why:** users Desk ke andar hi sawal pooch kar documents mein madad le sakte hain, har "kahan hai…" wale sawal par support ticket banane ki zaroorat nahi.
- **Hum isay kaise istemal kar sakte hain:** pehli dafa ERP use karne wale clients ke handover package mein shamil karein — is se hamare post-go-live support tickets kam ho jayenge.
- **GitHub:** https://github.com/alyf-de/ask_alyf — `bench get-app https://github.com/alyf-de/ask_alyf`

### ERPNext Copilot — plain-English queries, actions, charts, scheduled reports
- **What/why:** managers sada English mein data pooch sakte hain, charts aur scheduled reports le sakte hain — na SQL, na har report ke liye developer.
- **Hum isay kaise istemal kar sakte hain:** un owners aur finance heads ko bechein jo har hafte "bas ek aur report" mangte hain; go-live ke foran baad phase-2 add-on, jab report ki requests peak par hoti hain.
- **GitHub:** https://github.com/byt3crafter/erpnext-copilot — `bench get-app https://github.com/byt3crafter/erpnext-copilot`

### NextAssist — multi-provider AI chat assistant
- **What/why:** AI chat assistant jo OpenAI, Claude ya Gemini par chalta hai (client pehle se jis ki payment karta ho), sandboxed code runner ke saath.
- **Hum isay kaise istemal kar sakte hain:** un clients ko propose karein jo pehle se ChatGPT/Claude ki payment karte hain aur poochte hain "kya AI hamara ERP data use kar sakta hai?" — koi naya vendor bechne ki zaroorat nahi.
- **GitHub:** https://github.com/navdeepghai/nextassist — `bench get-app https://github.com/navdeepghai/nextassist`

### Frappe Crema — LLM toolkit for Frappe (OCR + NL list views + scheduled AI tasks)
- **What/why:** ek hi toolkit — OCR/document extraction se records banana, natural-language list views aur edits, aur scheduled AI tasks.
- **Hum isay kaise istemal kar sakte hain:** client sites par isay hamara standard AI toolkit banayein — supplier bills OCR se andar, sada zuban mein list edits, raat ko draft reports — har client ke liye alag AI app seekhne ki bajaye ek hi toolkit seekhna hai.
- **GitHub:** https://github.com/amsys/crema — `bench get-app https://github.com/amsys/crema`

### HUF AI — open-source AI infrastructure for any Frappe app
- **What/why:** bespoke AI features banane ke liye reusable multi-agent / AI-workflow layer, one-off scripts ki bajaye.
- **Hum isay kaise istemal kar sakte hain:** HUF par custom AI workflows banayein (support emails ki auto-triage, routine POs ki approval) one-off scripts ki bajaye — kaam repeatable ho jata hai aur productised service ke tor par bill ho sakta hai.
- **GitHub:** https://github.com/tridz-dev/huf — `bench get-app https://github.com/tridz-dev/huf`

### Frappe MCP — turn Frappe apps into MCP servers (official Frappe)
- **What/why:** kisi bhi Frappe app ko AI agents (Claude waghera) ke samne controlled tareeqe se expose karne ka official building block.
- **Hum isay kaise istemal kar sakte hain:** client ki custom app ko Claude/ChatGPT ke samne expose karne ka standard tareeqa — official Frappe code hai, is liye propose karne ke liye safe choice hai.
- **GitHub:** https://github.com/frappe/mcp — `bench get-app https://github.com/frappe/mcp`

### MCP ERPNext — MCP server with 97 tools (Casys-AI)
- **What/why:** agents ko ERPNext se connect karne ke liye sab se bara ready-made tool surface (97 tools, 11 categories), npx se zero-config.
- **Hum isay kaise istemal kar sakte hain:** pehli meeting mein clients ko quick AI-agent demos ke liye use karein ("apne live stock ke bare mein Claude se poochein"); production ke liye unhein official Frappe MCP route par le jayein.
- **GitHub:** https://github.com/Casys-AI/mcp-erpnext — not a bench app; MCP server via npx.

---
