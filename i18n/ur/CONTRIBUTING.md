# Contributing

Khush amdeed! Yeh hub public hai taake koi bhi is se Frappe aur
ERPNext seekh sake — aur koi bhi is ko behtar banane mein madad kar
sakta hai. Chhoti fixes bhi utni hi welcome hain jitni bari nayi
lessons. Pehle permission lene ki zaroorat nahi: issue ya pull
request kholein, aur owner merge se pehle is ko review kare ga.

> **Sab se ahem aik rule:** changes sirf fork → branch → pull
> request se aate hain, owner ki review ke saath. Koi bhi seedha
> `main` par push nahi karta, aur koi bhi published release ko
> edit nahi karta.

## Contribute karne ke tareeqe

- **Typo ya broken link fix karein** — sab se chhota, sab se useful PR.
- **Nayi lesson suggest karein** — pehle lesson-request template se
  aik issue kholein, taake likhne se pehle topic par agree ho jaye.
- **Troubleshooting entry add karein** — aik asal error,
  `guides/troubleshooting.md` wale format mein: exact error → kab
  hota hai → kyun → fix, tartib se → prevention.
- **Case study add karein** — aik asal project jis par aap ne kaam
  kiya ho, anonymised: na client ka naam, na company ka naam,
  na quotes, na measured numbers. Sirf approximate numbers, aur
  yeh likh dein ke approximate hain.
- **Catalog mein nayi app add karein** — sahi category file mein
  `research/apps-catalog/` ke neeche aik entry: GitHub link, install
  command, aur aik line ke hum isay kaise istemal kar sakte hain.
- **Lesson behtar karein** — aik zyada clear example, aik missing
  common mistake, aik command jo nayi version mein badal gaya ho.

## Contribute kaise karein (PR flow)

1. **Fork** karein, phir branch banayein: `fix/typo-lesson-05`
   ya `add/lesson-frappe-mail`.
2. **Change DONO languages mein karein** — English aur Roman Urdu,
   wahi structure, wahi headings. Aik content PR jis mein sirf aik
   language ho, merge nahi ho sakta. (Roman Urdu rules neeche dekhein.)
3. **Docs site locally build karein** aur check karein ke aap ka page
   render hota hai:
   `sh scripts/sync-docs.sh && .venv-docs/bin/mkdocs build --clean`
   (ya browser mein preview ke liye `mkdocs serve`).
4. **Pull request kholein** — chhoti description ke saath ke kya
   badla aur kyun. PR template mein checklist hai — is ko honestly
   tick karein.
5. Owner review kare ga, zaroorat par changes mange ga, aur merge
   kare ga.

## Content rules

- **Lesson format** — har lesson wahi shape follow karta hai: yeh kya
  hai, real code ya commands ke saath aik minimal working example,
  kab use karna hai — aur kab nahi — common mistakes, aur aik Next link.
- **Har claim ke liye source chahiye** — official docs, Frappe
  Blog/Forum, GitHub release, ya aik tested example. Source link karein.
- **Kabhi woh version promise na karein jo aap ne test nahi kiya.**
- **Likhne se pehle facts verify karein** — DocType ya field ko Frappe
  source ya docs mein check karein, memory se nahi. (Example: Contact
  DocType mein `user` aur `links` Dynamic Link child table hai —
  Contact par koi `customer` field nahi hai.)
- **No invented names, quotes, ya numbers.** Agar number approximate
  hai, to yeh likh dein.
- **Entries chhoti rakhein** — kya, kab, kaise use karna hai, source link.
- **Aik file mein aik topic, pehle beginner.**

### Roman Urdu rules

- Urdu version mein **0 Devanagari / Arabic-script characters**.
  Sirf Roman Urdu — Latin letters mein likhi hui Urdu.
- Code, commands, DocType aur field names, URLs aur app names
  **English** mein rehte hain.
- "How we can use it" wali line hamesha
  **"Hum isay kaise istemal kar sakte hain"** hoti hai.
- English file wali headings aur structure, wahi tartib mein.

## Kya change NA karein

- Files delete na karein, published releases rewrite na karein, ya
  released versions ke CHANGELOG history entries edit na karein.
- Repo settings, topics, `mkdocs.yml`, ya `.github/workflows/` ke
  neeche kuch bhi change na karein — agar lagta hai ke wahan kuch
  badalna chahiye, to pehle issue kholein.
- Bina issue mein discuss kiye naya top-level section ya nayi guide
  add na karein.

## Sawal hain?

Issue kholein — templates (lesson request, bug report, new app) aap
ki guidance ke liye hain. Agar samajh na aaye ke kaun sa template
fit hota hai, to qareeb tareen wala lein aur text mein likh dein.
