# HR — Frappe / ERPNext Apps

> [Apps Catalog](../apps-catalog.md) ka hissa — is category mein 2 apps hain. Har app mukhtasar hai: ye kya karta hai, kyun faida-mand hai, NexTash ke kaam ke liye ek **Hum isay kaise istemal kar sakte hain** line, aur GitHub link + install command. Pehle staging par test karein.


**Baseline:** **Frappe HR / HRMS** (official) — https://github.com/frappe/hrms, `bench get-app hrms` — employee lifecycle, leave, attendance, expense claims, performance, payroll, recruitment; free GPL-3.0, v14–v16. **Hum isay kaise istemal kar sakte hain:** HRMS ko un clients ko standalone add-on ke tor par bechein jo ERPNext bina HR ke chala rahe hain; `/hrms` par ESS PWA shift workers wali factories ke liye mobile attendance pitch hai.

### Discipline HR — attendance discipline & automated payroll penalties
- **What/why:** late attendance par grace periods aur automatic payroll deductions — woh rules jo har HR client mangta hai lekin HRMS mein nahi hain.
- **Hum isay kaise istemal kar sakte hain:** shift workers wali factories ko offer karein jahan late-coming roz ka HR headache hai — ye woh manual spreadsheet replace kar deta hai jo HR head aaj maintain karta hai.
- **GitHub:** https://github.com/cre8tivMaxx/discipline_hr — `bench get-app https://github.com/cre8tivMaxx/discipline_hr`

### Biometric Attendance Sync Tool — ZKTeco fingerprint devices → ERPNext (official Frappe)
- **What/why:** biometric devices ko poll karta hai aur punches ko Employee Checkin records mein sync karta hai — manual CSV imports ki zaroorat nahi.
- **Hum isay kaise istemal kar sakte hain:** har HRMS proposal mein shamil karein un factories/offices ke liye jin ke paas pehle se ZKTeco machines hain — punches auto-attendance mein flow karte hain, ek quick win jo HR sale ko asaan bana deta hai.
- **GitHub:** https://github.com/frappe/biometric-attendance-sync-tool — not a bench app; clone and run the Python sync scripts: `git clone https://github.com/frappe/biometric-attendance-sync-tool.git`

---
