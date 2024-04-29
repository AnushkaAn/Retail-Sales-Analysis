import pandas as pd
import matplotlib.pyplot as plt

# Load the data from 'dat.txt' with the correct delimiter
file_path = 'dat.txt'  # Ensure this path is correct
data = pd.read_csv(file_path, delimiter='\t')  # Adjust the delimiter if needed

# Correct the column names if necessary
expected_column_names = ['Transaction ID', 'Date', 'Customer_ID', 'Gender', 'Age', 'Product_Category', 'Quantity', 'Price_Per_Unit', 'Total_Price']

if data.columns.tolist() != expected_column_names:
    data.columns = expected_column_names  # Correct column names if needed

# Convert 'Date' to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Data cleaning: Remove duplicates and handle missing data
data = data.drop_duplicates(subset=['Transaction ID'])  # Remove duplicates
data = data.dropna()  # Handle missing data

# Create 'Age_Group' before grouping by it
age_bins = [0, 25, 35, 45, 55, 65, 100]
age_labels = ['0-25', '26-35', '36-45', '46-55', '56-65', '66+']
data['Age_Group'] = pd.cut(data['Age'], bins=age_bins, labels=age_labels)  # Correctly define 'Age_Group'

# Filter data for sales in 2023
sales_2023 = data[data['Date'].dt.year == 2023]

# Analyze customer purchasing behavior
customer_purchases = sales_2023.groupby('Customer_ID').agg({
    'Total_Price': 'sum',
    'Quantity': 'sum'
}).sort_values(by='Total_Price', ascending=False)

# Analyze product popularity by category
category_popularity = sales_2023.groupby('Product_Category').agg({
    'Total_Price': 'sum',
    'Quantity': 'sum'
}).sort_values(by='Total_Price', ascending=False)

# Visualization: Line chart for monthly sales trends in 2023
monthly_sales = sales_2023.resample('MS', on='Date').agg({
    'Total_Price': 'sum'
})  # Fixes the FutureWarning

plt.figure(figsize=(10, 6))
plt.plot(monthly_sales.index, monthly_sales['Total_Price'], marker='o', linestyle='-', color='b')
plt.title('Monthly Sales Trends for 2023')
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.show()

# Bar chart for product popularity by total sales
plt.figure(figsize=(10, 6))
category_popularity['Total_Price'].plot(kind='bar', color='orange')
plt.title('Product Popularity by Total Sales (2023)')
plt.xlabel('Product_Category')
plt.ylabel('Total Sales ($)')
plt.show()

# Analyze sales by age group
age_group_sales = sales_2023.groupby('Age_Group').agg({
    'Total_Price': 'sum',
    'Quantity': 'sum'
})

# Bar chart for sales by age group
plt.figure(figsize=(10, 6))
age_group_sales['Total_Price'].plot(kind='bar', color='green')
plt.title('Sales by Age Group (2023)')
plt.xlabel('Age Group')
plt.ylabel('Total Sales ($)')
plt.show()

# Additional visualizations (pie chart, scatter plot, etc.)
# Pie chart for sales distribution by product category
plt.figure(figsize=(8, 8))
category_popularity['Total_Price'].plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Sales Distribution by Product Category (2023)')
plt.show()

# Scatter plot for total sales against age
plt.figure(figsize=(10, 6))
plt.scatter(data['Age'], data['Total_Price'], c='purple', alpha=0.5)
plt.title('Scatter Plot of Total Sales by Age')
plt.xlabel('Age')
plt.ylabel('Total Sales ($)')
plt.show()

# Histogram of unit sales to understand the distribution of sales quantity
plt.figure(figsize=(10, 6))
plt.hist(sales_2023['Quantity'], bins=10, color='teal', alpha=0.7)
plt.title('Histogram of Units Sold (2023)')
plt.xlabel('Units Sold')
plt.ylabel('Frequency')
plt.show()

# Bar chart for sales by gender and product category
gender_category_sales = sales_2023.groupby(['Gender', 'Product_Category']).agg({
    'Total_Price': 'sum'
}).unstack()

gender_category_sales.plot(kind='bar', figsize=(10, 6))
plt.title('Sales by Gender and Product Category (2023)')
plt.xlabel('Gender')
plt.ylabel('Total Sales ($)')
plt.show()