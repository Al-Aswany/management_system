import frappe
from datetime import datetime 

def calculate_days():
    employees = frappe.get_list("MS Employee", fields=["name", "hired_on"])
    today = datetime.now().strftime('%Y-%m-%d')
    today = datetime.strptime(today, '%Y-%m-%d')
    for employee in employees:
        if employee.hired_on:
            hired_on = employee.hired_on
            hired_on = hired_on.strftime('%Y-%m-%d')
            hired_on=datetime.strptime(hired_on, '%Y-%m-%d')
            number_of_days =( today - hired_on).days
            frappe.db.set_value("MS Employee", employee.name, "days_employed", int(number_of_days)+1)
            frappe.db.commit()
        else:
            frappe.db.set_value("MS Employee", employee.name, "days_employed", 0)
            frappe.db.commit()