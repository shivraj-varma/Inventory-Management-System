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

# product function to add, update, delete, show all and save database or csv file
def Products():
    def add(): # nested function add
        connection = get_connection()
        if not connection: # check connection
            return
        
        try: # error headling
            cursor = connection.cursor()
            p_id = int(input("Enter Product id: "))

            # check if product existe in database
            cursor.execute(
                    "SELECT product_id FROM products WHERE product_id = %s",(p_id,))
            if cursor.fetchone():
                print("❌ Product with this id already existe! ")
                return
            # input Data
            name = input("Enter Product Name: ").strip().title()
            category = input("Enter Product Category: ").strip().title()
            description = input("Enter Product Description: ").strip().title()
            unit_price = int(input("Enter Per/Unit price: "))
            sku = input("Enter SKU code: ").strip().title()

            # Insert Data 
            cursor.execute('''INSERT INTO products (product_id, name, category, description, unit_price, sku)
                            VALUES (%s, %s, %s, %s, %s, %s)''',(p_id, name, category, description, unit_price, sku))

            connection.commit()
            print(f"✅ Product: {name} (Product id {p_id} Add Successfully.)")

        except Error as e:
            print(f"❌ Error Adding Product: {e}")
        finally:
            cursor.close()
            connection.close()

    def update():
        connection = get_connection()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            p_id = int(input("Enter Product id to Update: "))

            # check if product exists in database
            cursor.execute("SELECT product_id FROM products WHERE product_id = %s",(p_id,))
            if not cursor.fetchone():
                print("❌ Pruduct with this id already existe!")
                return
            name = input("Enter New Product Name (or press Enter to keep current): ").strip().title()
            category = input("Enter New Product Category (or press Enter to keep current): ").strip().title()
            description = input("Enter New Product Description (or press Enter to keep current): ").strip().title()
            unit_price = (input("Enter New Per/Unit price (or press Enter to keep current): "))
            sku = input("Enter new SKU code (or press Enter to keep current): ").strip().title()

            if name:
                cursor.execute("UPDATE products SET name = %s WHERE product_id = %s",(name, p_id))
            if category:
                cursor.execute("UPDATE products SET category = %s WHERE product_id = %s",(category, p_id))
            if description:
                cursor.execute("UPDATE products SET discription = %s WHERE product_id = %s",(description, p_id))
            if unit_price:
                cursor.execute("UPDATE products SET unit_price = %s WHERE product_id = %s",(unit_price, p_id))
            if sku:
                cursor.execute("UPDATE products SET sku = %s WHERE product_id = %s",(sku, p_id))

            connection.commit()
            print(f"✅ Product at this id({p_id}) Updated Successfully.")

        except Error as e:
            print(f"❌ Error in Adding Product: {e}")
        finally:
            cursor.close()
            connection.close()


    


def Inventory():
    pass

def Sales():
    pass

def Suppliers():
    pass
