import frappe
from frappe.utils import add_days, today


def daily():
	"""Remind the Gatekeeper about Delivery passes still in Draft after
	3 days — one ToDo per pass, so nothing waits at the gate forever."""
	cutoff = add_days(today(), -3)
	stale = frappe.get_list(
		"Gate Pass",
		filters={"purpose": "Delivery", "docstatus": 0, "gate_pass_date": ("<", cutoff)},
		fields=["name", "owner", "gate_pass_date"],
	)
	for row in stale:
		if frappe.db.exists(
			"ToDo",
			{"reference_type": "Gate Pass", "reference_name": row.name, "status": "Open"},
		):
			continue
		frappe.get_doc(
			{
				"doctype": "ToDo",
				"allocated_to": row.owner,
				"reference_type": "Gate Pass",
				"reference_name": row.name,
				"description": f"Delivery Gate Pass {row.name} from {row.gate_pass_date} is still in Draft.",
				"date": today(),
			}
		).insert(ignore_permissions=True)
