# Copyright (c) 2025, Al-Aswany and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MSEmployee(Document):

	def before_save(self):
		self.validate_mobile_number()

	def validate_mobile_number(self):
		# Ensure mobile number starts with '0' and has exactly 11 digits if provided.
		if self.mobile_number and ((not self.mobile_number.startswith('0')) or len(self.mobile_number) != 11):
			frappe.throw("Mobile number must start with '0' and be exactly 11 digits long")

	def on_update(self):
		# Update counts for current company and department
		self.update_company_count(self.company)
		self.update_department_count(self.department)
		
		# Check if department has changed and update the previous department count
		old_doc = self.get_doc_before_save()
		if old_doc and old_doc.department != self.department:
			self.update_department_count(old_doc.department)

	def after_delete(self):
		self.update_company_count(self.company)
		self.update_department_count(self.department)

	def update_company_count(self, company):
		if not company:
			return
			
		try:
			employee_count = frappe.db.count("MS Employee", {"company": company})
			frappe.db.set_value("MS Company", company, "number_of_employees", employee_count)
			frappe.db.commit()
		except Exception as e:
			frappe.log_error(f"Failed to update company count: {str(e)}", "MS Employee Update Error")

	def update_department_count(self, department):
		if not department:
			return
			
		try:
			employee_count = frappe.db.count("MS Employee", {"department": department})
			frappe.db.set_value("MS Department", department, "number_of_employees", employee_count)
			frappe.db.commit()
		except Exception as e:
			frappe.log_error(f"Failed to update department count: {str(e)}", "MS Employee Update Error")


		

