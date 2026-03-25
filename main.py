import mysql.connector              # cannect sql database 
from mysql.connector import Error   
import pandas as pd  
import csv            
import os   

CSV_FILE = "ims_data.csv"

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
                       contect BIGINT NOT NULL,
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
                cursor.execute("UPDATE products SET description = %s WHERE product_id = %s",(description, p_id))
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

    def delete():
        connection = get_connection()
        if not connection:
            print("Error connection not found")
            return
        try:
            cursor = connection.cursor()
            p_id = int(input("Enter Product id: "))

            # check if product id existe
            cursor.execute("SELECT product_id FROM products WHERE product_id = %s",(p_id,))
            if not cursor.fetchone():
                print("❌ Pruduct with this id not existe!")
                return
            
            cursor.execute("DELETE FROM products WHERE product_id = %s",(p_id,))
            connection.commit()
            print(f"✅ Product with this id{p_id} Delete Successfully!")
        except Error as e:
            print(f"❌Error: deleting product is {e}")
        finally:
            cursor.close()
            connection.close()

    def search_products():
        connection = get_connection()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            p_id = int(input("Enter Product id for search: "))
            
            # Check if product id existe in database
            cursor.execute("SELECT product_id FROM products WHERE product_id = %s",(p_id,))
            if not cursor.fetchone():
                print("❌This product id not Existe in database")
                return
            cursor.execute("SELECT * FROM products WHERE product_id = %s",(p_id,))
            result = cursor.fetchall()
            if result:
                print(f"\n📋 Product Details (Product id {p_id}):")
                print("-" * 60)
                for row in result:
                    print(f"PRODUCT: Name = {row[1]} | Category = {row[2]} | Description = {row[3]} | Unit Price = {row[4]} | Sku = {row[5]}")
            
            connection.commit()
        except Error as e:
            print(f"❌Error: searching products {e}")
        finally:
            cursor.close()
            connection.close()


    def show_all_products():
        connection = get_connection()
        if not connection:
            print("❌ Connection not found")
            return
        try:
            cursor = connection.cursor()
            
            # Check if Product table not empty
            cursor.execute("SELECT * FROM products")
            result = cursor.fetchall()
            if result:
                print(f"\n📋 SHOW ALL Product:")
                print("-" * 60)
                print(result)
            else:
                print("❌Product Table is Empty.")
            connection.commit()
        
        except Error as e:
            print(f"❌Error show all data {e}")
        finally:
            cursor.close()
            connection.close()
    def export_to_csv():
        connection = get_connection()
        if not connection:
            print("❌ Connection not found")
            return
        
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM products")
        rows = cursor.fetchall()

        with open(f"products.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)

    while True:
        print("=" * 50)
        print('''
                PRODUCTS DETAILS
            1. ADD 
            2. UPDATE 
            3. DELETE 
            4. SEARCH PRODUCT 
            5.SHOW ALL DATA 
            6. Export to CSV File
            7. EXIT 
            
        ''')
        user = int(input("Enter your choice: "))
        if user == 1:
            add()
        elif user == 2:
            update()
        elif user == 3:
            delete()
        elif user == 4:
            search_products()
        elif user == 5:
            show_all_products()
        elif user == 6:
            export_to_csv()
        elif user == 7:
            break
        else:
            print("❌ Invalid choice")


    
def Inventory():
    def add(): # nested function add
        connection = get_connection()
        if not connection: # check connection
            return
        
        try: # error headling
            cursor = connection.cursor()
            i_id = int(input("Enter Inventory id: "))

            # check if Inventory existe in database
            cursor.execute(
                    "SELECT inventory_id FROM inventory WHERE inventory_id = %s",(i_id,))
            if cursor.fetchone():
                print("❌ Inventory with this id already existe! ")
                return
            # input Data
            p_id = int(input("Enter Product id: "))
            quantity = input("Enter Quantity: ").strip().title()
            min_stock = input("Enter Minimum Stock: ").strip().title()
            last_update = input("Enter Today Date (yyyy-mm-dd): ").strip().title()


            # Insert Data 
            cursor.execute('''INSERT INTO inventory (inventory_id, product_id, quantity, min_stock, last_updated)
                            VALUES (%s, %s, %s, %s,%s)''',(i_id, p_id, quantity, min_stock, last_update))

            connection.commit()
            print(f"✅(Inventory id {i_id} Add Successfully.)")

        except Error as e:
            print(f"❌ Error Adding Inventory details: {e}")
        finally:
            cursor.close()
            connection.close()
    def update():
        connection = get_connection()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            i_id = int(input("Enter Inventory id to Update: "))

            # check if Inventory id exists in Inventory Table
            cursor.execute("SELECT inventory_id FROM inventory WHERE inventory_id = %s",(i_id,))
            if not cursor.fetchone():
                print("❌ Inventory with this id already existe!")
                return
            p_id = int(input("Enter New Product id (or press Enter to keep current): "))
            quantity = int(input("Enter New Quantity (or press Enter to keep current): "))
            
            min_stock = int(input("Enter Minimum Stock (or press Enter to keep current): "))
            last_update = input("Enter Todays Date (or press Enter to keep current): ").strip().title()

            if p_id:
                cursor.execute("UPDATE inventory SET product_id = %s WHERE inventory_id = %s",(p_id, i_id))
            if quantity:
                cursor.execute("UPDATE inventory SET quantity = %s WHERE inventory_id = %s",(quantity, i_id))
            
            if min_stock:
                cursor.execute("UPDATE inventory SET min_stock = %s WHERE inventory_id = %s",(min_stock, i_id))
            if last_update:
                cursor.execute("UPDATE inventory SET last_updated = %s WHERE inventoyr_id = %s",(last_update, i_id))

            connection.commit()
            print(f"✅ Inventory at this id({i_id}) Updated Successfully.")

        except Error as e:
            print(f"❌ Error in Adding Inventory Details: {e}")
        finally:
            cursor.close()
            connection.close()

    def delete():
        connection = get_connection()
        if not connection:
            print("Error connection not found")
            return
        try:
            cursor = connection.cursor()
            i_id = int(input("Enter Inventory id: "))

            # check if Inventoyr id existe
            cursor.execute("SELECT inventory_id FROM inventory WHERE inventory_id = %s",(i_id,))
            if not cursor.fetchone():
                print("❌ Inventory with this id not existe!")
                return
            
            cursor.execute("DELETE FROM inventory WHERE inventory_id = %s",(i_id,))
            connection.commit()
            print(f"✅ Inventory with this id {i_id} Delete Successfully!")
        except Error as e:
            print(f"❌Error: deleting Inventory is {e}")
        finally:
            cursor.close()
            connection.close()
    
    def search_products():
        connection = get_connection()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            i_id = int(input("Enter Inventory id for search: "))
            
            # Check if Inventory id existe in Inventory Table
            cursor.execute("SELECT inventory_id FROM inventory WHERE inventory_id = %s",(i_id,))
            if not cursor.fetchone():
                print("❌This Inventory id not Existe in Inventory Table")
                return
            cursor.execute("SELECT * FROM inventory WHERE inventory_id = %s",(i_id,))
            result = cursor.fetchall()
            if result:
                print(f"\n📋 Inventory Details (Inventory id {i_id}):")
                print("-" * 60)
                for row in result:
                    print(f"INVENTORY: Product id = {row[1]} | Quantity = {row[2]} | Minimum Stock = {row[3]} | Last Updated = {row[4]}")
            
            connection.commit()
        except Error as e:
            print(f"❌Error: searching Inventory {e}")
        finally:
            cursor.close()
            connection.close()

    def show_all_products():
        connection = get_connection()
        if not connection:
            print("❌ Connection not found")
            return
        try:
            cursor = connection.cursor()
            
            # Check if Inventory table not empty
            cursor.execute("SELECT * FROM inventory")
            result = cursor.fetchall()
            if result:
                print(f"\n📋 SHOW ALL Inventory Details:")
                print("-" * 60)
                print(result)
            else:
                print("❌Invenoty Table is Empty.")
            connection.commit()
        
        except Error as e:
            print(f"❌Error show all data {e}")
        finally:
            cursor.close()
            connection.close()
    def export_to_csv():
        connection = get_connection()
        if not connection:
            print("❌ Connection not found")
            return
        
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM inventory")
        rows = cursor.fetchall()

        with open(f"inventory.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)

    while True:
        print("=" * 50)
        print('''
                INVENTORY DETAILS
            1. ADD 
            2. UPDATE 
            3. DELETE 
            4. SEARCH PRODUCT 
            5. SHOW ALL DATA 
            6. Export to CSV File
            7. EXIT 
            
        ''')
        user = int(input("Enter your choice: "))
        if user == 1:
            add()
        elif user == 2:
            update()
        elif user == 3:
            delete()
        elif user == 4:
            search_products()
        elif user == 5:
            show_all_products()
        elif user ==6:
            export_to_csv()
        elif user == 7:
            break
        else:
            print("❌ Invalid choice")



def Sales():
    def add(): # nested function add
        connection = get_connection()
        if not connection: # check connection
            return

        
        try: # error headling
            cursor = connection.cursor()
            s_id = int(input("Enter Sales id: "))

            # check if Sales is existe in Sales Table
            cursor.execute(
                    "SELECT sales_id FROM sales WHERE sales_id = %s",(s_id,))
            if cursor.fetchone():
                print("❌ Sales with this id already existe! ")
                return
            # input Data
            p_id = int(input("Enter Product id: "))
            quantity_sold = int(input("Enter Sold Quantity: "))
            sale_date = input("Enter Todays Date: ")
            # Calculate Total Amount of product sale
            cursor.execute("SELECT unit_price FROM products WHERE product_id = %s", (p_id,))
            price = cursor.fetchone()[0]

            total_amount = price * quantity_sold


            # Insert Data 
            cursor.execute('''INSERT INTO sales (sales_id, product_id, quantity_sold, sale_date, total_amount)
                            VALUES (%s, %s, %s, %s,%s)''',(s_id, p_id, quantity_sold, sale_date, total_amount))

            connection.commit()
            print(f"✅(Sales id {s_id} Add Successfully.)")

        except Error as e:
            print(f"❌ Error Adding Sales details: {e}")
        finally:
            cursor.close()
            connection.close()

    def update():
        connection = get_connection()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            s_id = int(input("Enter Sales id to Update: "))

            # check if Sales id exists in Inventory Table
            cursor.execute("SELECT sales_id FROM Sales WHERE sales_id = %s",(s_id,))
            if not cursor.fetchone():
                print("❌ Sales with this id already existe!")
                return
            p_id = int(input("Enter New Product id (or press Enter to keep current): "))
            quantity_sold = int(input("Enter New Quantity Sold (or press Enter to keep current): "))
            
            sales_date = (input("Enter Sales Date (or press Enter to keep current): "))
            cursor.execute("SELECT unit_price FROM products WHERE product_id = %s", (p_id,))
            price = cursor.fetchone()[0]

            total_amount = price * quantity_sold
            
            

            if p_id:
                cursor.execute("UPDATE sales SET sales_id = %s WHERE sales_id = %s",(p_id, s_id))
            if quantity_sold:
                cursor.execute("UPDATE sales SET quantity_sold = %s WHERE sales_id = %s",(quantity_sold, s_id))
            
            if sales_date:
                cursor.execute("UPDATE sales SET sale_date = %s WHERE sales_id = %s",(sales_date, s_id))
            if total_amount:
                cursor.execute("UPDATE sales SET total_amount = %s WHERE sales_id = %s",(total_amount, s_id))

            connection.commit()
            print(f"✅ Sales at this id({s_id}) Updated Successfully.")

        except Error as e:
            print(f"❌ Error in Updating Sales Details: {e}")
        finally:
            cursor.close()
            connection.close()
    

    def delete():
        connection = get_connection()
        if not connection:
            print("Error connection not found")
            return
        try:
            cursor = connection.cursor()
            s_id = int(input("Enter Sales id: "))

            # check if Sales id existe
            cursor.execute("SELECT sales_id FROM sales WHERE sales_id = %s",(s_id,))
            if not cursor.fetchone():
                print("❌ sales with this id not existe!")
                return
            
            cursor.execute("DELETE FROM sales WHERE sales_id = %s",(s_id,))
            connection.commit()
            print(f"✅ Sales with this id {s_id} Delete Successfully!")
        except Error as e:
            print(f"❌Error: deleting Sales is {e}")
        finally:
            cursor.close()
            connection.close()
    
    def search_products():
        connection = get_connection()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            s_id = int(input("Enter sales id for search: "))
            
            # Check if sales id existe in sales Table
            cursor.execute("SELECT sales_id FROM sales WHERE sales_id = %s",(s_id,))
            if not cursor.fetchone():
                print("❌This sales id not Existe in sales Table")
                return
            cursor.execute("SELECT * FROM sales WHERE sales_id = %s",(s_id,))
            result = cursor.fetchall()
            if result:
                print(f"\n📋 Sales Details (Sales id {s_id}):")
                print("-" * 60)
                for row in result:
                    print(f"SALES: Product id = {row[1]} | Quantity Sold = {row[2]} | Sales Date = {row[3]} | Total Amount = {row[4]}")
            
            connection.commit()
        except Error as e:
            print(f"❌Error: searching Sales id {e}")
        finally:
            cursor.close()
            connection.close()

    def show_all_products():
        connection = get_connection()
        if not connection:
            print("❌ Connection not found")
            return
        try:
            cursor = connection.cursor()
            
            # Check if Sales table not empty
            cursor.execute("SELECT * FROM sales")
            result = cursor.fetchall()
            if result:
                print(f"\n📋 SHOW ALL Sales Details:")
                print("-" * 60)
                print(result)
            else:
                print("❌Sales Table is Empty.")
            connection.commit()
        
        except Error as e:
            print(f"❌Error show all data {e}")
        finally:
            cursor.close()
            connection.close()
    def export_to_csv():
        connection = get_connection()
        if not connection:
            print("❌ Connection not found")
            return
        
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM sales")
        rows = cursor.fetchall()

        with open(f"sales.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)

    while True:
        print("=" * 50)
        print('''
                SALES DETAILS
            1. ADD 
            2. UPDATE 
            3. DELETE 
            4. SEARCH PRODUCT
            5. SHOW ALL DATA 
            6. Export to CSV File
            7. Exit
            
        ''')
        user = int(input("Enter your choice: "))
        if user == 1:
            add()
        elif user == 2:
            update()
        elif user == 3:
            delete()
        elif user == 4:
            search_products()
        elif user == 5:
            show_all_products()
        elif user == 6:
            export_to_csv()
        elif user == 7:
            break
        else:
            print("❌ Invalid choice")



def Suppliers():
    def add(): # nested function add
        connection = get_connection()
        if not connection: # check connection
            return

        
        try: # error headling
            cursor = connection.cursor()
            s_id = int(input("Enter Supplier id: "))

            # check if Supplier id is existe in Sales Table
            cursor.execute(
                    "SELECT supplier_id FROM suppliers WHERE supplier_id = %s",(s_id,))
            if cursor.fetchone():
                print("❌ Supplier with this id already existe! ")
                return
            # input Data
            p_id = int(input("Enter Product id: "))
            name= input("Enter Suppliers Name: ").strip().title()
            contect = int(input("Enter Supplier Number: "))

            # Insert Data 
            cursor.execute('''INSERT INTO suppliers (supplier_id, product_id,name, contect )
                            VALUES (%s, %s, %s, %s)''',(s_id, p_id, name, contect))

            connection.commit()
            print(f"✅(Supplier id {s_id} Add Successfully.)")

        except Error as e:
            print(f"❌ Error Adding Suppliers details: {e}")
        finally:
            cursor.close()
            connection.close()
    def update():
        connection = get_connection()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            s_id = int(input("Enter Supplier id to Update: "))

            # check if Suppliers id exists in Suppliers Table
            cursor.execute("SELECT supplier_id FROM suppliers WHERE supplier_id = %s",(s_id,))
            if not cursor.fetchone():
                print("❌ Suppliers with this id already existe!")
                return
            p_id = int(input("Enter New Product id (or press Enter to keep current): "))
            name = (input("Enter New Supplier Name (or press Enter to keep current): ")).strip().title()
            
            contect = int(input("Enter Supplier Contect Number (or press Enter to keep current): "))
            if p_id:
                cursor.execute("UPDATE suppliers SET product_id = %s WHERE supplier_id = %s",(p_id, s_id))
            if name:
                cursor.execute("UPDATE suppliers SET name = %s WHERE supplier_id = %s",(name, s_id))
            
            if contect:
                cursor.execute("UPDATE suppliers SET contect = %s WHERE supplier_id = %s",(contect, s_id))


            connection.commit()
            print(f"✅ Suppliers at this id({s_id}) Updated Successfully.")

        except Error as e:
            print(f"❌ Error in Updating Supplier Details: {e}")
        finally:
            cursor.close()
            connection.close()

    def delete():
        connection = get_connection()
        if not connection:
            print("Error connection not found")
            return
        try:
            cursor = connection.cursor()
            s_id = int(input("Enter Supplier id: "))

            # check if Supplier id existe
            cursor.execute("SELECT supplier_id FROM suppliers WHERE supplier_id = %s",(s_id,))
            if not cursor.fetchone():
                print("❌ Supplier with this id not existe!")
                return
            
            cursor.execute("DELETE FROM suppliers WHERE supplier_id = %s",(s_id,))
            connection.commit()
            print(f"✅ Suppliers with this id {s_id} Delete Successfully!")
        except Error as e:
            print(f"❌Error: deleting Suppliers is {e}")
        finally:
            cursor.close()
            connection.close()
    
    def search_products():
        connection = get_connection()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            s_id = int(input("Enter Supplier id for search: "))
            
            # Check if Supplier id existe in sales Table
            cursor.execute("SELECT supplier_id FROM suppliers WHERE supplier_id = %s",(s_id,))
            if not cursor.fetchone():
                print("❌This Suppplier id not Existe in Supplier Table")
                return
            cursor.execute("SELECT * FROM suppliers WHERE supplier_id = %s",(s_id,))
            result = cursor.fetchall()
            if result:
                print(f"\n📋 Suppliers Details (Supplier id {s_id}):")
                print("-" * 60)
                for row in result:
                    print(f"SUPPLIERS: Product id = {row[1]} | Name = {row[2]} | Contect = {row[3]} ")
            
            connection.commit()
        except Error as e:
            print(f"❌Error: searching Suppliers id {e}")
        finally:
            cursor.close()
            connection.close()

    def show_all_products():
        connection = get_connection()
        if not connection:
            print("❌ Connection not found")
            return
        try:
            cursor = connection.cursor()
            
            # Check if Suppliers table not empty
            cursor.execute("SELECT * FROM suppliers")
            result = cursor.fetchall()
            if result:
                print(f"\n📋 SHOW ALL Suppliers Details:")
                print("-" * 60)
                print(result)
            else:
                print("❌Suppliers Table is Empty.")
            connection.commit()
        
        except Error as e:
            print(f"❌Error show all data {e}")
        finally:
            cursor.close()
            connection.close()
        
    def export_to_csv():
        connection = get_connection()
        if not connection:
            print("❌ Connection not found")
            return
        
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM suppliers")
        rows = cursor.fetchall()

        with open(f"suppliers.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)


    while True:
        print("=" * 50)
        print('''
                PRODUCTS DETAILS
            1. ADD 
            2. UPDATE 
            3. DELETE 
            4. SEARCH PRODUCT 
            5. SHOW ALL DATA 
            6. Export to CSV File 
            7. EXIT 
            
        ''')
        user = int(input("Enter your choice: "))
        if user == 1:
            add()
        elif user == 2:
            update()
        elif user == 3:
            delete()
        elif user == 4:
            search_products()
        elif user == 5:
            show_all_products()
        elif user == 6:
            export_to_csv()
        elif user == 7:
            break
        else:
            print("❌ Invalid choice")


while True:
    print("*"*80)
    print('''
            Add, Update, Delete, Search, Show all 
          Your options =
          Products Details = 1
          Inventory Details = 2
          Sales Details = 3
          Suppliers = 4
          Exit = 5
''')

    try:
        user = int(input("Enter Your choice: "))

        if user == 1:
            Products()
        elif user== 2:
            Inventory()
        elif user == 3:
            Sales()
        elif user == 4:
            Suppliers()
        elif user == 5:
            break
        else:
            print("❌Invalid Choice!")
        
    except ValueError as v:
        print("❌Error :",v)
