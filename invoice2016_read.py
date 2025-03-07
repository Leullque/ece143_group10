import pandas as pd
from datetime import datetime

def invoice2016_read(filename):  
	'''                                                                 
	Reads the csv and cleans up the data to get it ready for analysis.
	POnumber can be used to match the entire row with its corresponding row with the output from purchase2016_read
	PODate, InvoiceDate, PayDate gets converted to date format.
	                                                                    
	filename:= filename with relative path to the invoice2016 csv
	x:= a pd.DataFrame object returned with the cleaned up data                                         
	'''
	assert(type(filename)) == str, "Input filename should be a string"

	x = pd.read_csv(filename)
	assert type(x) == pd.DataFrame, "Input x should be a panda series"
	assert len(x) > 0, "Input x should be non-empty"

	col_po_number = x["PONumber"]
	col_po_date = x["PODate"]
	col_invoice_date = x["InvoiceDate"]
	col_pay_date = x["PayDate"]

	po_number_list = col_po_number.tolist()
	po_date_list = col_po_date.tolist()
	invoice_date_list = col_invoice_date.tolist()
	pay_date_list = col_pay_date.tolist()

	print(po_date_list[5])
	print(type(po_date_list[5]))
	dt_po_date_list = []
	dt_invoice_date_list = []
	dt_pay_date_list = []

	for i in range(len(po_date_list)):
		dt_po_date_list.append(datetime.strptime(po_date_list[i], "%Y-%m-%d"))
		dt_invoice_date_list.append(datetime.strptime(invoice_date_list[i], "%Y-%m-%d"))
		dt_pay_date_list.append(datetime.strptime(pay_date_list[i], "%Y-%m-%d"))
		
	print(dt_po_date_list[5])
	print(type(dt_po_date_list[5]))		
	
	print("This dataset has", len(po_date_list), "entries\n")

	unique_po_number_list = set(po_number_list)
	print("This dataset has entries for", len(unique_po_number_list), "unique PO numbers\n")
	
	#row = x.loc[x['Size'] == '128.0 Gal']	
	#print(row)

	x["PODate"] = dt_po_date_list
	x["InvoiceDate"] = dt_invoice_date_list
	x["PayDate"] = dt_pay_date_list
	return x

print(invoice2016_read("archive/InvoicePurchases12312016.csv"))
