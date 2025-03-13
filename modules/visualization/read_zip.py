import zipfile
import pandas as pd
def read_zip(fname):
    '''Read a ziped csv file into dataframe
    
    Input: 
        fname(str): input file name
        
    Output:
        pd.DataFrame: dataframe of the csv file
    
    '''
    assert isinstance(fname, str)
    assert fname.endswith('.zip'), 'Input file should be a zip file'
    with zipfile.ZipFile(fname, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            return pd.read_csv(f)