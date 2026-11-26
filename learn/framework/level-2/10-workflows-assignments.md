# 10 — Workflows & Assignments

## What it is

A **Workflow** is a state machine for a document: who may move it from
one stage to the next, and under what condition. An **Assignment Rule**
routes the document to a person automatically — round robin, least busy,
or from a field on the document itself. Together they answer: *who approves
this, and whose desk does it land on?*

A Workflow only works on a **submittable** DocType (`is_submittable`) — it
drives `docstatus` (0 Draft, 1 Submitted, 2 Cancelled), so there must be a
submitted state to drive. When you activate a Workflow, Frappe creates the
`workflow_state` field on the DocType for you — do not drive state with a
custom Select field.

## Minimal working example — Quality Inspection approval

A spice batch arrives. The inspection must be approved by the QA Manager
before the batch can be used. Desk → **Workflow** → New, Document Type:
**Quality Inspection**, Is Active ✓.

**States** — each state carries a docstatus:

| State | Doc Status | Who can edit |
|---|---|---|
| Draft | 0 | Quality User |
| Pending Approval | 0 | — |
| Approved | 1 | — |
| Rejected | 0 | Quality User |

**Transitions** — each one: from a state, an action, to a state, a role,
an optional condition:

| From | Action | To | Allowed | Condition |
|---|---|---|---|---|
| Draft | Submit for Approval | Pending Approval | Quality User | |
| Pending Approval | Approve | Approved | Quality Manager | |
| Pending Approval | Reject | Rejected | Quality Manager | |
| Rejected | Revise | Draft | Quality User | |

Two rules that save real projects:

- **Intermediate approval states stay at docstatus 0.** Only the final
  "Approved" state is 1. A submitted document cannot go back to draft —
  docstatus only moves forward (0→0, 0→1, 1→1, 1→2).
- **Rejected is docstatus 0**, so it can be fixed and resubmitted. A
  rejected inspection that is docstatus 1 or 2 is stuck.

Set **Allow Self Approval = 0** when the creator must not approve their
own document. Only **one** Workflow per DocType can be active. Conditions
are Python expressions on the document: `doc.grand_total > 100000`,
`doc.inspection_type == "Incoming"`.

Apply a transition in code — never set `workflow_state` directly:

```python
from frappe.model.workflow import apply_workflow, get_transitions

apply_workflow(doc, "Approve")   # respects roles and conditions
get_transitions(doc)              # actions available to the current user
```

## Minimal working example — route inspections to the QA team

Desk → **Assignment Rule** → New, Document Type: **Quality Inspection**:

| Field | Value |
|---|---|
| Assign Condition | `doc.inspection_type == "Incoming"` |
| Rule | Round Robin |
| Users | qa.ahmed@…, qa.sana@…, qa.bilal@… |
| Priority | 1 |
| Assignment Days | Mon–Fri |

**Round Robin** cycles through the users in order. **Load Balancing**
gives the document to whoever has the fewest open assignments — the right
choice for support tickets. **Based on Field** reads a User link field from
the document itself (for example, each factory's designated auditor). The
highest Priority rule that matches wins. `Unassign Condition` releases the
assignment (for example, when the document is cancelled); `Close Condition`
closes the ToDo when the work is done.

## When to use — and when not to

| Situation | Use |
|---|---|
| "Who may approve this, and in what order?" | Workflow |
| "Whose desk does this land on?" | Assignment Rule |
| A rule the document must pass (dates, quantities, limits) | Controller `validate` / `before_submit` — not a Workflow condition |
| A document that is never submitted | No Workflow — workflows need a submittable DocType |
| A one-off approval by email | Share the document + a comment — not a whole Workflow |
| Routing by team, territory, or workload | Assignment Rule, not a Workflow state |

## Common mistakes

- **Intermediate state at docstatus 1.** The document submits halfway
  through approval and can never go back to draft. Approvals stay at 0
  until the final state.
- **Setting `doc.workflow_state` directly** to skip an approval. Use
  `apply_workflow` — it checks roles, conditions, and self-approval.
- **Calling `doc.submit()` on a workflow-controlled document.** The
  workflow does the submit, when the final transition runs.
- **Driving state with a custom Select field.** Use the Workflow State
  field (`workflow_state`) — that is what the engine reads.
- **No state with docstatus 0.** New documents start there. Without one,
  nothing can be created.
- **An Assignment Rule with no users, or a condition that never matches.**
  Test the rule with a real document — an unmatched rule silently does
  nothing.
- **Two active workflows on one DocType.** Only one can be active; the
  second activation deactivates the first.
- **Business validation in a transition condition.** Conditions decide
  *who may act*; validation belongs in the controller (Lesson 05).

## Next

You have finished Level 2. You can put logic where it belongs, shape the
form, expose an API, build a report and a print format, lock down who sees
what, and route approvals to the right people.

Level 3 starts with the Scheduler — background jobs and queues:
[11 — Scheduler & Background Jobs](../level-3/11-scheduler-jobs.md).
