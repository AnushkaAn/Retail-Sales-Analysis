import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = 'dat.txt'  # Replace with your actual file path
data = pd.read_csv(file_path, delimiter='\t')

# Set column names and correct data types
expected_column_names = ['Transaction ID', 'Date', 'Customer_ID', 'Gender', 'Age', 'Product_Category', 'Quantity', 'Price_Per_Unit', 'Total_Price']
if data.columns.tolist() != expected_column_names:
    data.columns = expected_column_names

data['Date'] = pd.to_datetime(data['Date'])

# Clean the data
data = data.drop_duplicates(subset=['Transaction ID'])
data = data.dropna()

# Define age groups
age_bins = [0, 25, 35, 45, 55, 65, 100]
age_labels = ['0-25', '26-35', '36-45', '46-55', '56-65', '66+']
data['Age_Group'] = pd.cut(data['Age'], bins=age_bins, labels=age_labels)

# Filter data for 2023
sales_2023 = data[data['Date'].dt.year == 2023]

# Grouped analysis
customer_purchases = sales_2023.groupby('Customer_ID').agg({
    'Total_Price': 'sum',
    'Quantity': 'sum'
}).sort_values(by='Total_Price', ascending=False)

category_popularity = sales_2023.groupby('Product_Category').agg({
    'Total_Price': 'sum',
    'Quantity': 'sum'
}).sort_values(by='Total_Price', ascending=False)

monthly_sales = sales_2023.resample('MS', on='Date').agg({
    'Total_Price': 'sum'
})

age_group_sales = sales_2023.groupby('Age_Group').agg({
    'Total_Price': 'sum',
    'Quantity': 'sum'
})

gender_category_sales = sales_2023.groupby(['Gender', 'Product_Category']).agg({
    'Total_Price': 'sum'
}).unstack()

# Set up subplots grid
fig, axs = plt.subplots(3, 3, figsize=(15, 15))
fig.subplots_adjust(wspace=0.5, hspace=1.0)  # Add spacing between subplots

# Plot data on the grid
# (0, 0) - Line plot for monthly sales trends
axs[0, 0].plot(monthly_sales.index, monthly_sales['Total_Price'], marker='o', linestyle='-', color='b')
axs[0, 0].set_title('Monthly Sales Trends (2023)')
axs[0, 0].set_xlabel('Month')
axs[0, 0].set_ylabel('Total Sales ($)')

# (0, 1) - Bar chart for product popularity by total sales
category_popularity['Total_Price'].plot(kind='bar', color='orange', ax=axs[0, 1])
axs[0, 1].set_title('Product Popularity by Total Sales (2023)')
axs[0, 1].set_xlabel('Product Category')
axs[0, 1].set_ylabel('Total Sales ($)')

# (0, 2) - Bar chart for sales by age group
age_group_sales['Total_Price'].plot(kind='bar', color='green', ax=axs[0, 2])
axs[0, 2].set_title('Sales by Age Group (2023)')
axs[0, 2].set_xlabel('Age Group')
axs[0, 2].set_ylabel('Total Sales ($)')

# (1, 0) - Pie chart for sales distribution by product category
category_popularity['Total_Price'].plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=axs[1, 0])
axs[1, 0].set_title('Sales Distribution by Product Category (2023)')
axs[1, 0].set_ylabel('')  # Hide y-axis label for pie chart

# (1, 1) - Scatter plot for total sales against age
axs[1, 1].scatter(data['Age'], data['Total_Price'], c='purple', alpha=0.5)
axs[1, 1].set_title('Scatter Plot of Total Sales by Age')
axs[1, 1].set_xlabel('Age')
axs[1, 1].set_ylabel('Total Sales ($)')

# (1, 2) - Histogram of unit sales
axs[1, 2].hist(sales_2023['Quantity'], bins=10, color='teal', alpha=0.7)
axs[1, 2].set_title('Histogram of Units Sold (2023)')
axs[1, 2].set_xlabel('Units Sold')
axs[1, 2].set_ylabel('Frequency')

# (2, 0) - Bar chart for sales by gender and product category
gender_category_sales.plot(kind='bar', ax=axs[2, 0])
axs[2, 0].set_title('Sales by Gender and Product Category (2023)')
axs[2, 0].set_xlabel('Gender')
axs[2, 0].set_ylabel('Total Sales ($)')

# Turn off unused plots
axs[2, 1].axis('off')
axs[2, 2].axis('off')

# Show the plots
plt.show()
