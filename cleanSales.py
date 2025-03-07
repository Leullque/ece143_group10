import pandas as pd
import re

# ====== FUNCTION DEFINITIONS ======

def missing_data(df):
    """Returns the number of rows with missing data in a given DataFrame."""
    return df.isna().any(axis=1).sum()

def remove_whitespace(df, *columns):
    """Removes leading and trailing whitespaces from specified columns."""
    for column in columns:
        df[column] = df[column].str.strip()
    return df

def convert_to_ml(size):
    size = size.strip()  # Remove extra spaces

    # Convert Liter (L) to mL
    if "L" in size and "mL" not in size:
        match = re.match(r"(\d*\.?\d+)L", size)
        if match:
            return float(match.group(1)) * 1000  # Convert to mL
        
    # Standardize Liter notation
    if size == "Liter":
        return 1000

    # Convert pack sizes (e.g., "100mL 4 Pk" → 400mL or "4 Pk 100mL" → 400mL)
    match = re.match(r"(\d+)\s*mL\s+(\d+)\s*Pk", size)  # "100mL 4 Pk"
    if match:
        unit_size, count = map(int, match.groups())
        return unit_size * count

    match = re.match(r"(\d+)\s*Pk\s+(\d+)\s*mL", size)  # "4 Pk 100mL"
    if match:
        count, unit_size = map(int, match.groups())
        return unit_size * count

    # Convert single mL sizes (e.g., "750mL")
    match = re.match(r"(\d+)\s*mL", size)
    if match:
        return int(match.group(1))
    
    # Convert fluid ounces to milliliters
    oz_to_ml = {"5.0 Oz": "148", "22.0 Oz": "650"}
    if size in oz_to_ml:
        return oz_to_ml[size]
    
    # Handle mixed packs
    if "/" in size or "+" in size:
        return "Mixed Pack"




# ====== MAIN EXECUTION ======

# Load CSV file
sales_df = pd.read_csv("archive/SalesFINAL12312016.csv")

# Check for missing data
print("Number of missing rows in end_inv:", missing_data(sales_df), "\n")

# Remove whitespace
columns_to_clean = ['Description', 'SalesDate', 'VendorName']
sales_df = remove_whitespace(sales_df, *columns_to_clean)

# Analyze unique values
print("Number of unique Stores in sales_df:", sales_df['Store'].nunique())
print("Store distribution:\n", sales_df['Store'].value_counts())

print("\nNumber of unique Brands in sales_df:", sales_df['Brand'].nunique())
print("Brand distribution:\n", sales_df['Brand'].value_counts())

print("\nNumber of unique Descriptions in sales_df:", sales_df['Description'].nunique())
print("Description distribution:\n", sales_df['Description'].value_counts())

print("\nNumber of unique Classifications in sales_df:", sales_df['Classification'].nunique())
print("Classification distribution:\n", sales_df['Classification'].value_counts())

print("\nNumber of unique VendorNo in sales_df:", sales_df['VendorNo'].nunique())
print("VendorNo distribution:\n", sales_df['VendorNo'].value_counts())

print("\nNumber of unique Vendor Names in sales_df:", sales_df['VendorName'].nunique())
print("Vendor Name distribution:\n", sales_df['VendorName'].value_counts())

# Standardize Size column to mL or "Mixed Pack" for unclear size values
print("\nNumber of Unique sizes before standardization:", sales_df['Size'].nunique())
print("Distribution of unique Sizes before standardization:\n", sales_df['Size'].value_counts())

sales_df['Size'] = sales_df['Size'].apply(convert_to_ml)
print("\nNumber of Unique sizes after standardization:", sales_df['Size'].nunique())
print("Distribution of unique Sizes after standardization:\n", sales_df['Size'].value_counts())

# drop rows with "Mixed Pack" size ?
# sales_df = sales_df[sales_df['Size'] != "Mixed Pack"]
# print("Distribution of unique Sizes after standardization:\n", sales_df['Size'].value_counts())

# Convert 'Size' to numeric
sales_df['Size'] = pd.to_numeric(sales_df['Size'], errors='coerce')

# Get sum of the 'Size' column to make sure numeric
total_size = sales_df['Size'].sum()
print("\nSum of Size column:", total_size)


# Convert 'SalesDollars' to numeric
sales_df['SalesDollars'] = pd.to_numeric(sales_df['SalesDollars'], errors='coerce')

# Get sum of the 'SalesDollars' column to make sure numeric
total_sales_dollars = sales_df['SalesDollars'].sum()
print("\nSum of SalesDollars column:", total_sales_dollars)


# Convert 'SalesPrice' to numeric
sales_df['SalesPrice'] = pd.to_numeric(sales_df['SalesPrice'], errors='coerce')

# Get sum of the 'SalesPrice' column to make sure numeric
total_sales_price = sales_df['SalesPrice'].sum()
print("\nSum of SalesPrice column:", total_sales_price)

# Convert 'Volume' to numeric
sales_df['Volume'] = pd.to_numeric(sales_df['Volume'], errors='coerce')

# Get sum of the 'Volume' column to make sure numeric
total_volume = sales_df['Volume'].sum()
print("\nSum of Volume column:", total_volume)

# Convert 'ExciseTax' to numeric
sales_df['ExciseTax'] = pd.to_numeric(sales_df['ExciseTax'], errors='coerce')

# Get sum of the 'ExciseTax' column to make sure numeric
total_excise_tax = sales_df['ExciseTax'].sum()
print("\nSum of ExciseTax column:", total_excise_tax)


# Save the cleaned data 
sales_df.to_csv("archive/cleaned_Sales.csv", index=False)

