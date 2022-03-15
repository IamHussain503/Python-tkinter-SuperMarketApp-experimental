import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import os
import datetime


def main():
    root = tk.Tk()
    root.title("Product List")
    root.geometry("800x600")
    app = ProductList(root)
    root.mainloop()


class ProductList:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self.frame.pack()
        self.create_widgets()
        self.create_db()
        self.create_table()
        self.get_products()

    def create_widgets(self):
        self.lbl_title = ttk.Label(self.frame, text="Product List")
        self.lbl_title.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.lbl_search = ttk.Label(self.frame, text="Search:")
        self.lbl_search.grid(row=1, column=0, sticky="e")
        self.ent_search = ttk.Entry(self.frame, width=30)
        self.ent_search.grid(row=1, column=1, sticky="ew")
        self.btn_search = ttk.Button(
            self.frame, text="Search", command=self.search_product)
        self.btn_search.grid(row=1, column=2, sticky="ew")
        self.lbl_product = ttk.Label(self.frame, text="Product:")
        self.lbl_product.grid(row=2, column=0, sticky="e")
        self.ent_product = ttk.Entry(self.frame, width=30)
        self.ent_product.grid(row=2, column=1, sticky="ew")
        self.lbl_price = ttk.Label(self.frame, text="Price:")
        self.lbl_price.grid(row=2, column=2, sticky="e")
        self.ent_price = ttk.Entry(self.frame, width=30)
        self.ent_price.grid(row=2, column=3, sticky="ew")
        self.lbl_purchasedate = ttk.Label(self.frame, text="Purchase Date:")
        self.lbl_purchasedate.grid(row=3, column=0, sticky="e")
        self.ent_purchasedate = ttk.Entry(self.frame, width=30)
        self.ent_purchasedate.grid(row=3, column=1, sticky="ew")
        self.lbl_inventory = ttk.Label(self.frame, text="Inventory:")
        self.lbl_inventory.grid(row=3, column=2, sticky="e")
        self.ent_inventory = ttk.Entry(self.frame, width=30)
        self.ent_inventory.grid(row=3, column=3, sticky="ew")
        self.btn_add = ttk.Button(
            self.frame, text="Add", command=self.add_product)
        self.btn_add.grid(row=4, column=0, sticky="ew")
        self.btn_remove = ttk.Button(
            self.frame, text="Remove", command=self.remove_product)
        self.btn_remove.grid(row=4, column=1, sticky="ew")
        self.btn_update = ttk.Button(
            self.frame, text="Update", command=self.update_product)
        self.btn_update.grid(row=4, column=2, sticky="ew")
        self.btn_clear = ttk.Button(
            self.frame, text="Clear", command=self.clear_product)
        self.btn_clear.grid(row=4, column=3, sticky="ew")
        self.lbl_product_list = ttk.Label(self.frame, text="Product List:")
        self.lbl_product_list.grid(row=5, column=0, sticky="ew")
        self.lbl_product_list_display = ttk.Label(self.frame, text="")
        self.lbl_product_list_display.grid(row=6, column=0, sticky="ew")
        self.lbl_product_list_display.bind(
            "<Button-1>", self.display_product_list)
        self.lbl_product_list_display.bind(
            "<Double-Button-1>", self.display_product_list)

    def create_db(self):
        self.db = sqlite3.connect("product.db")
        self.cursor = self.db.cursor()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS product(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            price REAL,
            purchasedate TEXT,
            inventory INTEGER
            )""")

    def get_products(self):
        self.cursor.execute("SELECT * FROM product")
        self.products = self.cursor.fetchall()

    def add_product(self):
        product = self.ent_product.get()
        price = self.ent_price.get()
        purchasedate = self.ent_purchasedate.get()
        inventory = self.ent_inventory.get()
        if product == "" or price == "" or purchasedate == "" or inventory == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            self.cursor.execute("INSERT INTO product(product, price, purchasedate, inventory) VALUES(?, ?, ?, ?)", (
                product, price, purchasedate, inventory))
            self.db.commit()
            self.get_products()
            self.clear_product()
            self.display_product_list()

    def remove_product(self):
        product = self.ent_product.get()
        if product == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            self.cursor.execute(
                "DELETE FROM product WHERE product = ?", (product,))
            self.db.commit()
            self.get_products()
            self.clear_product()
            self.display_product_list()

    def update_product(self):
        product = self.ent_product.get()
        price = self.ent_price.get()
        purchasedate = self.ent_purchasedate.get()
        inventory = self.ent_inventory.get()
        if product == "" or price == "" or purchasedate == "" or inventory == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            self.cursor.execute("UPDATE product SET price = ?, purchasedate = ?, inventory = ? WHERE product = ?", (
                price, purchasedate, inventory, product))
            self.db.commit()
            self.get_products()
            self.clear_product()
            self.display_product_list()

    def clear_product(self):
        self.ent_product.delete(0, "end")
        self.ent_price.delete(0, "end")
        self.ent_purchasedate.delete(0, "end")
        self.ent_inventory.delete(0, "end")

    def search_product(self):
        product = self.ent_search.get()
        if product == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            self.cursor.execute(
                "SELECT * FROM product WHERE product = ?", (product,))
            self.products = self.cursor.fetchall()
            self.clear_product()
            self.display_product_list()

    def display_product_list(self, event=None):
        self.lbl_product_list_display.config(text="")
        for product in self.products:
            self.lbl_product_list_display.config(
                text=self.lbl_product_list_display.cget("text") + "\n" + str(product))


if __name__ == "__main__":
    main()
