# Copyright (c) 2025, Al-Aswany and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MSProject(Document):
	
	def on_update(self):

		if self.company:
			self.update_company_count(self.company)

		if self.department:
			self.update_department_count(self.department)

		if self.get_doc_before_save() and self.get_doc_before_save().department != self.department:

			old_department = self.get_doc_before_save().department
			if old_department:
				self.update_department_count(old_department)

		new_employees = []
		if  self.assigned_employees:
			for emp in self.assigned_employees:
				if emp.employee:
					new_employees.append(emp.employee) 
			
			for employee in new_employees:
				self.update_employee_count(employee)
		
		# Check if employees were removed by comparing with previous version
		if self.get_doc_before_save():
			old_doc = self.get_doc_before_save()
			if old_doc.assigned_employees:
				old_employees = []
				for emp in old_doc.assigned_employees:
					if emp.employee:
						old_employees.append(emp.employee)
				
				# Find employees removed from project
				for employee in old_employees:
					if employee not in new_employees:
						self.update_employee_count(employee)

	def after_delete(self):
		# Update all related counts
		if self.company:
			self.update_company_count(self.company)
		if self.department:
			self.update_department_count(self.department)

		if self.assigned_employees:
			for emp in self.assigned_employees:
				if emp.employee:
					self.update_employee_count(emp.employee)

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

	def update_employee_count(self, employee):
		try:
			project_count = frappe.db.count("Employee Project", {"employee": employee})			
			frappe.db.set_value("MS Employee", employee, "number_of_assigned_projects", project_count)
			frappe.db.commit()
		except Exception as e:
			frappe.log_error(f"Failed to update employee project count: {str(e)}", "MS Project Update Error")

	def update_employees_count(self, employees):
		if not employees:
			return
			
		for employee in employees:
			self.update_employee_count(employee)

