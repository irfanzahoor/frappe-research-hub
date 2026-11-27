app_name = "lal_mirch_foods"
app_title = "Lal Mirch Foods"
app_publisher = "Muhammad Irfaan"
app_description = "Demo app for the Frappe Research Hub practice project — Gate Pass register for the Lal Mirch Foods spice factory."
app_license = "mit"

# Document Events
# ---------------
# Hook on document methods and events.
# The Gate Pass item rule lives here (not in the controller) so the
# server enforces it even when the client script is bypassed:
# a Delivery or Pickup pass must list at least one item.
doc_events = {
	"Gate Pass": {
		"validate": "lal_mirch_foods.api.validate_gate_pass",
	}
}

# Scheduled Tasks
# ---------------
scheduler_events = {
	"daily": [
		"lal_mirch_foods.tasks.daily"
	],
}

# Fixtures
# --------
# Customizations made in Desk (Custom Fields, Property Setters, Print
# Formats) live in the database until exported:
#   bench --site <site> export-fixtures --app lal_mirch_foods
# Uncomment and list them here to ship them with the app:
# fixtures = ["Custom Field", "Property Setter", "Print Format"]
