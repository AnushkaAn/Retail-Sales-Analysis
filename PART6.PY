import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load and preprocess the data
file_path = 'dat.txt'  # Ensure this path is correct
data = pd.read_csv(file_path, delimiter='\t')

# Ensure proper column names
expected_column_names = ['Transaction ID', 'Date', 'Customer_ID', 'Gender', 'Age', 'Product_Category', 'Quantity', 'Price_Per_Unit', 'Total_Price']
if data.columns.tolist() != expected_column_names:
    data.columns = expected_column_names

# Convert 'Date' to datetime and clean data
data['Date'] = pd.to_datetime(data['Date'])
data = data.drop_duplicates(subset=['Transaction ID']).dropna()

# Define age groups
age_bins = [0, 25, 35, 45, 55, 65, 100]
age_labels = ['0-25', '26-35', '36-45', '46-55', '56-65', '66+']
data['Age_Group'] = pd.cut(data['Age'], bins=age_bins, labels=age_labels)

# Filter data for 2023
sales_2023 = data[data['Date'].dt.year == 2023]

# Analysis of monthly sales
monthly_sales = sales_2023.resample('MS', on='Date').agg({
    'Total_Price': 'sum'
})

# Analysis of customer purchases
customer_purchases = sales_2023.groupby('Customer_ID').agg({
    'Total_Price': 'sum',
    'Quantity': 'sum'
}).sort_values(by='Total_Price', ascending=False)

# Analysis of product popularity by category
category_popularity = sales_2023.groupby('Product_Category').agg({
    'Total_Price': 'sum',
    'Quantity': 'sum'
}).sort_values(by='Total_Price', ascending=False)

# Analysis of sales by age group
age_group_sales = sales_2023.groupby('Age_Group').agg({
    'Total_Price': 'sum',
    'Quantity': 'sum'
})

# Analysis of sales by gender and product category
gender_category_sales = sales_2023.groupby(['Gender', 'Product_Category']).agg({
    'Total_Price': 'sum'
}).unstack()

# Create a simple text-based report with key insights and recommendations
report = []

report.append("Sales Analysis Report for 2023")
report.append("===================================")
report.append(f"Report Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report.append("\n")

# Monthly sales insights
highest_sales_month = monthly_sales['Total_Price'].idxmax().strftime('%B %Y')
lowest_sales_month = monthly_sales['Total_Price'].idxmin().strftime('%B %Y')

report.append("Monthly Sales Analysis:")
report.append(f"  - Highest sales month: {highest_sales_month}")
report.append(f"  - Lowest sales month: {lowest_sales_month}")
report.append(f"  - Total sales for the year: ${monthly_sales['Total_Price'].sum():,.2f}")
report.append("\n")

# Customer purchases insights
top_customer_id = customer_purchases.index[0]
top_customer_total = customer_purchases.loc[top_customer_id, 'Total_Price']

report.append("Customer Purchasing Analysis:")
report.append(f"  - Customer with the highest total spending: {top_customer_id} (${top_customer_total:,.2f})")
report.append(f"  - Total unique customers in 2023: {len(customer_purchases)}")
report.append("\n")

# Product popularity insights
most_popular_category = category_popularity.index[0]
most_popular_category_sales = category_popularity.loc[most_popular_category, 'Total_Price']

report.append("Product Popularity Analysis:")
report.append(f"  - Most popular product category by sales: {most_popular_category} (${most_popular_category_sales:,.2f})")
report.append(f"  - Total unique product categories in 2023: {len(category_popularity)}")
report.append("\n")

# Sales by age group insights
largest_age_group = age_group_sales['Total_Price'].idxmax()

report.append("Sales by Age Group:")
report.append(f"  - Age group with the highest sales: {largest_age_group}")
report.append(f"  - Total sales by age group:")
for age_group, total in age_group_sales['Total_Price'].items():
    report.append(f"    - {age_group}: ${total:,.2f}")
report.append("\n")

# Recommendations based on analysis
report.append("Recommendations:")
report.append("  - Focus marketing efforts on the age group with the highest sales for targeted campaigns.")
report.append("  - Consider product bundling or discounts in lower-sales months to increase revenue.")
report.append("  - Strengthen customer loyalty programs to retain top customers and encourage repeat business.")
report.append("  - Explore partnerships or promotions with most popular product categories to increase engagement.")

# Output the report as text
report_text = "\n".join(report)
print(report_text)

