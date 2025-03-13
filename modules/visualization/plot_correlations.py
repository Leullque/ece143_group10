import matplotlib.pyplot as plt
import pandas as pd
def plot_correlations(df, title):
    '''Plot correlation scatter plots for df
    
    Input: 
        df: dataframe with columns 'onHand', 'Weighted_Avg_Price'
        title: str, title of the plot
    
    Output: none, show the scatter plot
    '''
    assert isinstance(df, pd.DataFrame)
    assert 'onHand' in df.columns
    assert 'Weighted_Avg_Price' in df
    assert isinstance(title, str)
    
    plt.scatter(df['onHand'], df['Weighted_Avg_Price'], color='c', marker='o')
    plt.xlabel('Stock Quantity for each sotre')
    plt.ylabel('Average price in each store($)')
    plt.title(title)
    plt.show()