# 10 — Workflows & Assignments

## Yeh kya hai

Ek **Workflow** ek document ke liye state machine hai: kaun isay ek stage
se agle stage par le ja sakta hai, aur kis shart par. Ek **Assignment Rule**
document ko khud-ba-khud ek shakhs tak route karta hai — round robin, least
busy, ya document par mojood ek field se. Dono mil kar jawab dete hain:
*isay kaun approve karta hai, aur yeh kis ki desk par jata hai?*

Ek Workflow sirf ek **submittable** DocType (`is_submittable`) par kaam
karta hai — yeh `docstatus` ko drive karta hai (0 Draft, 1 Submitted,
2 Cancelled), is liye drive karne ke liye ek submitted state honi chahiye.
Jab aap Workflow activate karte hain, Frappe aap ke liye DocType par
`workflow_state` field bana deta hai — state ko custom Select field se
drive na karein.

## Minimal working example — Quality Inspection approval

Ek spice batch aaya hai. Batch istemal hone se pehle inspection ko QA
Manager se approve karwana lazmi hai. Desk → **Workflow** → New, Document
Type: **Quality Inspection**, Is Active ✓.

**States** — har state ka ek docstatus hota hai:

| State | Doc Status | Kaun edit kar sakta hai |
|---|---|---|
| Draft | 0 | Quality User |
| Pending Approval | 0 | — |
| Approved | 1 | — |
| Rejected | 0 | Quality User |

**Transitions** — har ek: ek state se, ek action, ek state tak, ek role,
ek optional condition:

| From | Action | To | Allowed | Condition |
|---|---|---|---|---|
| Draft | Submit for Approval | Pending Approval | Quality User | |
| Pending Approval | Approve | Approved | Quality Manager | |
| Pending Approval | Reject | Rejected | Quality Manager | |
| Rejected | Revise | Draft | Quality User | |

Do rules jo asal projects ko bachate hain:

- **Intermediate approval states docstatus 0 par rehti hain.** Sirf aakhri
  "Approved" state 1 hoti hai. Ek submitted document draft mein wapas nahi
  ja sakta — docstatus sirf aage barhta hai (0→0, 0→1, 1→1, 1→2).
- **Rejected docstatus 0 hoti hai**, is liye isay theek karke dobara submit
  kiya ja sakta hai. Ek rejected inspection jo docstatus 1 ya 2 par ho, woh
  phans jati hai.

**Allow Self Approval = 0** set karein jab creator ko apna khud ka document
approve nahi karna chahiye. Ek DocType par sirf **ek** Workflow active ho
sakta hai. Conditions document par Python expressions hote hain:
`doc.grand_total > 100000`, `doc.inspection_type == "Incoming"`.

Code mein transition lagayein — `workflow_state` ko kabhi seedha set na
karein:

```python
from frappe.model.workflow import apply_workflow, get_transitions

apply_workflow(doc, "Approve")   # respects roles and conditions
get_transitions(doc)              # actions available to the current user
```

## Minimal working example — inspections ko QA team tak route karein

Desk → **Assignment Rule** → New, Document Type: **Quality Inspection**:

| Field | Value |
|---|---|
| Assign Condition | `doc.inspection_type == "Incoming"` |
| Rule | Round Robin |
| Users | qa.ahmed@…, qa.sana@…, qa.bilal@… |
| Priority | 1 |
| Assignment Days | Mon–Fri |

**Round Robin** users ke darmiyan tarteeb se cycle karta hai. **Load
Balancing** document usay deta hai jis ke paas sab se kam open assignments
hon — support tickets ke liye sahi choice. **Based on Field** document se
khud ek User link field parhta hai (masalan, har factory ka designated
auditor). Sab se zyada Priority wala rule jo match kare, woh jeet ta hai.
`Unassign Condition` assignment ko release kar deta hai (masalan, jab
document cancel ho jaye); `Close Condition` ToDo ko band kar deta hai jab
kaam mukammal ho jaye.

## Kab istemal karein — aur kab nahi

| Situation | Use |
|---|---|
| "Isay kaun approve kar sakta hai, aur kis tarteeb mein?" | Workflow |
| "Yeh kis ki desk par jata hai?" | Assignment Rule |
| Ek rule jo document ko pass karna lazmi hai (dates, quantities, limits) | Controller `validate` / `before_submit` — Workflow condition nahi |
| Ek document jo kabhi submit nahi hota | Koi Workflow nahi — workflows ko submittable DocType chahiye |
| Email se ek baar ki approval | Document share karein + ek comment — poora Workflow nahi |
| Team, territory, ya workload ke hisab se routing | Assignment Rule, Workflow state nahi |

## Aam ghaltiyan

- **Intermediate state docstatus 1 par.** Document approval ke aadhe
  raste mein submit ho jata hai aur kabhi draft mein wapas nahi ja sakta.
  Approvals aakhri state tak 0 par rehti hain.
- **`doc.workflow_state` ko seedha set karna** taake approval skip ho
  jaye. `apply_workflow` istemal karein — yeh roles, conditions, aur
  self-approval ko check karta hai.
- **Workflow-controlled document par `doc.submit()` call karna.** Workflow
  khud submit karta hai, jab aakhri transition chalta hai.
- **State ko custom Select field se drive karna.** Workflow State field
  (`workflow_state`) istemal karein — engine wohi parhta hai.
- **Koi state nahi jis ka docstatus 0 ho.** Naye documents wahin se shuru
  hote hain. Is ke baghair kuch create nahi ho sakta.
- **Ek Assignment Rule jis mein koi users nahi, ya condition jo kabhi match
  nahi karti.** Rule ko ek asal document se test karein — ek unmatched rule
  khamoshi se kuch nahi karta.
- **Ek DocType par do active workflows.** Sirf ek active ho sakta hai;
  doosri activation pehli ko deactivate kar deti hai.
- **Transition condition mein business validation.** Conditions yeh tay
  karti hain ke *kaun act kar sakta hai*; validation controller mein hoti
  hai (Lesson 05).

## Next

Aap ne Level 2 mukammal kar liya hai. Aap logic ko us ki sahi jagah par
rakh sakte hain, form ko shape de sakte hain, API expose kar sakte hain,
report aur print format bana sakte hain, lock down kar sakte hain ke kaun
kya dekhta hai, aur approvals ko sahi logon tak route kar sakte hain.

Level 3 Scheduler se shuru hota hai — background jobs aur queues:
[11 — Scheduler & Background Jobs](../level-3/11-scheduler-jobs.md).
