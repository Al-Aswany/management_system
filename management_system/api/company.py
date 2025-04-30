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




