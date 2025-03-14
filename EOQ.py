# Import the necessary modules 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import regex as re
import datetime
from scipy import stats
import regex as re

def pre_process_size(string):
    """
    Pre-processes a size string by extracting numerical values and their corresponding units,
    then converts the values to a standardized milliliter (mL) format.

    Parameters:
    string (str): A string containing numerical values and units.

    Returns:
    float: The equivalent size in milliliters (mL).
    """
    assert isinstance(string, str), "Input must be a string"
    
    numbers = [i[0] for i in re.findall(r'(\d+(\.\d+)?)', string)]
    units = re.findall(r'[a-zA-Z]+', string)

    # Ensure numbers and units are of equal length
    if len(units) != len(numbers):
        if len(units) < len(numbers):
            for _ in range(len(numbers) - len(units)):
                units.append(None)
        else:
            for _ in range(len(units) - len(numbers)):
                numbers.append('1')
    
    dictionary = {}
    for i in range(len(numbers)):
        dictionary[float(numbers[i])] = units[i]
    
    answer = 1
    for key, value in dictionary.items():
        if value is None:
            answer *= key
        elif value.lower() in ['ml', 'milliliter', 'millilitre']:
            answer *= key
        elif value.lower() in ['l', 'liter', 'litre']:
            answer = 1000 * key
        elif value.lower() in ['oz']:
            answer = 30 * key
        elif value.lower() in ['pk']:
            answer *= key
    
    return answer
#Function to calculate EOQ

def calculate_EOQ(df_row):
    brand = int(df_row['Brand'])
    try :
        S = df['CPO']
    except:
        S=30
        D = 1.1 * df_row['TotalSaleQuantity']  # Should be changed to demand data.
        H = 0.25 * purchases_2017_df.loc[purchases_2017_df['Brand']==brand]['PurchasePrice'].values[0]

    return int(np.ceil(np.sqrt(2*D*S/H)))
    
