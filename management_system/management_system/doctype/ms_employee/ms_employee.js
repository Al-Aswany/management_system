// Copyright (c) 2025, Al-Aswany and contributors
// For license information, please see license.txt

frappe.ui.form.on('MS Employee', {
	onload: function(frm) {
		// show only departments following the selected company
		frm.set_df_property('department', 'read_only', 1);
		if(frm.doc.company){
			frm.set_df_property('department', 'read_only', 0);
        frm.set_query('department', function() {
            return {
                filters: {
                    'company': frm.doc.company 
                }
            };
        });
		}

	},
	company: function(frm) {
		frm.set_df_property('department', 'read_only', 1);
		frm.doc.department = null
		if(frm.doc.company){
			frm.set_df_property('department', 'read_only', 0);
        frm.set_query('department', function() {
            return {
                filters: {
                    'company': frm.doc.company 
                }
            };
        });
		}
    },
});
