import pandas as pd
import numpy as np
import datetime
import gc

def EOQ():
    # Load large CSVs in chunks (if needed)
    df_pur2017 = pd.read_csv('archive/2017PurchasePricesDec.csv', dtype={'Volume': 'float32'})
    df_pur2016 = pd.read_csv('archive/PurchasesFINAL12312016.csv', 
                             usecols=['PONumber', 'Brand', 'Quantity', 'PurchasePrice', 'Dollars', 'InvoiceDate', 'ReceivingDate', 'PODate'],
                             parse_dates=['InvoiceDate', 'ReceivingDate', 'PODate'])
    df_invoice = pd.read_csv('archive/InvoicePurchases12312016.csv', 
                             usecols=['PONumber', 'Quantity', 'Freight', 'InvoiceDate', 'PayDate'], 
                             parse_dates=['InvoiceDate', 'PayDate'])
    df_sale = pd.read_csv('archive/cleaned_Sales.csv', 
                          usecols=['Brand', 'SalesQuantity', 'SalesDollars', 'SalesPrice'])

    # Optimize data types
    df_pur2016['Quantity'] = df_pur2016['Quantity'].astype('int32')
    df_pur2016['PurchasePrice'] = df_pur2016['PurchasePrice'].astype('float32')
    df_pur2016['Dollars'] = df_pur2016['Dollars'].astype('float32')

    df_invoice['Quantity'] = df_invoice['Quantity'].astype('int32')
    df_invoice['Freight'] = df_invoice['Freight'].astype('float32')

    # Aggregate Order Cost
    avg_order_cost = df_pur2016[df_pur2016['InvoiceDate'] <= datetime.datetime(2016, 12, 31)].groupby('Brand').agg(
        TotalOrderQuantity=('Quantity', 'sum'),
        AvgProductCost=('PurchasePrice', 'mean'),
        AvgOrderValue=('Dollars', 'mean'),
        TotalOrderCost=('Dollars', 'sum')
    ).reset_index().set_index('Brand')

    # Aggregate Sales Price
    avg_sale_price = df_sale.groupby('Brand').agg(
        TotalSaleQuantity=('SalesQuantity', 'sum'),
        TotalSales=('SalesDollars', 'sum'),
        AvgSalePrice=('SalesPrice', 'mean')
    ).reset_index()

    # Step 1: Merge Invoice & Purchase Data
    single_merge = df_invoice[['PONumber', 'Quantity', 'Freight']].merge(
        df_pur2016[['PONumber', 'Brand']], on='PONumber', how='inner')

    # Step 2: Merge with Volume Data
    merged_invoices = single_merge.merge(
        df_pur2017[['Brand', 'Volume']], on='Brand', how='inner')

    # Process in Chunks to Prevent Kernel Crash
    chunk_size = 50000  # Adjust based on available memory
    chunks = []

    for chunk in np.array_split(merged_invoices, len(merged_invoices) // chunk_size + 1):
        chunk["VolQuantity"] = chunk["Quantity"] * chunk["Volume"]
        chunk["VolQuantityTotal"] = chunk.groupby("PONumber")["VolQuantity"].transform('sum')
        chunk['CPO'] = chunk["VolQuantity"] / chunk["VolQuantityTotal"] * chunk["Freight"]
        chunks.append(chunk)

    # Reassemble the DataFrame
    merged_invoices = pd.concat(chunks, ignore_index=True)

    # Print Sample Output
    print(merged_invoices.head())

    # Free Up Memory
    del df_pur2016, df_pur2017, df_invoice, df_sale, single_merge, chunks
    gc.collect()

if __name__ == '__main__':
    EOQ()