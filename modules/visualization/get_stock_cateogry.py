import numpy as np
from scipy import stats

# Based on the stock left percentile, assignt the category
stock_categories={
    0:'Out of Stock',
    1: 'Re order',
    2: 'Slow Moving Stock',
    3: 'Excess/Obsolete',
}
def get_stock_category(df):
    ''' Assign category to each store based on their stock status
    
    Input:
        df(pd.DataFrame): dataframe of the stock data
    
    Output:
        int: the category of the stock
    '''
    begin,end = df['Quantity_invest'], df['StockLeft']

    if ~np.isnan(begin)  and ~np.isnan(end):
        percentile = stats.percentileofscore(np.arange(0,begin),end)

        if end<0:
            return 0
        if end==0 and begin>0:
            return 0
        if percentile<=30:
            return 1
        if percentile>30 and percentile<=75:
            return 2
        if percentile>75 and percentile<=100:
            return 3
            
    if begin==0 and np.isnan(end):
        return 0
    
    if np.isnan(begin) and ~np.isnan(end):
        return 4

    if ~np.isnan(begin) and np.isnan(end):
        return 0