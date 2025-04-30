import json
from frappe import _
import frappe    


def _get_request_data():
    """Parse and return request data as JSON"""
    return json.loads(frappe.request.data.decode('utf-8'))

def _format_project_data(project):
    """Create a standardized project data response"""
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

    if hasattr(project, 'assigned_employees'):
        for emp in project.assigned_employees:
            project_data['assigned_employees'].append({
                'employee': emp.employee
            })
    
    return project_data


def _handle_employee_assignments(project, assigned_employees):
    """Process and assign employees to a project"""
    if assigned_employees is None:
        return
        
    # For update operations, clear existing employees first
    if project.get('name'):
        project.assigned_employees = []
        
    for emp in assigned_employees:
        if isinstance(emp, dict) and 'doctype' in emp:
            emp.pop('doctype')
        project.append('assigned_employees', {
            'employee': emp.get('employee') if isinstance(emp, dict) else emp
        })


@frappe.whitelist()
def create_project():
    data = _get_request_data()
    assigned_employees = data.pop('assigned_employees', None)
    
    project = frappe.new_doc('MS Project')
    
    # Set project attributes
    for key, value in data.items():
        if key != 'doctype' and hasattr(project, key):
            project.set(key, value)
    
    _handle_employee_assignments(project, assigned_employees)
    
    project.save()
    frappe.db.commit()
    
    return {
        'status': 'success', 
        'message': _('Project created successfully'), 
        'data': _format_project_data(project)
    }


@frappe.whitelist()
def get_projects(project=None):
    if project:
        # Get single project
        project_doc = frappe.get_doc('MS Project', project)
        return {
            'status': 'success', 
            'data': _format_project_data(project_doc)
        }
    else:
        # Get all projects
        projects = frappe.get_list(
            'MS Project', 
            fields=['name', 'project_name', 'company', 'department',
                    'description', 'start_date', 'end_date'],
            order_by='project_name'
        )
        
        # Get assigned employees for each project
        for project in projects:
            employees = frappe.get_list(
                'Employee Project', 
                filters={'parent': project.name},
                fields=['employee']
            )
            project['assigned_employees'] = employees
            
        return {'status': 'success', 'data': projects}


@frappe.whitelist()
def update_project():
    data = _get_request_data()
    
    project_id = data.get('name')
    assigned_employees = data.pop('assigned_employees', None)
    
    project = frappe.get_doc('MS Project', project_id)
    
    # Update project attributes
    for key, value in data.items():
        if key != 'name' and key != 'doctype' and hasattr(project, key):
            project.set(key, value)
    
    _handle_employee_assignments(project, assigned_employees)
    
    project.save()
    frappe.db.commit()
    
    return {
        'status': 'success', 
        'message': _('Project updated successfully'), 
        'data': _format_project_data(project)
    }

@frappe.whitelist()
def delete_project():
    data = _get_request_data()
    project_id = data.get('name')
    
    frappe.delete_doc('MS Project', project_id)
    frappe.db.commit()
    
    return {'status': 'success', 'message': _('Project deleted successfully')}
