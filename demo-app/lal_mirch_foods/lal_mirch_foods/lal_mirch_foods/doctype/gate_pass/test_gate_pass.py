import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, today


class TestGatePass(FrappeTestCase):
	def test_future_date_is_blocked(self):
		doc = frappe.get_doc(
			{
				"doctype": "Gate Pass",
				"gate_pass_date": add_days(today(), 1),
				"visitor_name": "Test Visitor",
				"purpose": "Visit",
			}
		)
		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_delivery_pass_without_items_is_blocked(self):
		doc = frappe.get_doc(
			{
				"doctype": "Gate Pass",
				"gate_pass_date": today(),
				"visitor_name": "Test Supplier",
				"purpose": "Delivery",
			}
		)
		self.assertRaises(frappe.ValidationError, doc.insert)
