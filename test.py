import frappe
import erpnext

def submit():
    i = 0
    for si in frappe.get_all("Sales Invoice", filters=[["docstatus","=",0],["posting_date",">=","2017-01-01"]]):
        si = frappe.get_doc("Sales Invoice", si.name) 
        i += 1
        try:
          si.submit()
          print "{0} {1} Ok".format(i,si.name)
        except frappe.exceptions.ValidationError as e:
          print "{0} {1} Not Ok : {2}".format(i,si.name,e.args)
