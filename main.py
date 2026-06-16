import tkinter as tk
from tkinter import ttk

from database import accessing_sql_db
from gui import AssetAddingGUI, ViewDataBaseGUI
from config import types_of_assets

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Asset Inventory")
        self.root.geometry("400x280")
        self.root.resizable(False, False)
        self.create_widgets()
    def create_widgets(self):
        tk.Label(self.root, text = "IT Asset Management System", bg = "#5285A1", fg = "white", width= 100, font = ("Arial", 20)).pack(pady= 3)
        tk.Label(self.root, text = "Add a New Asset", bg = "#6DA9C9", fg = "white", width= 100, font = ("Arial", 17)).pack(pady = 3)
        # Adding to Asset Inventory
        tk.Label(self.root, text = "Type of Asset:", font= ("Arial", 15), justify="center").pack()
        self.type_of_asset_inp = ttk.Combobox(self.root, values = types_of_assets, width= 25, state= 'readonly')
        self.type_of_asset_inp.set(types_of_assets[0])
        self.type_of_asset_inp.pack()
        tk.Button(self.root, text = "Add an Asset", command=self.asset_adding, padx= 80, pady=2).pack(pady=5)
        # Viewing Asset Database
        tk.Label(self.root, text = "View Asset Inventory", bg = "#6DA9C9", fg = "white", width= 100, font = ("Arial", 17)).pack(pady = 3)
        tk.Label(self.root, text = "View Database", font= ("Arial", 15), justify="center").pack()
        tk.Button(self.root, text = "View", command=self.view_asset_database, padx= 100, pady=2).pack(pady=5)
    # Redirects user to Adding an Asset Window
    def asset_adding(self):
        asset_type_var = self.type_of_asset_inp.get()
        # If the error Label already exists it is destroyed to prevent label stacking
        if hasattr(self, 'type_of_asset_error_label'):
            self.type_of_asset_error_label.destroy()
        # Checks if the combobox value is it's default value
        if asset_type_var == types_of_assets[0]:
            self.type_of_asset_error_label = tk.Label(self.root, text="Please select a type of asset", fg="red")
            self.type_of_asset_error_label.pack()
        # If it isn't the Adding an Asset Window is opened
        else:
            add_asset_window = tk.Toplevel(self.root)
            AssetAddingGUI(add_asset_window, asset_type_var)
    # Opens Database Window
    def view_asset_database(self):
        view_database_window = tk.Toplevel(self.root)
        ViewDataBaseGUI(view_database_window)
        
# Main global Function to run the GUI
if __name__ == "__main__":
    accessing_sql_db()
    root = tk.Tk()
    main_window = MainGUI(root)
    root.mainloop()