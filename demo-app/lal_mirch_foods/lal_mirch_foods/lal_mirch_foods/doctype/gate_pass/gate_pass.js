// lal_mirch_foods/lal_mirch_foods/doctype/gate_pass/gate_pass.js
frappe.ui.form.on("Gate Pass", {
	refresh(frm) {
		// New passes always start with today — the guard should not type it.
		if (frm.is_new()) {
			frm.set_value("gate_pass_date", frappe.datetime.nowdate());
		}
	},
	validate(frm) {
		if (
			(frm.doc.purpose === "Delivery" || frm.doc.purpose === "Pickup") &&
			!frm.doc.items.length
		) {
			frappe.throw(__("Add at least one item for a Delivery or Pickup pass."));
		}
	},
});
