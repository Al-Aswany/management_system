# Copyright (c) 2025, Al-Aswany and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MSProject(Document):
	
	def on_update(self):
		# For new projects, update all counts
		if self.company:
			self.update_company_count(self.company)

		# Handle department change
		if self.department:
			self.update_department_count(self.department)
			

		# Handle employees change
		new_employees = []
		if frappe.get_list('Employee Project', filters={'parent': self.name}):
			new_employees = frappe.get_list('Employee Project', 
										 filters={'parent': self.name},
										 fields=['employee'])
			self.update_employees_count(new_employees)
		

	def after_delete(self):
		# Update all related counts
		if self.company:
			self.update_company_count(self.company)
		if self.department:
			self.update_department_count(self.department)
			
		employees = []
		if frappe.get_list('Employee Project', filters={'parent': self.name}):
			employees = frappe.get_list('Employee Project', 
									 filters={'parent': self.name},
									 fields=['employee'])
			self.update_employees_count(employees)

	def update_company_count(self, company):
		if not company:
			return
			
		try:
			project_count = frappe.db.count("MS Project", {"company": company})
			frappe.db.set_value("MS Company", company, "number_of_projects", project_count)
			frappe.db.commit()
		except Exception as e:
			frappe.log_error(f"Failed to update company project count: {str(e)}", "MS Project Update Error")

	def update_department_count(self, department):
		if not department:
			return
			
		try:
			project_count = frappe.db.count("MS Project", {"department": department})
			frappe.db.set_value("MS Department", department, "number_of_projects", project_count)
			frappe.db.commit()
		except Exception as e:
			frappe.log_error(f"Failed to update department project count: {str(e)}", "MS Project Update Error")

	def update_employees_count(self, employees):
		if not employees:
			return
			
		for employee in employees:
			try:
				project_count = frappe.db.count("Employee Project", {"employee": employee.employee})
				frappe.db.set_value("MS Employee", employee.employee, "number_of_assigned_projects", project_count)
				frappe.db.commit()
			except Exception as e:
				frappe.log_error(f"Failed to update employee project count: {str(e)}", "MS Project Update Error")

