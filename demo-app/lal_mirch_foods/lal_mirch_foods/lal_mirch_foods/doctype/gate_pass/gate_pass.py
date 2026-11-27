import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, today


class GatePass(Document):
	def validate(self):
		self.validate_date_not_in_future()
		self.validate_item_quantities()

	def validate_date_not_in_future(self):
		if self.gate_pass_date and getdate(self.gate_pass_date) > getdate(today()):
			frappe.throw(_("Gate Pass Date cannot be in the future."))

	def validate_item_quantities(self):
		for row in self.items:
			if row.qty is not None and row.qty <= 0:
				frappe.throw(_("Qty must be positive on row {0}.").format(row.idx))
