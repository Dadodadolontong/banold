import frappe

#Pending:
#1. Auto Batch number --> Ok
#2. Update FG Qty  --> Ok
#3. Additional cost
#4. Full cycle test

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

        fg = frappe.get_doc({
                "doctype":"Batch",
                "batch_id":doc.batch_no,
                "item":"FG-ALNPKT-00",
                "expiry_date":frappe.utils.data.add_years(doc.planned_start_date,2)}).insert()
				
        bch = frappe.get_doc({
                "doctype":"Batch",
                "batch_id":doc.batch_no+"-B",
                "item":"IM-ALNWIP-00",
                "expiry_date":frappe.utils.data.add_years(doc.planned_start_date,2),
				"reference_name":doc.batch_no}).insert()

        sch = frappe.get_doc({
                "doctype":"Batch",
                "batch_id":doc.batch_no+"-S",
                "item":"FG-ALNSCH-00",
                "expiry_date":frappe.utils.data.add_years(doc.planned_start_date,2),
				"reference_name":doc.batch_no}).insert()

def calc_rate(doc, method):
	
	from frappe.utils import flt
	
	if (doc.purpose in ["Manufacture", "Repack"]) and (frappe.db.get_value('BOM',{'name':doc.bom_no},'custom_costing')):
	
		rm_material_cost = 0.0
		pm_material_cost = 0.0
		rm_qty = 0.0
		rm_rate = 0.0
		pm_qty = 0.0
		scrap_qty = 0.0
		fg_qty = 0.0
		
		scrap_rate = 0.0
		
		prd_qty = frappe.get_doc('Production Order',doc.production_order).qty
		batch_no = frappe.get_doc('Production Order',doc.production_order).batch_no
		
		for d in doc.get('items'):
			if not d.t_warehouse:
			   item_cat = frappe.get_doc('Item',d.item_code).item_group
			   
			   if item_cat == "Raw Material":
					rm_material_cost += flt(d.basic_amount)
					rm_qty += flt(d.qty)
			   else:
					pm_material_cost += flt(d.basic_amount)
					pm_qty += flt(d.qty)
			else:	  
				if frappe.get_doc('Production Order',doc.production_order).scrap_warehouse == d.t_warehouse:
					#Scrap item --> Sachet nya
					scrap_qty += flt(d.qty)
												   
				if frappe.get_doc('Production Order',doc.production_order).fg_warehouse == d.t_warehouse:
					#fg item --> Sisa cair nya
					fg_qty += flt(d.qty)
		
		#Hitung cost sachet: (rm_material_cost + pm_material_cost - sisa fg_qty*rate) / im_qty
		
		rm_rate = rm_material_cost / prd_qty 
		
		scrap_rate = (rm_material_cost + pm_material_cost - (rm_rate*fg_qty))/scrap_qty
		
		for d in doc.get('items'):
			if d.t_warehouse:
			    
				d.batch_no = frappe.db.get_value('Batch',{"reference_name":batch_no,"item":d.item_code},"name")
				
				if frappe.get_doc('Production Order',doc.production_order).scrap_warehouse == d.t_warehouse:
					#Scrap item
					d.basic_rate = scrap_rate
					d.basic_amount = scrap_rate * d.qty		
			   
				if frappe.get_doc('Production Order',doc.production_order).fg_warehouse == d.t_warehouse:
					#fg item
					d.basic_rate = rm_rate
					d.basic_amount = rm_rate * d.qty
					
		doc.set_total_incoming_outgoing_value()
