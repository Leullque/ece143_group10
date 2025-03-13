import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def plot_dailysale(df):
    ''' Visualize the total daily sales
    
    Input:
        df(pd.DataFrame): dataframe of the sales data
        
    Output:
        None, show the line chart
    '''
    assert isinstance(df, pd.DataFrame)
    assert 'SalesDate' in df.columns
    assert 'SalesDollars' in df.columns
    
    df['month'] = df['SalesDate'].dt.month
    ticks = []
    sales_by_store = df[df['month'] == 1]
    sales_by_store = sales_by_store.groupby('SalesDate')[['SalesDollars']].agg({'SalesDollars':'sum'})
    sales_by_store = sales_by_store.sort_index()
    ticks = [date.strftime('%b %d') for date in sales_by_store.index]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=sales_by_store, x=sales_by_store.index, y='SalesDollars', 
                marker='o', ax=ax, color='c')

    ax.set(xlabel='Date', ylabel='Total Sales ($)', title='Daily Sales Over Time')
    xticks = list(range(0, len(ticks), 7))
    if len(ticks)-1 not in xticks:
        xticks.append(-1)
    ax.set_xticks(sales_by_store.index[xticks])
    ax.set_xticklabels([ticks[i] for i in xticks], rotation=45, ha='right')
    ax.grid(True, linestyle='--', alpha=0.6)

    plt.show()