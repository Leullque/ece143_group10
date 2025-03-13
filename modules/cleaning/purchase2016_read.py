import pandas as pd
from datetime import datetime

def purchase2016_read(filename):  
	'''                                                                 
	Reads the csv and cleans up the data to get it ready for analysis.
	InventoryID gets broken down into store ID, city, and brand ID and adds these columns to the dataframe.
	Size field gets cleaned up and replaced with the converted volume.
	PODate, ReceivingDate, InvoiceDate, PayDate gets converted to date format.
	                                                                    
	filename:= filename with relative path to the purchases2016 csv
	x:= a pd.DataFrame object returned with the cleaned up data                                         
	'''
	assert(type(filename)) == str, "Input filename should be a string"

	x = pd.read_csv(filename)
	assert type(x) == pd.DataFrame, "Input x should be a panda series"
	assert len(x) > 0, "Input x should be non-empty"

	col_inventory_id = x["InventoryId"]
	col_size = x["Size"]
	col_po_number = x["PONumber"]
	col_po_date = x["PODate"]
	col_receiving_date = x["ReceivingDate"]
	col_invoice_date = x["InvoiceDate"]
	col_pay_date = x["PayDate"]
	
	inventory_id_list = col_inventory_id.tolist()
	size_list = col_size.tolist()
	po_number_list = col_po_number.tolist()
	po_date_list = col_po_date.tolist()
	receiving_date_list = col_receiving_date.tolist()
	invoice_date_list = col_invoice_date.tolist()
	pay_date_list = col_pay_date.tolist()

	print(po_date_list[5])
	print(type(po_date_list[5]))
	city_list = []
	dt_po_date_list = []
	dt_receiving_date_list = []
	dt_invoice_date_list = []
	dt_pay_date_list = []

	for i in range(len(inventory_id_list)):
		split_item = inventory_id_list[i].split("_")
		city_list.append(split_item[1])
		dt_po_date_list.append(datetime.strptime(po_date_list[i], "%Y-%m-%d"))
		dt_receiving_date_list.append(datetime.strptime(receiving_date_list[i], "%Y-%m-%d"))
		dt_invoice_date_list.append(datetime.strptime(invoice_date_list[i], "%Y-%m-%d"))
		dt_pay_date_list.append(datetime.strptime(pay_date_list[i], "%Y-%m-%d"))
		
	print(dt_po_date_list[5])
	print(type(dt_po_date_list[5]))		
	print("This dataset has ", len(po_date_list), "entries\n")
	
	unique_city_list = set(city_list)
	print("This dataset has data for", len(unique_city_list), "different cities\n")
	print(unique_city_list)
	
	unique_size_list = set(size_list)
	print("This dataset has purchases for", len(unique_size_list), "unique volumes of product\n")
	print(unique_size_list)

	unique_po_number_list = set(po_number_list)
	print("This dataset has entries for", len(unique_po_number_list), "unique PO numbers\n")
	
	#row = x.loc[x['Size'] == '128.0 Gal']	
	#print(row)

	x["City"] = city_list
	x["PODate"] = dt_po_date_list
	x["ReceivingDate"] = dt_receiving_date_list
	x["InvoiceDate"] = dt_invoice_date_list
	x["PayDate"] = dt_pay_date_list
	return x

print(purchase2016_read("archive/PurchasesFINAL12312016.csv"))
