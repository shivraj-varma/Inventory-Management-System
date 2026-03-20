import mysql.connector              # cannect sql database 
from mysql.connector import Error   
import pandas as pd  
import csv               

# Create function for database connection
def get_connection():
    # Error heandling
    try:
        connection= mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "shivraj@001M",
            database = "i_m_s_db"
        )
        return connection
    except Error as e:
        print(f"❌Database connection : {e}")
        return None
    
# create function for database tables 
def create_tables():
    connection = get_connection() 
    if connection: 
        cursor = connection.cursor()

        # Create Product table
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS products(
                       product_id INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(200) NOT NULL,
                       category VARCHAR(100) NOT NULL,
                       description VARCHAR(400) NOT NULL,
                       unit_price INT NOT NULL,
                       sku VARCHAR(100) NOT NULL
                       )
            ''')
        # Create Inventory table
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventory(
                       inventory_id INT AUTO_INCREMENT PRIMARY KEY,
                       product_id INT,
                       quantity INT NOT NULL,
                       min_stock INT NOT NULL,
                       last_updated DATE NOT NULL,
                       FOREIGN KEY (product_id) REFERENCES products(product_id)
                       )
            ''')
        # Create Sales table
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS sales(
                       sales_id INT AUTO_INCREMENT PRIMARY KEY,
                       product_id INT,
                       quantity_sold INT NOT NULL,
                       sale_date DATE NOT NULL,
                       total_amount INT NOT NULL,
                       FOREIGN KEY (product_id) REFERENCES products(product_id)
                       )
            ''')
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS suppliers(
                       supplier_id INT AUTO_INCREMENT PRIMARY KEY,
                       product_id INT,
                       name VARCHAR(100) NOT NULL,
                       contect INT NOT NULL,
                       FOREIGN KEY (product_id) REFERENCES products(product_id)
                       )
            ''')
        
        connection.commit()
        cursor.close()
        connection.close()


def Product():
    pass

def Inventory():
    pass

def Sales():
    pass

def Suppliers():
    pass
