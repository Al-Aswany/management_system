# Copyright (c) 2025, Al-Aswany and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MSDepartment(Document):
	
	def on_update (self):
		self.update_company_count(self.company)

	def after_delete(self):
		self.update_company_count(self.company)

	def update_company_count(self, company):
		count = frappe.db.count('MS Department', {'company': company})
		frappe.db.set_value('MS Company', company, 'number_of_departments', count)
