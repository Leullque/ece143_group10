import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
def plot_byweekday(df):
    ''' Visualize the total sales by weekdays
    
    Input:
        df(pd.DataFrame): dataframe of the sales data
        
    Output:
        None, show bar plot
    '''
    assert isinstance(df, pd.DataFrame)
    assert 'SalesDate' in df.columns, 'SalesDate column is missing'
    assert 'SalesDollars' in df.columns, 'SalesDollars column is missing'
    
    df['Weekday'] = df['SalesDate'].dt.weekday
    sales_by_weekday = df[df['month'] == 1]
    sales_by_weekday = sales_by_weekday.groupby('Weekday')[['SalesDollars']].agg({'SalesDollars':'sum'})
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=sales_by_weekday, x=sales_by_weekday.index, y='SalesDollars', ax=ax, color='c')
    ax.set(xlabel='Weekday', ylabel='Total Sales ($)', title='Total Sales by Weekday')
    ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    plt.show()