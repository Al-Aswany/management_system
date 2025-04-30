import frappe
from frappe import _
import json



@frappe.whitelist()
def get_companies(company=None):
    if company:
        # Get specific company with only selected fields
        company_doc = frappe.get_doc('MS Company', company)
        company_data = {
            'name': company_doc.name,
            'company_name': company_doc.company_name,
            'number_of_departments': company_doc.number_of_departments,
            'number_of_employees': company_doc.number_of_employees,
            'number_of_projects': company_doc.number_of_projects
        }
        return {'status': 'success', 'data': company_data}
    else:
        # Get all companies
        companies = frappe.get_list('MS Company', 
                                  fields=['name', 'company_name', 'number_of_departments', 'number_of_employees', 'number_of_projects'],
                                  order_by='company_name')
        return {'status': 'success', 'data': companies}



#######################################################
# Employee API Endpoints
#######################################################

@frappe.whitelist()
def create_employee():
    # Create new employee document
    data = json.loads(frappe.request.data.decode('utf-8'))
    
    employee = frappe.new_doc('MS Employee')
    for key, value in data.items():
        employee.set(key, value)
    
    employee.save()
    frappe.db.commit()
    
    # Return same fields as get_employees
    employee_data = {
        'name': employee.name,
        'employee_name': employee.employee_name,
        'email_address': employee.email_address,
        'mobile_number': employee.mobile_number,
        'address': employee.address,
        'company': employee.company,
        'department': employee.department,
        'title': employee.title,
        'hired': employee.hired,
        'hired_on': employee.hired_on,
        'days_employed': employee.days_employed,
        'number_of_assigned_projects': employee.number_of_assigned_projects
    }
    
    return {'status': 'success', 'message': _('Employee created successfully'), 'data': employee_data}



#######################################################
# Project API Endpoints
#######################################################

@frappe.whitelist()
def create_project():
    # Create new project
    data = json.loads(frappe.request.data.decode('utf-8'))

    assigned_employees = data.pop('assigned_employees', None)

    project = frappe.new_doc('MS Project')

    for key, value in data.items():
        if key != 'doctype' and hasattr(project, key):
            project.set(key, value)

    if assigned_employees:
        for emp in assigned_employees:
            if 'doctype' in emp:
                emp.pop('doctype')
            project.append('assigned_employees', {
                'employee': emp.get('employee')
            })

    project.save()
    frappe.db.commit()
    
    # Create a clean response
    project_data = {
        'name': project.name,
        'project_name': project.project_name,
        'company': project.company,
        'department': project.department,
        'description': project.description,
        'start_date': project.start_date,
        'end_date': project.end_date,
        'assigned_employees': []
    }
    
    # Add simplified employee data to response
    if hasattr(project, 'assigned_employees'):
        for emp in project.assigned_employees:
            project_data['assigned_employees'].append({
                'employee': emp.employee
            })
    
    return {'status': 'success', 'message': _('Project created successfully'), 'data': project_data}

@frappe.whitelist()
def get_projects(project=None):
    if project:
        project_doc = frappe.get_doc('MS Project', project)

        employees = []
        if frappe.get_list('Employee Project', filters={'parent': project.name}):
            employees = frappe.get_list('Employee Project', 
                                         filters={'parent': project.name},
                                         fields=['employee'])
        
        project_data = {
            'name': project_doc.name,
            'project_name': project_doc.project_name,
            'company': project_doc.company,
            'department': project_doc.department,
            'description': project_doc.description,
            'start_date': project_doc.start_date,
            'end_date': project_doc.end_date,
            'assigned_employees': employees,
        }
        return {'status': 'success', 'data': project_data}
    else:
        projects = frappe.get_list('MS Project', 
                                 fields=['name', 'project_name', 'company', 'department',
                                        'description', 'start_date', 'end_date'],
                                 order_by='project_name')
        
        for project in projects:
            if frappe.get_list('Employee Project', filters={'parent': project.name}):
                employees = frappe.get_list('Employee Project', 
                                         filters={'parent': project.name},
                                         fields=['employee'])
                project['assigned_employees'] = employees
            
        return {'status': 'success', 'data': projects}

@frappe.whitelist()
def update_project():
    # Update project
    data = json.loads(frappe.request.data.decode('utf-8'))
    
    project_id = data.get('name')
    project = frappe.get_doc('MS Project', project_id)
    
    # Extract assigned_employees before updating project
    assigned_employees = data.pop('assigned_employees', None)
    
    # Update fields
    for key, value in data.items():
        if key != 'name' and key != 'doctype' and hasattr(project, key):
            project.set(key, value)
    
    # Update assigned_employees if provided
    if assigned_employees is not None:
        # Clear existing assigned_employees
        project.assigned_employees = []
        
        # Add new assigned_employees
        for emp in assigned_employees:
            if 'doctype' in emp:
                emp.pop('doctype')
            project.append('assigned_employees', {
                'employee': emp.get('employee')
            })
    
    project.save()
    frappe.db.commit()
    
    # Create a clean response
    project_data = {
        'name': project.name,
        'project_name': project.project_name,
        'company': project.company,
        'department': project.department,
        'description': project.description,
        'start_date': project.start_date,
        'end_date': project.end_date,
        'assigned_employees': []
    }
    
    # Add simplified employee data to response
    if hasattr(project, 'assigned_employees'):
        for emp in project.assigned_employees:
            project_data['assigned_employees'].append({
                'employee': emp.employee
            })
    
    return {'status': 'success', 'message': _('Project updated successfully'), 'data': project_data}

@frappe.whitelist()
def delete_project():
    # Delete project
    data = json.loads(frappe.request.data.decode('utf-8'))
    
    project_id = data.get('name')
    frappe.delete_doc('MS Project', project_id)
    frappe.db.commit()
    return {'status': 'success', 'message': _('Project deleted successfully')}
