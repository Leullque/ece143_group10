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
end_inv = pd.read_csv("archive/EndInvFINAL12312016.csv")

# Check for missing data
print("Missing rows in end_inv:", missing_data(end_inv), "\n")
#empty_rows = end_inv[end_inv['City'].isna() | (end_inv['City'] == "")]
#print("Empty Rows:",empty_rows)

# Fix missing city data
missing_city_count = end_inv['City'].isna().sum()
print(f"Number of missing 'City' values in end_inv: {missing_city_count}")
if missing_city_count > 0:
    end_inv.loc[end_inv['City'].isna(), 'City'] = 'TYWARDREATH'
print("Number of missing rows in end_inv after fix:", missing_data(end_inv))

# Remove whitespace
columns_to_clean = ['City', 'Description']
end_inv = remove_whitespace(end_inv, *columns_to_clean)

# Analyze unique values
print("Number of unique Stores in end_inv:", end_inv['Store'].nunique())
print("Store distribution:\n", end_inv['Store'].value_counts())

print("\nNumber of unique Cities in end_inv:", end_inv['City'].nunique())
print("Cities distribution:\n", end_inv['City'].value_counts())

print("\nNumber of unique Brands in end_inv:", end_inv['Brand'].nunique())
print("Brand distribution:\n", end_inv['Brand'].value_counts())

print("\nNumber of unique Descriptions in end_inv:", end_inv['Description'].nunique())
print("Description distribution:\n", end_inv['Description'].value_counts())

print("\nNumber of unique Dates in end_inv:", end_inv['endDate'].nunique())
print("Date distribution:\n", end_inv['endDate'].value_counts())

# drop endDate column since all the same 2016-12-31
end_inv = end_inv.drop(columns=['endDate'])

# Standardize Size column to mL or "Mixed Pack" for unclear size values
print("\nNumber of Unique sizes before standardization:", end_inv['Size'].nunique())
print("Distribution of unique Sizes before standardization:\n", end_inv['Size'].value_counts())

end_inv['Size'] = end_inv['Size'].apply(convert_to_ml)
print("\nNumber of Unique sizes after standardization:", end_inv['Size'].nunique())
print("Distribution of unique Sizes after standardization:\n", end_inv['Size'].value_counts())

# drop rows with "Mixed Pack" size ?
# end_inv = end_inv[end_inv['Size'] != "Mixed Pack"]
# print("Distribution of unique Sizes after standardization:\n", end_inv['Size'].value_counts())


# Convert 'Price' to numeric
end_inv['Price'] = pd.to_numeric(end_inv['Price'], errors='coerce')

# Get sum of the 'Price' column to make sure numeric
total_price = end_inv['Price'].sum()
print("\nSum of Price column:", total_price)

# Convert 'Size' to numeric
end_inv['Size'] = pd.to_numeric(end_inv['Size'], errors='coerce')

# Get sum of the 'Size' column
total_size = end_inv['Size'].sum()
print("\nSum of Size column:", total_size)

# get all rows with 'Store' value 3
# store46_df = end_inv[end_inv['Store'] == 46]
# print(store46_df)

# Get all rows with 'Vodka' in 'Desciption' column
# vodka_df = end_inv[end_inv['Description'].str.contains('Vodka', case=False, na=False)]
# print(vodka_df)


# Save the cleaned data 
end_inv.to_csv("archive/cleaned_EndInv.csv", index=False)