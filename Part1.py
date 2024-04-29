import mysql.connector
import pandas as pd

# Step 1: Connect to the MySQL Database
def create_db_connection():
    # MySQL connection details (update with your values)
    host = "localhost"
    user = "root"  # Default user in XAMPP
    password = ""  # Your MySQL password in XAMPP
    database = "dbms"  # Name of the database you want to connect to

    # Create the connection
    conn = mysql.connector.connect( 
        host=host,
        user=user,
        passwd=password,
        database=database
    )
    return conn

# Step 2: Extract Data from the Database
def extract_data(connection, query):
    # Use a cursor to execute a SQL query
    cursor = connection.cursor()
    cursor.execute(query)

    # Fetch all the rows from the query result
    rows = cursor.fetchall()

    # Get the column names
    column_names = [desc[0] for desc in cursor.description]

    # Create a DataFrame from the rows and column names
    df = pd.DataFrame(rows, columns=column_names)
    return df

# Step 3: Save Data to a Text File
def save_to_text_file(df, filename):
    # Save the DataFrame to a text file with tab-separated values
    df.to_csv(filename, sep='\t', index=False)

# Example usage
if __name__ == "__main__":
    # Create a database connection
    conn = create_db_connection()

    # Define the SQL query to extract data from a specific table
    query = "SELECT * FROM retail_sales"  # Modify to your table name

    # Extract data from the database
    data_from_db = extract_data(conn, query)

    # Save the extracted data to a text file
    save_to_text_file(data_from_db, 'dat.txt')  # Change filename as needed

    # Close the connection
    conn.close()
