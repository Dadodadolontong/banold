import frappe

@frappe.whitelist()

def test(doc, method):
	doc.po_no = '123456'

def printit(doc, method):
	frappe.msgprint('123456')

def check_batch(doc, method):
        
        batch_exists = frappe.db.exists({
                             "doctype": "Batch",
                             "batch_id":doc.batch_no})

	if batch_exists:
           frappe.msgprint(_("Batch sudah ada"))
           validated = false	

def production_order_on_submit(doc, method):

        frappe.msgprint(_("Test ok")

        batch = frappe.get_doc({
                "doctype":"Batch",
                "batch_id":doc.batch_no,
                "item":"IM-ALNWIP-00",
                "expiry_date":frappe.utils.data.add_years(doc.planned_start_date,2)}).insert()

        sch = frappe.get_doc({
                "doctype":"Batch",
                "batch_id":doc.batch_no,
                "item":"FG-ALNSCH-00",
                "expiry_date":frappe.utils.data.add_years(doc.planned_start_date,2)}).insert()

        fg = frappe.get_doc({
                "doctype":"Batch",
                "batch_id":doc.batch_no,
                "item":"FG-ALNPKT-00",
                "expiry_date":frappe.utils.data.add_years(doc.planned_start_date,2)}).insert()

