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
beg_inv = pd.read_csv("archive/BegInvFINAL12312016.csv")

# Check for missing data
print("Missing rows in beg_inv:", missing_data(beg_inv), "\n")


# Remove whitespace
columns_to_clean = ['City', 'Description']
beg_inv = remove_whitespace(beg_inv, *columns_to_clean)


# Drop duplicate data (uncomment if needed)
# beg_inv = beg_inv.drop_duplicates()

# Analyze unique values
print("Number of unique Stores in beg_inv:", beg_inv['Store'].nunique())
print("Store distribution:\n", beg_inv['Store'].value_counts())

print("\nNumber of unique Cities in beg_inv:", beg_inv['City'].nunique())
print("Cities distribution:\n", beg_inv['City'].value_counts())

print("\nNumber of unique Brands in beg_inv:", beg_inv['Brand'].nunique())
print("Brand distribution:\n", beg_inv['Brand'].value_counts())

print("\nNumber of unique Descriptions in beg_inv:", beg_inv['Description'].nunique())
print("Description distribution:\n", beg_inv['Description'].value_counts())

print("\nNumber of unique Dates in beg_inv:", beg_inv['startDate'].nunique())
print("Date distribution:\n", beg_inv['startDate'].value_counts())

# drop startDate column since all the same 2016-01-01
beg_inv = beg_inv.drop(columns=['startDate'])

# Standardize Size column to mL or "Mixed Pack" for unclear size values
print("\nNumber of Unique sizes before standardization:", beg_inv['Size'].nunique())
print("Distribution of unique Sizes before standardization:\n", beg_inv['Size'].value_counts())

beg_inv['Size'] = beg_inv['Size'].apply(convert_to_ml)
print("\nNumber of Unique sizes after standardization:", beg_inv['Size'].nunique())
print("Distribution of unique Sizes after standardization:\n", beg_inv['Size'].value_counts())

# Convert 'Price' to numeric
beg_inv['Price'] = pd.to_numeric(beg_inv['Price'], errors='coerce')

# Get sum of the 'Price' column
total_price = beg_inv['Price'].sum()
print("\nSum of Price column:", total_price)

# Convert 'Size' to numeric
beg_inv['Size'] = pd.to_numeric(beg_inv['Size'], errors='coerce')

# Get sum of the 'Size' column
total_size = beg_inv['Size'].sum()
print("\nSum of Size column:", total_size)

# get all rows with 'Store' value 3
# store3_df = beg_inv[beg_inv['Store'] == 46]
# print(store3_df)

# Get all rows with 'Vodka' in 'Desciption' column
# vodka_df = beg_inv[beg_inv['Description'].str.contains('Vodka', case=False, na=False)]
# print(vodka_df)


# Save the cleaned data 
beg_inv.to_csv("archive/cleaned_BegInv.csv", index=False)



