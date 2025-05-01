# Copyright (c) 2025, Al-Aswany and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class PerformanceReview(Document):
	def validate(self):
		self.validate_status_transition()
		self.validate_required_fields_for_status()
	
	def validate_status_transition(self):
		"""Validate that status transitions follow the proper workflow"""
		if not self.is_new():
			old_doc = self.get_doc_before_save()
			allowed_transitions = {
				"Pending Review": ["Review Scheduled"],
				"Review Scheduled": ["Feedback Provided"],
				"Feedback Provided": ["Under Approval"],
				"Under Approval": ["Review Approved", "Review Rejected"],
				"Review Approved": [],  # Terminal state
				"Review Rejected": []   # Terminal state
			}
			
			if old_doc.status != self.status and self.status not in allowed_transitions.get(old_doc.status, []):
				frappe.throw(_(f"Cannot transition from {old_doc.status} to {self.status}. Invalid status transition."))
	
	def validate_required_fields_for_status(self):
		"""Validate required fields based on status"""
		if self.status == "Feedback Provided" and not self.feedback:
			frappe.throw(_("Feedback is required when status is 'Feedback Provided'"))
		
		if self.status == "Review Scheduled" and not self.review_date:
			frappe.throw(_("Review Date is required when status is 'Review Scheduled'"))
	
	def on_submit(self):
		"""Handle document submission logic"""
		if self.status == "Review Rejected":
			frappe.throw(_("Cannot submit a rejected performance review"))
		
		# Set status to approved upon submission if not already
		if self.status != "Review Approved":
			self.status = "Review Approved"
	
	def on_cancel(self):
		"""Handle document cancellation logic"""
		self.status = "Review Rejected"
