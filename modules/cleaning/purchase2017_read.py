import pandas as pd
from datetime import datetime

def purchase2017_read(filename):  
	'''                                                                 
	Reads the csv and cleans up the data to get it ready for analysis.
	Brand can be used to match the entire row with its corresponding row with the output from purchase2016_read
	                                                                    
	filename:= filename with relative path to the purchases2016 csv
	x:= a pd.DataFrame object with ID as index and Timestamp as a column                                         
	'''
	assert(type(filename)) == str, "Input filename should be a string"

	x = pd.read_csv(filename)
	assert type(x) == pd.DataFrame, "Input x should be a panda series"
	assert len(x) > 0, "Input x should be non-empty"

	col_size = x["Size"]
	size_list = col_size.tolist()

	print(len(size_list))	
	unique_size_list = set(size_list)
	print(len(unique_size_list))
	print(unique_size_list)


	
	#row = x.loc[x['Size'] == '128.0 Gal']	
	#print(row)

	return x

print(purchase2017_read("archive/2017PurchasePricesDec.csv"))