def EOQ():
    # Define the file paths as a variable
    sales = read_zip('archive\SalesFINAL12312016.csv')
    invoices = read_zip('archive\InvoicePurchases12312016.csv')
    beginning = read_zip('archive\BegInvFINAL12312016.csv')
    ending = read_zip('archive\EndInvFINAL12312016.csv')
    purchases_2016 = read_zip('archive\PurchasesFINAL12312016.csv')
    purchases_2017 = read_zip('archive\2017PurchasePricesDec.csv')
    
    #Load all dataframes
    
    sales_df = pd.read_csv(sales,parse_dates=['SalesDate'])
    invoices_df = pd.read_csv(invoices,parse_dates=['InvoiceDate','PODate','PayDate'])
    beginning_df = pd.read_csv(beginning,parse_dates=['startDate'])
    ending_df = pd.read_csv(ending,parse_dates=['endDate'])
    purchases_2016_df = pd.read_csv(purchases_2016,parse_dates=['PODate','ReceivingDate','InvoiceDate','PayDate'])
    purchases_2017_df = pd.read_csv(purchases_2017)

    # Mapping the brand with the city of store
    brand_city_mapping = ending_df.groupby('Brand')['City'].apply(lambda x: list(x)[0]).to_dict()
    
    # Cleaning the df for SalesFINAL12312016.csv file
    categorical_columns = ['InventoryId','Description','VendorName']
    integer_columns = ['Store','Brand','Size','SalesQuantity','Volume','Classification','VendorNo']
    sales_df['Size'] = sales_df['Size'].apply(lambda x: pre_process_size(x))
    for col in categorical_columns:
        sales_df[col]=sales_df[col].astype('category')
    for col in integer_columns:
        sales_df[col]=sales_df[col].astype('int')
    
    #Checking for NA values
    sales_df.isna().sum(),sales_df.dtypes
    
    # Cleaning the df for the BegInvFINAL12312016.csv File
    categorical_columns = ['InventoryId','Description','City']
    integer_columns = ['Store','Brand','Size','onHand']
    beginning_df['Size'] = beginning_df['Size'].apply(lambda x: pre_process_size(x))
    for col in categorical_columns:
        beginning_df[col]=beginning_df[col].astype('category')
    for col in integer_columns:
        beginning_df[col]=beginning_df[col].astype('int')
    
    #Checking for NA values
    beginning_df.isna().sum(),beginning_df.dtypes
    
    # Cleaning the df for the EndInvFINAL12312016.csv File
    categorical_columns = ['InventoryId','Description','City']
    integer_columns = ['Store','Brand','Size','onHand']
    ending_df['Size'] = ending_df['Size'].apply(lambda x: pre_process_size(x))
    ending_df['City'] = ending_df['City'].fillna(ending_df['Brand'].map(brand_city_mapping))
    for col in categorical_columns:
        ending_df[col]=ending_df[col].astype('category')
    for col in integer_columns:
        ending_df[col]=ending_df[col].astype('int')
    
    # Found one row with no brand , hence dropping the specific row
    ending_df = ending_df.dropna()
    ending_df.isna().sum(),ending_df.dtypes
    
    #Cleaning the PurchasesFINAL12312016.csv file
    purchases_2016_df = purchases_2016_df.dropna()
    categorical_columns = ['InventoryId','Description','VendorName']
    integer_columns = ['Store','Brand','Size','VendorNumber','PONumber','Quantity','Classification']
    purchases_2016_df['Size'] = purchases_2016_df['Size'].apply(lambda x: pre_process_size(x))
    
    for col in categorical_columns:
        purchases_2016_df[col]=purchases_2016_df[col].astype('category')
    for col in integer_columns:
        purchases_2016_df[col]=purchases_2016_df[col].astype('int')
    
    # Checking for NA values
    purchases_2016_df.isna().sum(),purchases_2016_df.dtypes
    
    # Cleaning the InvoicePurchases12312016.csv file
    categorical_columns = ['VendorName']
    integer_columns = ['VendorNumber','PONumber','Quantity']
    float_columns = ['Dollars','Freight']
    for col in categorical_columns:
        invoices_df[col]=invoices_df[col].astype('category')
    for col in integer_columns:
        invoices_df[col]=invoices_df[col].astype('int')
    for col in float_columns:
        invoices_df[col]=invoices_df[col].astype('float')
    invoices_df.drop(columns=['Approval'],inplace=True)
    
    #Checking for NA values
    invoices_df.isna().sum(),invoices_df.dtypes
    
    #Cleaning the 2017PurchasePricesDec.csv file
    purchases_2017_df['Volume'] = purchases_2017_df['Volume'].replace('Unknown',np.nan)
    
    purchases_2017_df.dropna(inplace=True)
    categorical_columns = ['Description','VendorName']
    integer_columns = ['Brand','VendorNumber','Volume','Classification']
    purchases_2017_df['Size'] = purchases_2017_df['Size'].apply(lambda x: pre_process_size(x))
    for col in categorical_columns:
        purchases_2017_df[col]=purchases_2017_df[col].astype('category')
    for col in integer_columns:
        purchases_2017_df[col]=purchases_2017_df[col].astype('float')
    
    # Check for NA values
    purchases_2017_df.isna().sum(),purchases_2017_df.dtypes

    # Lead time plot for 2016 data

    purchases_2016_df['LeadTime'] = (purchases_2016_df['ReceivingDate'] - purchases_2016_df['PODate']).dt.days
    
    lead_time_df = purchases_2016_df.groupby('Brand').agg(MaxLeadTime=('LeadTime','max'),MinLeadTime=('LeadTime','min'),AvgLeadTime=('LeadTime','mean'))
    lead_time_df['AvgLeadTime'] = lead_time_df['AvgLeadTime'].round(0).astype('int')
    
    #Get the starting inventory data for each brand
    starting_inventory_by_brand = beginning_df.groupby('Brand')[['onHand','Price']].agg({'onHand':'sum','Price':'mean'}).reset_index()
    starting_inventory_by_brand.columns = ['Brand','Quantity','Price']
    
    #Get the ending inventory for each brand
    ending_inventory_by_brand = ending_df.groupby('Brand')[['onHand','Price']].agg({'onHand':'sum','Price':'mean'}).reset_index()
    ending_inventory_by_brand.columns = ['Brand','Quantity','Price']
    ending_inventory_by_brand['TotalValue'] = ending_inventory_by_brand['Quantity'] * ending_inventory_by_brand['Price']

    #For the 2016 purchases file, get the investment into each brand

    purchases_by_brand_16 = purchases_2016_df[purchases_2016_df['InvoiceDate']<=datetime.datetime(2016,12,31)].groupby('Brand')[['Quantity','PurchasePrice']].agg({'Quantity':'sum','PurchasePrice':'mean'}).reset_index()
    purchases_by_brand_16.columns = ['Brand','Quantity','Price']
    
    investment_16 = pd.concat([purchases_by_brand_16,starting_inventory_by_brand],ignore_index=True)
    investment_16 = investment_16.groupby('Brand').agg({'Quantity':'sum','Price':'mean'}).reset_index()
    investment_16['Investment'] = investment_16['Quantity']*investment_16['Price']

    #Ending inventory for the 2016 file
    
    ending_inventory_by_brand.columns=['Brand',	'Quantity','Price','Total_sale']
    stock = investment_16.merge(ending_inventory_by_brand,on='Brand',suffixes=('_invest','_sale'))
    stock['StockLeft'] = stock['Quantity_invest']-stock['Quantity_sale']
    
    #Get the purchase data for each brand
    purchases_by_brand = purchases_2016_df[purchases_2016_df['InvoiceDate']<datetime.datetime(2016,3,1)].groupby('Brand')[['Quantity','PurchasePrice']].agg({'Quantity':'sum','PurchasePrice':'mean'}).reset_index()
    purchases_by_brand.columns = ['Brand','Quantity','Price']
    
    # To calculate Order Cost, we use purchases and find the average order cost of each product. (H)
    
    avg_order_cost = purchases_2016_df[purchases_2016_df['InvoiceDate']<=datetime.datetime(2016,12,31)].groupby('Brand')[['Quantity','PurchasePrice','Dollars']].agg(TotalOrderQuantity=('Quantity','sum'),AvgProductCost=('PurchasePrice','mean'),AvgOrderValue=('Dollars','mean'),TotalOrderCost=('Dollars','sum')).reset_index()
    avg_order_cost = avg_order_cost.set_index('Brand')
    
    avg_sale_price = sales_df.groupby('Brand').agg(TotalSaleQuantity=('SalesQuantity','sum'),TotalSales=('SalesDollars','sum'),AvgSalePrice=('SalesPrice','mean')).reset_index()
    
    #Single merge
    single_merge = invoices_df[['PONumber','Quantity','Freight']].merge(purchases_2016_df[["PONumber", "Brand"]],on='PONumber',how='inner')

    #Merged Invoices
    merged_invoices = single_merge.merge(purchases_2017_df[["Brand", "Volume"]],on='Brand',how='inner')
    
    merged_invoices["VolQuantity"] = merged_invoices["Quantity"] * merged_invoices["Volume"]
    merged_invoices["VolQuantityTotal"] = merged_invoices.groupby("PONumber")['VolQuantity'].transform('sum')
    merged_invoices['CPO'] = merged_invoices["VolQuantity"] / merged_invoices["VolQuantityTotal"] * merged_invoices["Freight"]
    
    #After merging by invoices group by brand
    
    S = merged_invoices.groupby('Brand').agg({'CPO':'mean'})
    
    #Create a df for EOQ
    
    eoq_df = avg_sale_price.merge(S,on='Brand',how='inner')
    eoq_df.fillna(eoq_df.mean(),inplace=True)
    
    safety_df = sales_df.groupby('Brand').agg(MinSalesQty=('SalesQuantity','min'),MaxSalesQty=('SalesQuantity','max'),TotalSalesQty=('SalesQuantity','sum'),AvgSalesQty=('SalesQuantity','mean'),AvgSalePrice=('SalesDollars','mean'))
    safety_df['AvgSalesQty']=safety_df['AvgSalesQty'].round(0).astype(int)
    # safety_df
    safety_stock_df = safety_df.merge(lead_time_df,on='Brand')
    safety_stock_df['SafetyStock'] = (safety_stock_df['MaxLeadTime'] * safety_stock_df['MaxSalesQty'] ) - (safety_stock_df['AvgLeadTime'] * safety_stock_df['AvgSalesQty'])
    # safety_stock_df
    
    #For the 2016 purchases file, get the investment into each brand
    
    purchases_by_brand_16 = purchases_2016_df[purchases_2016_df['InvoiceDate']<=datetime.datetime(2016,12,31)].groupby('Brand')[['Quantity','PurchasePrice']].agg({'Quantity':'sum','PurchasePrice':'mean'}).reset_index()
    purchases_by_brand_16.columns = ['Brand','Quantity','Price']

    
    
    investment_16 = pd.concat([purchases_by_brand_16,starting_inventory_by_brand],ignore_index=True)
    investment_16 = investment_16.groupby('Brand').agg({'Quantity':'sum','Price':'mean'}).reset_index()
    investment_16['Investment'] = investment_16['Quantity']*investment_16['Price']

    #Ending inventory for the 2016 file
    
    ending_inventory_by_brand.columns=['Brand',	'Quantity','Price','Total_sale']
    stock = investment_16.merge(ending_inventory_by_brand,on='Brand',suffixes=('_invest','_sale'))
    stock['StockLeft'] = stock['Quantity_invest']-stock['Quantity_sale']
    
    #Get the ending inventory for each brand
    ending_inventory_by_brand = ending_df.groupby('Brand')[['onHand','Price']].agg({'onHand':'sum','Price':'mean'}).reset_index()
    ending_inventory_by_brand.columns = ['Brand','Quantity','Price']
    ending_inventory_by_brand['TotalValue'] = ending_inventory_by_brand['Quantity'] * ending_inventory_by_brand['Price']
    
    #Ending inventory for the 2016 file
    
    ending_inventory_by_brand.columns=['Brand',	'Quantity','Price','Total_sale']
    stock = investment_16.merge(ending_inventory_by_brand,on='Brand',suffixes=('_invest','_sale'))
    stock['StockLeft'] = stock['Quantity_invest']-stock['Quantity_sale']
    
    # Perform the EOQ on the eoq_df
    eoq_df['EOQ']  = eoq_df.apply(lambda x:calculate_EOQ(x),axis=1)
    
    #Plot the EOQ Figures
    fig,ax = plt.subplots(1,2,figsize=(10,4))
    sns.histplot(data=eoq_df,x='EOQ',ax=ax[0],bins=50)
    ax[0].set(xlabel='EOQ (Units)',ylabel='Frequency',title='Histogram')
    ax[0].set_yscale('log')
    
    sns.kdeplot(data=eoq_df,x='EOQ',ax=ax[1])
    ax[1].set(xlabel='EOQ (Units)',title='Kernel Density Estimate',ylabel='Density')
    ax[1].set_yscale('log')
    ax[1].set_yticklabels(labels='')
    
    fig.suptitle('EOQ')

    plt.show()
    
    # Create Pltos for the Actual and optimal stocks
    
    recommended_stock = safety_stock_df.merge(eoq_df,on='Brand')
    recommended_stock['RecommendedStock']= recommended_stock['EOQ'] + recommended_stock['SafetyStock']
    
    rec_stock = ending_inventory_by_brand[['Brand','Quantity']].merge(recommended_stock[['Brand','RecommendedStock']],on='Brand',how='inner')
    
    fig,ax = plt.subplots(1,1,figsize=(8,6))
    sns.histplot(data=rec_stock,x='Quantity',ax=ax,label='Actual Stock',binwidth=500,alpha=0.7)
    sns.histplot(data=rec_stock,x='RecommendedStock',ax=ax,color='r',fill=False,label='Optimal Stock',binwidth=500)
    ax.set_yscale('log')
    ax.set(xlabel='Product ID',ylabel='Amount of Stock(Units)',title='Recommended Stock')
    ax.legend()
    plt.show()

if __name__ == '__main__':
    EOQ()