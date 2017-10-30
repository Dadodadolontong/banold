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
           frappe.msgprint("Batch sudah ada")
           validated = false	

def production_order_on_submit(doc, method):

         bch = frappe.get_doc({
                "doctype":"Batch",
                "batch_id":doc.batch_no+"-B",
                "item":"IM-ALNWIP-00",
                "expiry_date":frappe.utils.data.add_years(doc.planned_start_date,2)}).insert()

        sch = frappe.get_doc({
                "doctype":"Batch",
                "batch_id":doc.batch_no+"-S",
                "item":"FG-ALNSCH-00",
                "expiry_date":frappe.utils.data.add_years(doc.planned_start_date,2)}).insert()

        fg = frappe.get_doc({
                "doctype":"Batch",
                "batch_id":doc.batch_no,
                "item":"FG-ALNPKT-00",
                "expiry_date":frappe.utils.data.add_years(doc.planned_start_date,2)}).insert()

def calc_rate(doc, method):
	from frappe.utils import flt
	
	rm_material_cost = 0.0
	pm_material_cost = 0.0
	rm_qty = 0.0
	rm_rate = 0.0
	pm_qty = 0.0
	im_qty = 0.0
	fg_qty = 0.0
	fg_cost = 0.0
	im_cost = 0.0
	
	for d in doc.get('items'):
		if !d.t_warehouse:
		   item_cat = frappe.get_doc('Item',d.item).item_group
		   
		   if item_cat == "Raw Material":
				rm_material_cost += flt(d.basic_amount)
				rm_qty += flt(d.qty)
		   else:
		      pm_material_cost += flt(d.basic_amount)
			  pm_qty += flt(d.qty)
		else:	  
			if frappe.get_doc('Production Order',se.production_order).scrap_warehouse == d.t_warehouse:
				#Scrap item
				im_qty += flt(d.qty)
		   
			if frappe.get_doc('Production Order',se.production_order).fg_warehouse == d.t_warehouse:
				#fg item
				fg_qty += flt(d.qty)
	
    if rm_qty:	
		rm_rate = rm_material_cost / rm_qty
	
	if fg_qty:
		fg_rate = (rm_material_cost - im_cost + pm_material_cost)/fg_qty
	
	for d in doc.get('items'):
		if d.t_warehouse:
			if frappe.get_doc('Production Order',se.production_order).scrap_warehouse = d.t_warehouse:
				#Scrap item
				d.basic_rate = rm_rate
				d.basic_amount = rm_rate * d.qty
		   
			if frappe.get_doc('Production Order',se.production_order).fg_warehouse = d.t_warehouse:
				#fg item
				d.basic_rate = fg_rate
				d.basic_amount = fg_rate * d.qty