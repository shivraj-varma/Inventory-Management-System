
# Inventory Management System (IMS) 📦

A robust command-line interface (CLI) application built with **Python** and **MySQL** to manage product stock, track inventory levels, record sales, and maintain supplier information.

## 🚀 Features

The system is divided into four core modules, each supporting full **CRUD** (Create, Read, Update, Delete) operations:

*   **Product Management:** Add, update, and categorize products with SKU tracking.
*   **Inventory Tracking:** Monitor stock levels, set minimum stock alerts, and track last updated dates.
*   **Sales Records:** Log sales transactions. The system automatically calculates total amounts based on the product's unit price.
*   **Supplier Directory:** Maintain a database of suppliers linked to specific products.
*   **Data Export:** Export any table (Products, Inventory, Sales, Suppliers) directly to **CSV files** for external reporting.

## 🛠️ Tech Stack

*   **Language:** Python 3.x
*   **Database:** MySQL
*   **Libraries:** 
    *   `mysql-connector-python` (Database connectivity)
    *   `csv` (Data export)

## 📋 Database Schema

The project uses a relational database `i_m_s_db` with the following tables:
1.  **products**: `product_id`, `name`, `category`, `description`, `unit_price`, `sku`.
2.  **inventory**: `inventory_id`, `product_id` (FK), `quantity`, `min_stock`, `last_updated`.
3.  **sales**: `sales_id`, `product_id` (FK), `quantity_sold`, `sale_date`, `total_amount`.
4.  **suppliers**: `supplier_id`, `product_id` (FK), `name`, `contact`.

## ⚙️ Setup and Installation

### 1. Prerequisites
*   Install **MySQL Server** on your machine.
*   Install **Python**.

### 2. Install Dependencies
Install the MySQL connector using pip:
```bash
pip install mysql-connector-python
```

### 3. Database Configuration
Open `main.py` and update the `get_connection()` function with your MySQL credentials:
```python
connection = mysql.connector.connect(
    host="localhost",
    user="root",        # Your MySQL username
    password="your_password", # Your MySQL password
    database="i_m_s_db"
)
```

### 4. Initialize the Database
1. Create a database named `i_m_s_db` in your MySQL server:
   ```sql
   CREATE DATABASE i_m_s_db;
   ```
2. Ensure you call the `create_tables()` function once to generate the necessary tables.

### 5. Running the Application
```bash
python main.py
```

## 📖 How to Use

Once the script starts, you will be presented with a main menu:
1.  **Products Details:** Manage the master list of items you sell.
2.  **Inventory Details:** Manage the stock counts and restocking thresholds.
3.  **Sales Details:** Record new sales (this module fetches the unit price from the Products table automatically).
4.  **Suppliers:** Manage contact information for your vendors.
5.  **Export:** In each sub-menu, use option `6` to generate a CSV file of that specific data.

## ⚠️ Important Note
*   **Foreign Keys:** Ensure a Product ID exists in the `products` table before trying to add it to Inventory, Sales, or Suppliers, as these tables rely on `product_id` as a reference.
*   **Error Handling:** The system includes try-except blocks to handle database connection issues and input errors.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/your-username/your-repo-name/issues).

---

### Project Structure
```text
.
├── main.py            # Main application logic
├── products.csv       # Exported product data (generated)
├── inventory.csv      # Exported inventory data (generated)
├── sales.csv          # Exported sales data (generated)
└── suppliers.csv      # Exported supplier data (generated)
```

**Developed by [Your Name]**
