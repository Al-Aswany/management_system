import frappe
import json
from frappe import _

def _get_employee_data(employee_doc):
    """Helper function to extract standard employee data fields"""
    return {
        'name': employee_doc.name,
        'employee_name': employee_doc.employee_name,
        'email_address': employee_doc.email_address,
        'mobile_number': employee_doc.mobile_number,
        'address': employee_doc.address,
        'company': employee_doc.company,
        'department': employee_doc.department,
        'title': employee_doc.title,
        'hired': employee_doc.hired,
        'hired_on': employee_doc.hired_on,
        'days_employed': employee_doc.days_employed,
        'number_of_assigned_projects': employee_doc.number_of_assigned_projects
    }

@frappe.whitelist()
def get_employees(employee=None):
    if employee:
        # Get specific employee
        employee_doc = frappe.get_doc('MS Employee', employee)
        return {'status': 'success', 'data': _get_employee_data(employee_doc)}
    else:
        # Get all employees
        fields = list(_get_employee_data(frappe.new_doc('MS Employee')).keys())
        employees = frappe.get_list('MS Employee', fields=fields, order_by='employee_name')
        return {'status': 'success', 'data': employees}

@frappe.whitelist()
def update_employee():
    data = json.loads(frappe.request.data.decode('utf-8'))
    
    employee_id = data.get('name')
    employee = frappe.get_doc('MS Employee', employee_id)
    
    for key, value in data.items():
        if key != 'name' and hasattr(employee, key):
            employee.set(key, value)
    
    employee.save()
    frappe.db.commit()
    
    return {
        'status': 'success', 
        'message': _('Employee updated successfully'), 
        'data': _get_employee_data(employee)
    }

@frappe.whitelist()
def create_employee():
    data = json.loads(frappe.request.data.decode('utf-8'))
    
    employee = frappe.new_doc('MS Employee')
    for key, value in data.items():
        employee.set(key, value)
    
    employee.save()
    frappe.db.commit()

    return {
        'status': 'success', 
        'message': _('Employee created successfully'), 
        'data': _get_employee_data(employee)
    }

@frappe.whitelist()
def delete_employee():
    data = json.loads(frappe.request.data.decode('utf-8'))
    
    employee_id = data.get('name')
    frappe.delete_doc('MS Employee', employee_id)
    frappe.db.commit()
    
    return {'status': 'success', 'message': _('Employee deleted successfully')}