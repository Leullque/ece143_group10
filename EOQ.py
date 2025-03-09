import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import regex as re
import datetime
from scipy import stats

def EOQ():
    df_pur2017 = pd.read_csv('archive/2017PurchasePricesDec.csv')
    df_pur2016 = pd.read_csv('archive/PurchasesFINAL12312016.csv')
    df_invoice = pd.read_csv('archive/InvoicePurchases12312016.csv')
    df_sale = pd.read_csv('archive/cleaned_Sales.csv')
    
    df_invoice['InvoiceDate'] = pd.to_datetime(df_invoice['InvoiceDate'])
    df_invoice['PayDate'] = pd.to_datetime(df_invoice['PayDate'])
    df_pur2016['InvoiceDate'] = pd.to_datetime(df_pur2016['InvoiceDate'])
    df_pur2016['ReceivingDate'] = pd.to_datetime(df_pur2016['ReceivingDate'])
    df_pur2016['PODate'] = pd.to_datetime(df_pur2016['PODate'])
    

    avg_order_cost = df_pur2016[df_pur2016['InvoiceDate']
        <=datetime.datetime(2016,12,31)].groupby('Brand')[[
            'Quantity','PurchasePrice','Dollars']].agg(
            TotalOrderQuantity=('Quantity','sum'),
            AvgProductCost=('PurchasePrice','mean'),
            AvgOrderValue=('Dollars','mean'),
            TotalOrderCost=('Dollars','sum')).reset_index()
    avg_order_cost = avg_order_cost.set_index('Brand')

    avg_sale_price = df_sale.groupby('Brand').agg(TotalSaleQuantity=('SalesQuantity','sum'),
                                                  TotalSales=('SalesDollars','sum'),
                                                  AvgSalePrice=('SalesPrice','mean')).reset_index()
    #Single merge
    single_merge = df_invoice[['PONumber','Quantity','Freight']].merge(df_pur2016[["PONumber", "Brand"]],on='PONumber',how='inner')

    #Merged Invoices
    merged_invoices = single_merge.merge(df_pur2017[["Brand", "Volume"]],on='Brand',how='inner')

    merged_invoices["VolQuantity"] = merged_invoices["Quantity"] * merged_invoices["Volume"]
    merged_invoices["VolQuantityTotal"] = merged_invoices.groupby("PONumber")['VolQuantity'].transform('sum')
    merged_invoices['CPO'] = merged_invoices["VolQuantity"] / merged_invoices["VolQuantityTotal"] * merged_invoices["Freight"]
    print(merged_invoices.head())
if __name__ == '__main__':
    EOQ()