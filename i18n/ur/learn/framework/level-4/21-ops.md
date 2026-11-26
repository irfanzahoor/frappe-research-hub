# 21 — Ops

## Yeh kya hai

Ops ek production site ko zinda rakhna hai: backed up, monitored, aur recoverable. Achhe ops ko koi notice nahi karta — us din tak jab disk bhar jaye, scheduler ruk jaye, ya koi site wapas na aaye. Yeh lesson weekly routine aur woh faisle hain (multi-site, Cloud vs self-hosted) jo bure din ko survivable banate hain.

## Minimal working example — weekly ops routine

Yeh har hafte, har production site par chalayein. Tees minute, wahi tarteeb:

```bash
# 1. Backup — database + files, compressed
bench --site mysite.local backup --with-files --compress

# 2. Prove the backup restores (on a spare site, monthly at least)
bench --site spare.local restore <backup.sql> \
  --with-public-files <public.tar> --with-private-files <private.tar>

# 3. Are the workers and scheduler alive?
bench doctor

# 4. Disk space — a full disk stops the database
df -h
```

Phir Desk mein: **Error Log** — har nayi error parhein, sirf unhein count na karein (ek error jo 200 dafa repeat ho, woh ek bug hai, use fix karein); **Email Queue** — draining, stuck nahi; **Background Jobs** — scheduler ne kal raat ke jobs chalaye. v16 mein, offsite backups ek alag app hain (`frappe/offsite_backups`) — use install karein, yeh assume na karein ke backups khud-ba-khud server se bahar chale jate hain. Backup files ko server se bahar rakhein: database wali disk par mojood backup ek copy hai, backup nahi.

## Multi-site benches

Ek bench kayi sites host kar sakta hai — woh apps share karte hain, har ek ka apna database aur files hain:

```bash
bench new-site client2.local
bench --site client2.local install-app erpnext
bench --site client2.local install-app my_app
```

Ise istemal karein: ek client group ke liye ek bench, production ke saath ek staging site, sample data wali ek training site. Sites ke beech kabhi database share na karein, aur production site par kabhi test na karein — ek test site muft hoti hai, production par ek test ek business day ki qeemat rakhta hai.

## Frappe Cloud vs self-hosted

| | Frappe Cloud | Self-hosted |
|---|---|---|
| Who runs the server | Frappe — updates, backups, monitoring included | Aap — OS, bench, backups, monitoring |
| Bench commands | No shell — site dashboard mein version aur settings | Full shell: `bench`, `console`, custom scripts |
| Control | Limited (no custom bench commands, no server access) | Full — koi bhi app, koi bhi integration, koi bhi schedule |
| Scaling | Plan chunein, Frappe use scale karta hai | Aap server ko size aur scale karte hain |
| Cost shape | Per site, per month | Server + aapka time |

Cloud tab chunein jab client bina IT person ke ERP chahta hai, aur standard apps kaafi hon. Self-hosted tab chunein jab aapko shell access, custom bench work, private integrations, ya aisa data chahiye jo client ke apne server par rehna lazmi ho. Kisi bhi surat mein, upar wali ops routine phir bhi apply hoti hai — Cloud backup automate karta hai, yeh check karne ki zaroorat khatam nahi karta ke backup mojood hai aur restore hota hai.

## Kab istemal karein — aur kab nahi

| Situation | Use |
|---|---|
| Ek site live hai | Weekly routine, har hafte, bina exception |
| Usi bench par doosra client | Doosri site, doosra bench nahi |
| Ek test ya training environment | Usi bench par ek alag site |
| "Backup mojood hai" | Restore test — ek backup jo kabhi restore nahi hua, woh backup nahi hai |
| Log mein ek error | Use parhein aur wajah fix karein — log clear na karein |
| Ek client jiske paas koi IT staff nahi | Frappe Cloud, aur aap routine check karte rahein |

## Common mistakes

- **Koi restore test nahi.** Backup file mojood hai, restore fail hota hai. Pata sab se bure din chalta hai.
- **Usi disk par backups.** Disk mar jaye to backup bhi uske saath mar jata hai.
- **Scheduler khamoshi se ruk gaya.** Koi emails nahi, koi notifications nahi, koi auto-reposts nahi — aur ek hafte tak kisi ko pata nahi chalta. `bench doctor` hi woh check hai.
- **Production par testing.** Live site par ek test import ek live import hai. Test site istemal karein.
- **Error Log ko ignore karna.** Errors barhte jate hain. Ek unread error ek bug report hai jo kisi ne file nahi ki.
- **Ek bench, ek site, hamesha.** Usi bench par doosri site muft hai — staging, training, aur agla client sab wahin rehte hain.

## Next

Aapne Framework path mukammal kar liya hai — saare 21 topics, apne pehle bench se lekar ek production site tak jise aap zinda rakh sakte hain.

- **Map review karein:** [Learn: Frappe Framework — Noob to Pro](../README.md)
- **Ise asal modules par istemal karein:** [Learn: ERPNext Modules](../../erpnext/README.md) — saare 14 modules, Accounting se lekar cross-module flows tak
- **Is se asal kaam karein:** [Guides](../../../guides/README.md) — upgrade, go-live, aur woh common mistakes jin se bachna hai
- **Current rahein:** [Research: 2024–2026 mein kya badla](../../../research/history-2024-2026.md) aur [apps catalog](../../../research/apps-catalog.md) — hub ecosystem ke saath barhta hai

Path mukammal hai. Seekhna nahi — agli production site woh jagah hai jahan yeh lessons apni qeemat sabit karte hain.
