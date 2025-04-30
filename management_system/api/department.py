import frappe
@frappe.whitelist()
def get_departments(department=None):
    if department:
        # Get specific department with only selected fields
        department_doc = frappe.get_doc('MS Department', department)
        department_data = {
            'name': department_doc.name,
            'department_name': department_doc.department_name,
            'company': department_doc.company,
            'number_of_employees': department_doc.number_of_employees,
            'number_of_projects': department_doc.number_of_projects
        }
        return {'status': 'success', 'data': department_data}
    else:
        # Get all departments
        departments = frappe.get_list('MS Department', 
                                    fields=['name', 'department_name', 'company', 'number_of_employees', 'number_of_projects'],
                                    order_by='department_name')
        return {'status': 'success', 'data': departments}
