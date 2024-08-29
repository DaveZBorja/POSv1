import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd
import os

# Database setup
def setup_database():
    conn = sqlite3.connect('pos_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                 id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 quantity INTEGER NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS parts (
                 id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 quantity INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

# Add item to inventory
def add_inventory_item(name, quantity):
    conn = sqlite3.connect('pos_system.db')
    c = conn.cursor()
    c.execute('INSERT INTO inventory (name, quantity) VALUES (?, ?)', (name, quantity))
    conn.commit()
    conn.close()

# Transfer units in/out
def transfer_units(name, quantity, transfer_type):
    conn = sqlite3.connect('pos_system.db')
    c = conn.cursor()
    if transfer_type == 'in':
        c.execute('UPDATE inventory SET quantity = quantity + ? WHERE name = ?', (quantity, name))
    elif transfer_type == 'out':
        c.execute('UPDATE inventory SET quantity = quantity - ? WHERE name = ?', (quantity, name))
    conn.commit()
    conn.close()

# Add part
def add_part(name, quantity):
    conn = sqlite3.connect('pos_system.db')
    c = conn.cursor()
    c.execute('INSERT INTO parts (name, quantity) VALUES (?, ?)', (name, quantity))
    conn.commit()
    conn.close()

# Export data
def export_data():
    conn = sqlite3.connect('pos_system.db')
    inventory_df = pd.read_sql_query('SELECT * FROM inventory', conn)
    parts_df = pd.read_sql_query('SELECT * FROM parts', conn)
    conn.close()
    
    if not os.path.exists('exports'):
        os.makedirs('exports')
    
    inventory_df.to_csv('exports/inventory.csv', index=False)
    parts_df.to_csv('exports/parts.csv', index=False)

    messagebox.showinfo("Export", "Data exported successfully!")

# Create main application window
class POSApp:
    def __init__(self, root):
        self.root = root
        root.title("POS System")

        self.create_widgets()

    def create_widgets(self):
        # Inventory Section
        tk.Label(self.root, text="Inventory Management").grid(row=0, column=0, columnspan=2)

        tk.Label(self.root, text="Item Name:").grid(row=1, column=0)
        self.item_name_entry = tk.Entry(self.root)
        self.item_name_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Quantity:").grid(row=2, column=0)
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=2, column=1)

        tk.Button(self.root, text="Add to Inventory", command=self.add_inventory).grid(row=3, column=0, columnspan=2)

        tk.Label(self.root, text="Transfer In/Out").grid(row=4, column=0, columnspan=2)

        tk.Button(self.root, text="Transfer In", command=self.transfer_in).grid(row=5, column=0)
        tk.Button(self.root, text="Transfer Out", command=self.transfer_out).grid(row=5, column=1)

        tk.Label(self.root, text="Part Management").grid(row=6, column=0, columnspan=2)

        tk.Label(self.root, text="Part Name:").grid(row=7, column=0)
        self.part_name_entry = tk.Entry(self.root)
        self.part_name_entry.grid(row=7, column=1)

        tk.Label(self.root, text="Quantity:").grid(row=8, column=0)
        self.part_quantity_entry = tk.Entry(self.root)
        self.part_quantity_entry.grid(row=8, column=1)

        tk.Button(self.root, text="Add Part", command=self.add_part).grid(row=9, column=0, columnspan=2)

        tk.Button(self.root, text="Export Data", command=export_data).grid(row=10, column=0, columnspan=2)

    def add_inventory(self):
        name = self.item_name_entry.get()
        quantity = self.quantity_entry.get()
        if name and quantity:
            try:
                quantity = int(quantity)
                add_inventory_item(name, quantity)
                messagebox.showinfo("Success", "Item added to inventory!")
            except ValueError:
                messagebox.showerror("Error", "Quantity must be an integer!")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def transfer_in(self):
        name = self.item_name_entry.get()
        quantity = self.quantity_entry.get()
        if name and quantity:
            try:
                quantity = int(quantity)
                transfer_units(name, quantity, 'in')
                messagebox.showinfo("Success", "Units transferred in!")
            except ValueError:
                messagebox.showerror("Error", "Quantity must be an integer!")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def transfer_out(self):
        name = self.item_name_entry.get()
        quantity = self.quantity_entry.get()
        if name and quantity:
            try:
                quantity = int(quantity)
                transfer_units(name, quantity, 'out')
                messagebox.showinfo("Success", "Units transferred out!")
            except ValueError:
                messagebox.showerror("Error", "Quantity must be an integer!")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def add_part(self):
        name = self.part_name_entry.get()
        quantity = self.part_quantity_entry.get()
        if name and quantity:
            try:
                quantity = int(quantity)
                add_part(name, quantity)
                messagebox.showinfo("Success", "Part added!")
            except ValueError:
                messagebox.showerror("Error", "Quantity must be an integer!")
        else:
            messagebox.showerror("Error", "All fields are required!")

if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    app = POSApp(root)
    root.mainloop()
