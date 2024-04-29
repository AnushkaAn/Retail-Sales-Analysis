import pandas as pd

# Load the .txt file into a DataFrame
file_path = 'dat.txt'  # Replace with your .txt file path
# Since the data appears tab-separated, use '\t' as the delimiter
data = pd.read_csv(file_path, delimiter='\t')

# Display the first few rows to understand the data structure
print("Data Head:")
print(data.head())
print("Column Names:", data.columns)

# Data cleaning and preparation
# Deduplicate based on 'Transaction ID' or another unique identifier
if '1' in data.columns:
    # Rename the first column to a more understandable name
    data.rename(columns={'1': 'Transaction ID'}, inplace=True)
    data = data.drop_duplicates(subset=['Transaction ID'])
else:
    print("Error: Expected unique identifier column 'Transaction ID' not found")

# Ensure the date column is in datetime format
date_column = '2023-11-24'  # Identify the correct date column
if date_column in data.columns:
    data[date_column] = pd.to_datetime(data[date_column])
    data.rename(columns={date_column: 'Transaction_Date'}, inplace=True)
else:
    print("Error: Expected 'Transaction_Date' column not found")

# Apply some filtering conditions
# Filter for transactions in 2023
if 'Transaction_Date' in data.columns:
    sales_2023 = data[data['Transaction_Date'].dt.year == 2023]

    # Display filtered data
    print("Filtered Data (2023):")
    print(sales_2023.head())
else:
    print("Error: 'Transaction_Date' column not found, unable to filter by year")
