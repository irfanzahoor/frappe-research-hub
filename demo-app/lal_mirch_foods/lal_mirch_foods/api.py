import frappe
from frappe import _


def validate_gate_pass(doc, method):
	"""Server-side mirror of the Gate Pass client rule: a Delivery or
	Pickup pass must list at least one item. Client scripts can be
	bypassed, so the server enforces it."""
	if doc.purpose in ("Delivery", "Pickup") and not doc.items:
		frappe.throw(_("Add at least one item for a Delivery or Pickup pass."))
