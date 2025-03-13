import pandas as pd
import matplotlib.pyplot as plt

def plot_cityCategory(df):
    '''Categorize the cities into 3 group and visualize their distribution
    
    Input:
        df(pd.DataFrame): dataframe of the sales data
    
    Output:
        None, show two pie plot
    '''
    assert isinstance(df, pd.DataFrame)
    assert 'City' in df.columns, 'City column is missing'
    assert 'SalesDollars' in df.columns, 'SalesDollars column is missing'
    
    # Give category for the city by total sales into 3 groups, by the total sales
    df['Category'] = pd.cut(df['SalesDollars'], bins=3, labels=['Low sales', 'Medium sales', 'High sales'])
    city_sum = df.groupby('Category').agg({'SalesDollars': 'sum', 'Category': 'count'})
    
    # Visualize the city count and sales distribution for each category
    plt.subplot(1, 2, 1)
    plt.pie(city_sum['Category'], labels=city_sum.index, autopct='%1.1f%%', startangle=170, colors=['lightblue', 'orange', 'seagreen'])
    plt.title("City Distribution")
    plt.subplot(1, 2, 2)
    plt.pie(city_sum['SalesDollars'], labels=city_sum.index, 
            autopct='%1.1f%%', startangle=170, colors=['lightblue', 'orange', 'seagreen'])
    plt.title("Sales Distribution")
    plt.show()