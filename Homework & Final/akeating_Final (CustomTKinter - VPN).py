import tkinter as tk
import customtkinter as ctk
import mysql.connector
from tkinter import Toplevel
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Establish the database connection 

def create_conn():
    conn = mysql.connector.connect(
        host="128.198.162.191",
        user="finalUser",
        password="itsover!",
        database="finaldb"
    )
    return conn

# Open db connection

conn = create_conn()
cursor = conn.cursor()

# Function to check and create tables if they don't exist

def check_and_create_tables():

    # Check if the akeating_products table exists

    cursor.execute("SHOW TABLES LIKE 'akeating_products';")
    result = cursor.fetchone()
    if not result:
        create_products_table()

    # Check if the akeating_sales table exists

    cursor.execute("SHOW TABLES LIKE 'akeating_sales';")
    result = cursor.fetchone()
    if not result:
        create_sales_table()

# Function to create akeating_products table

def create_products_table():
    create_query = """
    CREATE TABLE akeating_products (
        productID INT AUTO_INCREMENT PRIMARY KEY,
        productName VARCHAR(45),
        productPrice DECIMAL(8,2)
    );
    """
    cursor.execute(create_query)
    print("Created table akeating_products.")

# Function to create akeating_sales table

def create_sales_table():
    create_query = """
    CREATE TABLE akeating_sales (
        PK INT AUTO_INCREMENT PRIMARY KEY,
        productID INT,
        unitSales INT,
        salesDate DATE,
        FOREIGN KEY (productID) REFERENCES akeating_products(productID)
    );
    """
    cursor.execute(create_query)
    print("Created table akeating_sales.")

# Check and create tables on startup

check_and_create_tables()

# Build out the basics of our application window

ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("light")
window = ctk.CTk()
window.geometry("500x375")
window.title("CTk")

# Create form elements to enter records in our db

productName_label = ctk.CTkLabel(master=window, text="Product Name")
productName_label.grid(row=0, column=1, ipadx=1, padx=200, ipady=2, pady=2, sticky="w")
productName_input = ctk.CTkEntry(master=window)
productName_input.grid(row=1, column=1, ipadx=5, padx=175, sticky="w")

productPrice_label = ctk.CTkLabel(master=window, text="Product Price")
productPrice_label.grid(row=2, column=1, ipadx=1, padx=205, ipady=2, pady=2, sticky="w")
productPrice_input = ctk.CTkEntry(master=window)
productPrice_input.grid(row=3, column=1, ipadx=5, padx=175, sticky="w")

unitSold_label = ctk.CTkLabel(master=window, text="Units Sold")
unitSold_label.grid(row=4, column=1, ipadx=1, padx=215, ipady=2, pady=2, sticky="w")
unitSold_input = ctk.CTkEntry(master=window)
unitSold_input.grid(row=5, column=1, ipadx=5, padx=175, sticky="w")

salesDate_label = ctk.CTkLabel(master=window, text="Sales Date (YYYY-MM-DD)")
salesDate_label.grid(row=6, column=1, ipadx=1, padx=175, ipady=2, pady=2, sticky="w")
salesDate_input = ctk.CTkEntry(master=window)
salesDate_input.grid(row=7, column=1, ipadx=5, padx=175, sticky="w")

#-------------------------------------INSERT RECORDS---------------------------------------

def save_sale():
    productName = productName_input.get()
    productPrice = float(productPrice_input.get())  
    unitSold = int(unitSold_input.get())  
    salesDate = salesDate_input.get()

    # First insert the product into akeating_products table if not exists
    query2 = "INSERT INTO akeating_products (productName, productPrice) VALUES (%s, %s)"
    val2 = (productName, productPrice)
    cursor.execute(query2, val2)
    conn.commit()

    # Now insert the sale into akeating_sales table
    query = """
    INSERT INTO akeating_sales (productID, unitSales, salesDate)
    VALUES ((SELECT productID FROM akeating_products WHERE productName = %s LIMIT 1), %s, %s)
    """
    val = (productName, unitSold, salesDate)
    cursor.execute(query, val)
    conn.commit()

    clear_inputs()

# Define function to clear inputs

def clear_inputs():
    productName_input.delete(0, tk.END)
    productPrice_input.delete(0, tk.END)
    unitSold_input.delete(0, tk.END)
    salesDate_input.delete(0, tk.END)


# Add a button for inserting records

insert_button = ctk.CTkButton(master=window, text="Save Sale", command=save_sale)
insert_button.grid(row=8, column=1, padx=0, pady=10)

#-------------------------------------DISPLAY RECORDS---------------------------------------

def show_records():

    # Create a new window

    graph_window = Toplevel()
    graph_window.title("Bar Graph")
    graph_window.geometry("600x400")

    # Query to fetch product name, sales, and price data

    query = """
    SELECT akeating_products.productName, SUM(akeating_sales.unitSales * akeating_products.productPrice) 
    FROM akeating_products
    INNER JOIN akeating_sales ON akeating_products.productID = akeating_sales.productID
    GROUP BY akeating_products.productName 
    ORDER BY akeating_products.productName
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Process the query results
    # Extract categories

    categories = [row[0] for row in results]  
    values = [row[1] for row in results]

    # Create a bar graph using Matplotlib

    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(categories, values, color='darkblue')
    ax.set_title("Sales by Product")
    ax.set_ylabel("Total Dollar Sales")
    ax.set_xlabel("Product Name")

    # Embed the Matplotlib figure into the Tkinter window

    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

# Create a button that will search for records

search_button = ctk.CTkButton(master=window, text="Show Sales Graph", command=show_records)
search_button.grid(row=9, column=1, padx=0, pady=10)

window.mainloop()