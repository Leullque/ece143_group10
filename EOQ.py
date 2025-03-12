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
    #After merging by invoices group by brand

    S = merged_invoices.groupby('Brand').agg({'CPO':'mean'})

    #Create a df for EOQ

    eoq_df = avg_sale_price.merge(S,on='Brand',how='inner')
    eoq_df.fillna(eoq_df.mean(),inplace=True)
    #Function to calculate EOQ

    def calculate_EOQ(df_row):
        brand = int(df_row['Brand'])
        try :
            S = df_row['CPO']
        except:
            S=30
        D = 1.1 * df_row['TotalSaleQuantity']  # Should be changed to demand data.
        H = 0.25 * df_pur2017.loc[df_pur2017['Brand']==brand]['PurchasePrice'].values[0]

        return int(np.ceil(np.sqrt(2*D*S/H)))
    
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

    ending_inventory_by_brand = df_end.groupby('Brand')[['onHand','Price']].agg({'onHand':'sum','Price':'mean'}).reset_index()
    ending_inventory_by_brand.columns = ['Brand','Quantity','Price']
    ending_inventory_by_brand['TotalValue'] = ending_inventory_by_brand['Quantity'] * ending_inventory_by_brand['Price']
    ending_inventory_by_brand.columns=['Brand',	'Quantity','Price','Total_sale']
    stock = investment_16.merge(ending_inventory_by_brand,on='Brand',suffixes=('_invest','_sale'))
    stock['StockLeft'] = stock['Quantity_invest']-stock['Quantity_sale']
    
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