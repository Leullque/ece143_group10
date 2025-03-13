import pandas as pd
import matplotlib.pyplot as plt
def plot_stock(df):
    '''
    Plot the stock shown in df and the average price in each store.
    
    Input(pd.DataFrame): df, a dataframe with columns 'Store', 'onHand', and 'Price'.
    
    Output(plt.Figure): a bar plot showing the stock in each store and the average price in each store.
    '''
    assert isinstance(df, pd.DataFrame)
    assert 'Store' in df.columns
    assert 'onHand' in df.columns
    assert 'Price' in df.columns
    
    df['onHand_Price'] = df['onHand'] * df['Price']
    store_counts = df.groupby('Store').agg({'onHand': 'sum', 'onHand_Price': 'sum'}).reset_index()
    store_counts['Weighted_Avg_Price'] = store_counts['onHand_Price'] / store_counts['onHand']

    store_counts.drop(columns=['onHand_Price'], inplace=True)
    df.drop(columns=['onHand_Price'], inplace=True)
    store_counts

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(store_counts['Store'], store_counts['onHand'], color='c', alpha=0.6)
    ax.set_xlabel('Store')
    ax.set_ylabel('Number of Items', color='c')
    ax.set_title('Stock and Average Price in Each Store')
    ax2 = ax.twinx()
    ax2.plot(store_counts['Store'], store_counts['Weighted_Avg_Price'], color='salmon', marker='o')
    ax2.set_ylabel('Average Price', color='salmon')
    return fig