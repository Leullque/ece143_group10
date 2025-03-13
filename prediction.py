import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
import zipfile
import re

def read_zip(fname):
    """
    Reads a CSV file from a ZIP archive and returns it as a Pandas DataFrame.
    
    Args:
        fname (str): Path to the ZIP file.
    
    Returns:
        pd.DataFrame: The extracted dataset.
    """
    with zipfile.ZipFile(fname, 'r') as z:
        with z.open(z.namelist()[0]) as f:
            return pd.read_csv(f)

def extract_city(inventory_id):
    """
    Extracts the city name from the InventoryId using regex.
    
    Args:
        inventory_id (str): Inventory ID containing the city name.
    
    Returns:
        str: Extracted city name or None if not found.
    """
    match = re.search(r'_(.*?)_', inventory_id)
    return match.group(1) if match else None

def feature_engineering(df_Sales):
    """
    Performs feature engineering on the sales dataset.
    
    Steps:
    - Extracts city from InventoryId.
    - Converts SalesDate to datetime format and extracts the weekday.
    - Drops unnecessary columns.
    - Aggregates sales quantity for unique feature combinations.
    - Encodes City as a categorical numerical feature.
    
    Args:
        df_Sales (pd.DataFrame): Raw sales dataset.
    
    Returns:
        pd.DataFrame: Processed dataset.
        dict: Mapping of city codes to original names.
    """
    # Extract city name
    df_Sales['City'] = df_Sales['InventoryId'].apply(extract_city)
    # Convert date
    df_Sales['SalesDate'] = pd.to_datetime(df_Sales['SalesDate'], format='%m/%d/%Y')
    # Extract weekday
    df_Sales['Weekday'] = df_Sales['SalesDate'].dt.weekday 
    
    # Drop unnecessary columns
    df_Sales = df_Sales.drop(columns=['SalesDollars', 'VendorName', 'SalesDate', "ExciseTax", "Description", "InventoryId", "Size"], errors='ignore')
    
    # Aggregate sales quantity for unique feature combinations
    df_Sales = df_Sales.groupby(df_Sales.columns.drop('SalesQuantity').tolist(), as_index=False)['SalesQuantity'].sum()
    
    # Encode City as a categorical numerical feature
    df_Sales['City'] = df_Sales['City'].astype('category')
    city_mapping = dict(enumerate(df_Sales['City'].cat.categories))  # Store mapping
    df_Sales['City'] = df_Sales['City'].cat.codes
    
    return df_Sales, city_mapping

def dataset_split(df_Sales):
    """
    Splits the dataset into training and testing sets.
    
    Args:
        df_Sales (pd.DataFrame): Processed dataset.
    
    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    X = df_Sales.drop(columns=['SalesQuantity'])  # Features
    y = df_Sales['SalesQuantity']  # Target variable
    return train_test_split(X, y, test_size=0.2)

def train_and_test(X_train, X_test, y_train, y_test, model):
    """
    Trains a given model and evaluates its performance using MAE and MSE.
    
    Args:
        X_train (pd.DataFrame): Training features.
        X_test (pd.DataFrame): Testing features.
        y_train (pd.Series): Training target.
        y_test (pd.Series): Testing target.
        model: Scikit-learn regression model.
    
    Returns:
        tuple: (Mean Absolute Error, Mean Squared Error)
    """
    model.fit(X_train, y_train)  # Train model
    y_pred = model.predict(X_test)  # Predict
    return mean_absolute_error(y_test, y_pred), mean_squared_error(y_test, y_pred)

def analysis():
    """
    Runs multiple regression models on the dataset and compares their performance.
    
    Returns:
        pd.DataFrame: Model performance metrics.
    """
    dataset_Sales = read_zip("archive/cleaned_Sales.csv.zip")
    df_Sales, _ = feature_engineering(dataset_Sales.copy())
    X_train, X_test, y_train, y_test = dataset_split(df_Sales)
    
    # Initialize models
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0),
        "Random Forest": RandomForestRegressor(n_estimators=100),
        "KNN": KNeighborsRegressor(n_neighbors=5)
    }
    
    # Evaluate models
    results = {"Model": [], "MAE": [], "MSE": []}
    for name, model in models.items():
        mae, mse = train_and_test(X_train, X_test, y_train, y_test, model)
        results["Model"].append(name)
        results["MAE"].append(round(mae, 2))
        results["MSE"].append(round(mse, 2))
    
    return pd.DataFrame(results)

def actual_vs_predicted_rf():
    """
    Trains a Random Forest model and returns actual vs predicted values.
    
    Returns:
        tuple: (Actual values, Predicted values)
    """
    dataset_Sales = read_zip("archive/cleaned_Sales.csv.zip")
    df_Sales, _ = feature_engineering(dataset_Sales.copy())
    X_train, X_test, y_train, y_test = dataset_split(df_Sales)
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)
    return y_test, model.predict(X_test)

if __name__ == '__main__':
    model_performance = analysis()
    
    # Print model performance results
    for i, model in enumerate(model_performance["Model"]):
        mae = model_performance["MAE"][i]
        mse = model_performance["MSE"][i]
        print(f"{model}: - MAE: {mae}, MSE: {mse}")
