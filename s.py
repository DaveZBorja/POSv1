import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import csv

# Login Portal Class
class LoginPortal:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("Login Portal")
        self.root.geometry("300x150")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Username").pack(pady=10)
        self.username = tk.Entry(self.root)
        self.username.pack(pady=5)

        tk.Label(self.root, text="Password").pack(pady=10)
        self.password = tk.Entry(self.root, show='*')
        self.password.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.authenticate).pack(pady=15)

    def authenticate(self):
        username = self.username.get()
        password = self.password.get()

        if username == "admin" and password == "password":
            self.root.destroy()
            self.on_success()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

# POS Application Class
class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("POS System")
        self.root.geometry("800x600")
        self.root.configure(bg='#ffffff')

        # Create database connection
        self.conn = sqlite3.connect('pos.db')
        self.c = self.conn.cursor()

        # Set up GUI
        self.setup_gui()

    def setup_gui(self):
        # Create a frame for the dashboard
        self.dashboard_frame = tk.Frame(self.root, bg='#2196F3', height=50)
        self.dashboard_frame.pack(fill=tk.X, side=tk.TOP)

        # Dashboard Buttons
        self.home_button = tk.Button(self.dashboard_frame, text="Home", command=self.show_home, bg='#0D47A1', fg='white', width=10)
        self.home_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.products_button = tk.Button(self.dashboard_frame, text="Products", command=self.show_products, bg='#0D47A1', fg='white', width=10)
        self.products_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.query_button = tk.Button(self.dashboard_frame, text="Query", command=self.show_query, bg='#0D47A1', fg='white', width=10)
        self.query_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.export_button = tk.Button(self.dashboard_frame, text="Export", command=self.export_data, bg='#0D47A1', fg='white', width=10)
        self.export_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Main content area
        self.content_frame = tk.Frame(self.root, bg='#ffffff')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Initialize with the home page
        self.show_home()

    def show_home(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        tk.Label(self.content_frame, text="Welcome to the POS System", font=("Arial", 16, "bold"), bg='#ffffff').pack(pady=20)

    def show_products(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Add Product Section
        add_product_frame = tk.LabelFrame(self.content_frame, text="Add Product", padx=5, pady=5, bg='#e0e0e0')
        add_product_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(add_product_frame, text="Product Name", bg='#e0e0e0').grid(row=0, column=0, padx=5, pady=5)
        self.product_name = tk.Entry(add_product_frame, width=20)
        self.product_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_product_frame, text="Price", bg='#e0e0e0').grid(row=1, column=0, padx=5, pady=5)
        self.price = tk.Entry(add_product_frame, width=20)
        self.price.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_product_frame, text="Quantity", bg='#e0e0e0').grid(row=2, column=0, padx=5, pady=5)
        self.quantity = tk.Entry(add_product_frame, width=20)
        self.quantity.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(add_product_frame, text="Add Product", command=self.add_product, bg='#4CAF50', fg='white').grid(row=3, column=0, columnspan=2, pady=10)

        # Update Product Section
        update_product_frame = tk.LabelFrame(self.content_frame, text="Update Product", padx=5, pady=5, bg='#e0e0e0')
        update_product_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(update_product_frame, text="Product ID", bg='#e0e0e0').grid(row=0, column=0, padx=5, pady=5)
        self.update_product_id = tk.Entry(update_product_frame, width=20)
        self.update_product_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(update_product_frame, text="New Name", bg='#e0e0e0').grid(row=1, column=0, padx=5, pady=5)
        self.update_product_name = tk.Entry(update_product_frame, width=20)
        self.update_product_name.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(update_product_frame, text="New Price", bg='#e0e0e0').grid(row=2, column=0, padx=5, pady=5)
        self.update_price = tk.Entry(update_product_frame, width=20)
        self.update_price.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(update_product_frame, text="New Quantity", bg='#e0e0e0').grid(row=3, column=0, padx=5, pady=5)
        self.update_quantity = tk.Entry(update_product_frame, width=20)
        self.update_quantity.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(update_product_frame, text="Update Product", command=self.update_product, bg='#FF9800', fg='white').grid(row=4, column=0, columnspan=2, pady=10)

    def show_query(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        query_product_frame = tk.LabelFrame(self.content_frame, text="Query Products", padx=5, pady=5, bg='#e0e0e0')
        query_product_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        tk.Label(query_product_frame, text="Query by Name", bg='#e0e0e0').pack(pady=5)
        self.query_name = tk.Entry(query_product_frame, width=20)
        self.query_name.pack(pady=5)

        tk.Button(query_product_frame, text="Query by Name", command=self.query_product_by_name, bg='#2196F3', fg='white').pack(pady=5)
        
        tk.Button(query_product_frame, text="Delete by Name", command=self.delete_product_by_name, bg='#F44336', fg='white').pack(pady=5)

        self.query_results = tk.Text(query_product_frame, height=10, width=60)
        self.query_results.pack(pady=5)

        tk.Button(query_product_frame, text="Query All Products", command=self.query_products, bg='#2196F3', fg='white').pack(pady=5)

    def add_product(self):
        name = self.product_name.get()
        price = self.price.get()
        quantity = self.quantity.get()
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.c.execute("INSERT INTO products (name, price, quantity, date_added) VALUES (?, ?, ?, ?)", (name, price, quantity, date_added))
            self.conn.commit()
            messagebox.showinfo("Success", "Product added successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_product(self):
        product_id = self.update_product_id.get()
        new_name = self.update_product_name.get()
        new_price = self.update_price.get()
        new_quantity = self.update_quantity.get()

        try:
            self.c.execute("UPDATE products SET name = ?, price = ?, quantity = ? WHERE id = ?", (new_name, new_price, new_quantity, product_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Product updated successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def query_product_by_name(self):
        name = self.query_name.get()
        self.c.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + name + '%',))
        rows = self.c.fetchall()
        self.query_results.delete(1.0, tk.END)
        for row in rows:
            self.query_results.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Price: {row[2]}, Quantity: {row[3]}, Date Added: {row[4]}\n")

    def delete_product_by_name(self):
        name = self.query_name.get()
        try:
            self.c.execute("DELETE FROM products WHERE name = ?", (name,))
            self.conn.commit()
            if self.c.rowcount > 0:
                messagebox.showinfo("Success", "Product deleted successfully")
            else:
                messagebox.showwarning("Not Found", "No product found with the given name")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def query_products(self):
        self.c.execute("SELECT * FROM products")
        rows = self.c.fetchall()
        self.query_results.delete(1.0, tk.END)
        for row in rows:
            self.query_results.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Price: {row[2]}, Quantity: {row[3]}, Date Added: {row[4]}\n")

    def export_data(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not filepath:
            return

        self.c.execute('SELECT id, name, price, quantity, date_added FROM products')
        rows = self.c.fetchall()
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Product Name", "Price", "Quantity", "Date Added"])
            writer.writerows(rows)
        messagebox.showinfo("Success", "Data exported successfully")

    def show_services(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        tk.Label(self.content_frame, text="Services Information", font=("Arial", 16, "bold"), bg='#ffffff').pack(pady=20)

    def show_info(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        tk.Label(self.content_frame, text="Additional Information", font=("Arial", 16, "bold"), bg='#ffffff').pack(pady=20)

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    login = LoginPortal(root, lambda: POSApp(tk.Tk()))
    root.mainloop()
