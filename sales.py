import frappe

def explode(doc, method)
    
    for line in doc.get('items'):
        orig_qty = line.qty

        batch_avail = frappe.db.sql("""select batch_no, bt.expiry_date, warehouse, sum(actual_qty)i as onhand from `tabStock Ledger Entry` le join tabBatch bt on bt.name = le.batch_no where item_code = '{}' group by batch_no, bt.expiry_date, warehouse having sum(actual_qty) <> 0 order by bt.expiry_date""".format(line.item_code), as_dict=1)

        item = frappe.get_doc("Item",item_code);
        run_sum = orig_qty
    
        for batch in batch_avail:
            qty = min(flt(batch['onhand']),run_sum);

            doc.append("items", {
                      "item_code":line.item_code,
                      "qty": qty,
                      "batch_no": batch['batch_no'],
                      "warehouse": batch['warehouse'],
                      "stock_uom":line.uom,
                      "rate": line.price
            })

           ]

            run_sum-=qty;
            if (run_sum<=0):
               break

    