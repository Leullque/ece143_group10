import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
def plot_gaussian(df):
    '''Draw the distribution fit it to a Gaussian distribution
    
    Inputs:
        df(pd.DataFrame): dataframe of the vendor data
    
    Output:
        None, show the plot
    '''
    assert isinstance(df, pd.DataFrame)
    assert 'LeadTime' in df.columns
    
    mu, sigma = df['LeadTime'].mean(), df['LeadTime'].std()
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)

    plt.figure(figsize=(10, 5))
    sns.kdeplot(df['LeadTime'], fill=True, label='KDE', color='c')

    plt.plot(x, stats.norm.pdf(x, mu, sigma), label='Gaussian Fit', linestyle='dashed', color='salmon')

    plt.xlabel('Average Lead Time (days)')
    plt.ylabel('Density')
    plt.title('Gaussian Distribution of Average Lead Time by Vendor')
    plt.legend()
    plt.show()