import tkinter as tk
from tkinter import ttk
import sqlite3
# Import choices and database variables
from config import types_of_assets, status_options, month_options
from database import db_file

# Asset Adding Window Class Declaration
class AssetAddingGUI:
    def __init__(self, window, asset_type):
        self.window = window
        self.asset_type = asset_type
        self.window.title("Adding a New Asset")
        self.window.geometry("400x540")
        self.window.resizable(False, False)
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self.window, text = f"Register New {self.asset_type} Asset", bg = "#6DA9C9", fg = "white", width= 100, font = ("Arial", 17)).pack()
        if self.asset_type in types_of_assets[1:]:
            # Asset Name Input Field
            tk.Label(self.window, text = "Asset Name").pack()
            self.asset_name_inp = tk.Entry(self.window)
            self.asset_name_inp.pack()
            # Asset Type Input Field
            ttk.Separator(self.window, orient="horizontal").pack(fill='x', pady=10)
            tk.Label(self.window, text = "Asset Type").pack()
            self.asset_type_inp = tk.Entry(self.window)
            self.asset_type_inp.pack()
            # IP Address Input Field (Hardware assets only)
            if self.asset_type == "Hardware":
                ttk.Separator(self.window, orient="horizontal").pack(fill='x', pady=10)
                self.ip_frame = tk.Frame(self.window)
                self.ip_frame.pack()
                tk.Label(self.ip_frame, text = "IP Address").pack()
                self.ip_address_inp1 = tk.Entry(self.ip_frame, width= 3)
                self.ip_address_inp1.pack(side=tk.LEFT, padx = 5)
                tk.Label(self.ip_frame, text = '.').pack(side= tk.LEFT, padx = 5)
                self.ip_address_inp2 = tk.Entry(self.ip_frame, width= 3)
                self.ip_address_inp2.pack(side=tk.LEFT, padx = 5)
                tk.Label(self.ip_frame, text = '.').pack(side= tk.LEFT, padx = 5)
                self.ip_address_inp3 = tk.Entry(self.ip_frame, width= 3)
                self.ip_address_inp3.pack(side=tk.LEFT, padx = 5)
                tk.Label(self.ip_frame, text = '.').pack(side= tk.LEFT, padx = 5)
                self.ip_address_inp4 = tk.Entry(self.ip_frame, width= 3)
                self.ip_address_inp4.pack(side=tk.LEFT, padx = 5)
            # Renewal Date boolean logic 
            ttk.Separator(self.window, orient="horizontal").pack(fill='x', pady=10)
            self.add_renewal_date = tk.BooleanVar()
            # Renewal Date Input Field
            ttk.Checkbutton(self.window, text = "Add Renewal Date?", variable= self.add_renewal_date, command=self.toggle_date_field).pack()
            self.date_frame = tk.Frame(self.window)
            tk.Label(self.date_frame, text = "Renewal Date").pack()
            # Day selection Field
            self.renewal_day_inp = tk.Spinbox(self.date_frame, width= 3, from_=1, to=31, state='readonly')
            self.renewal_day_inp.pack(side = tk.LEFT, padx = 5)
            # Month Selection Field
            tk.Label(self.date_frame, text = "/").pack(side= tk.LEFT, padx=5)
            self.renewal_month_inp = ttk.Combobox(self.date_frame, width= 9, values = month_options, state='readonly')
            self.renewal_month_inp.pack(side = tk.LEFT, padx = 5)
            # Year Selection Field
            tk.Label(self.date_frame, text = "/").pack(side= tk.LEFT, padx=5)
            renewal_year_inp = tk.Spinbox(self.date_frame, width= 4, from_=2026, to=2100, state='readonly')
            renewal_year_inp.pack(side = tk.LEFT, padx = 5)
            # Status Input Field
            ttk.Separator(self.window, orient="horizontal").pack(fill='x', pady=10)
            tk.Label(self.window, text = "Status").pack()
            self.status_input = ttk.Combobox(self.window, values = status_options, state = "readonly")
            self.status_input.set(status_options[0])
            self.status_input.pack()
            # Adding to Database Button
            ttk.Separator(self.window, orient="horizontal").pack(fill='x', pady=10)
            tk.Button(self.window, text = "Add to Database", command=self.add_to_database, padx= 80, pady=2).pack(pady = 10)
        
    def toggle_date_field(self):
        if self.add_renewal_date.get():
            self.date_frame.pack()
        else:
            self.date_frame.pack_forget()

    # Validates user input and appends it to the database if the rules are met
    def add_to_database(self):
        # Storing user input in corresponding variables 
        asset_name_var = self.asset_name_inp.get()
        asset_type_var = self.asset_type_inp.get()
        asset_status_var = self.status_input.get()
        asset_ip_address_var1 = self.ip_address_inp1.get().strip() if self.asset_type == "Hardware" else "N/A"
        asset_ip_address_var2 = self.ip_address_inp2.get().strip() if self.asset_type == "Hardware" else "N/A"
        asset_ip_address_var3 = self.ip_address_inp3.get().strip() if self.asset_type == "Hardware" else "N/A"
        asset_ip_address_var4 = self.ip_address_inp4.get().strip() if self.asset_type == "Hardware" else "N/A"
        asset_ip_address_var = f'{asset_ip_address_var1}.{asset_ip_address_var2}.{asset_ip_address_var3}.{asset_ip_address_var4}'
        name_valid = type_valid = status_valid = False
        ip_address_valid = True if self.asset_type != "Hardware" else False
        
        if hasattr(self, 'name_error'):
            self.name_error.destroy()
        if hasattr(self, 'type_error'):
            self.type_error.destroy()
        if hasattr(self, 'ip_address_error'):
            self.ip_address_error.destroy()
        if hasattr(self, 'status_error'):
            self.status_error.destroy()

        # Asset Name Validation
        if asset_name_var.strip() == "": # Presence Check
            self.name_error = tk.Label(self.window, text = "Please Enter Asset Name", fg = "red")
            self.name_error.pack()
        elif len(asset_name_var) > 100: # Length Check
            self.name_error = tk.Label(self.window, text = "Name can't be more that 100 Characters", fg = "red")
            self.name_error.pack()
        else:
            name_valid = True
            asset_name_var = asset_name_var.capitalize()
        # Asset Type Validation
        if asset_type_var.strip() == "": # Presence Check
            self.type_error = tk.Label(self.window, text = "Please Enter Asset Type", fg = "red")
            self.type_error.pack()
        elif len(asset_type_var) > 50: # Length Check
            self.type_error = tk.Label(self.window, text = "Name can't be more that 50 Characters", fg = "red")
            self.type_error.pack()
        else:
            type_valid = True
            asset_type_var = asset_type_var.capitalize() 
        # Asset IP Address Validation (Hardware Assets Only)
        if self.asset_type == "Hardware":
            if asset_ip_address_var == "": # Presence Check
                self.ip_address_error = tk.Label(self.window, text = "Please Enter Asset IP Address", fg = "red")
                self.ip_address_error.pack()
            elif len(asset_ip_address_var) < 11:
                self.ip_address_error = tk.Label(self.window, text = "IP Address must be 8 digits minumum", fg = "red")
                self.ip_address_error.pack()
            elif len(asset_ip_address_var) > 16:
                self.ip_address_error = tk.Label(self.window, text = "IP Address must be 12 digits maximum", fg = "red")
                self.ip_address_error.pack()
            elif not asset_ip_address_var1.isdigit() or not asset_ip_address_var2.isdigit() or not asset_ip_address_var3.isdigit() or not asset_ip_address_var4.isdigit():
                self.ip_address_error = tk.Label(self.window, text = "IP Address can only be digits", fg = "red")
                self.ip_address_error.pack()
            else:
                ip_address_valid = True
        # Asset Status Validation
        if asset_status_var == status_options[0]: # Ensures default value can't be submitted
            self.status_error = tk.Label(self.window, text = "Please Select Asset Status", fg = "red")
            self.status_error.pack()
        else:
            status_valid = True
        # Defining Adding to DB function
        def append_to_db(tablename):
            connect = sqlite3.connect(db_file)
            cursor = connect.cursor()
            if tablename in ["furniture_assets", "software_assets"]:
                query = f"INSERT INTO {tablename} (assetName, assetType, assetStatus) VALUES (?, ?, ?)"
                data = (asset_name_var, asset_type_var, asset_status_var)
            else:
                query = f"INSERT INTO {tablename} (assetName, assetType, ipAddress, assetStatus) VALUES (?, ?, ?, ?)"
                data = (asset_name_var, asset_type_var, asset_ip_address_var, asset_status_var)
            cursor.execute(query, data)
            connect.commit()
            connect.close()
        # Checks if all values return true 
        if all ([name_valid, type_valid, ip_address_valid, status_valid]):
            loading_label = tk.Label(self.window, text = "Adding to Database..", fg = "green")
            loading_label.pack()
            if self.asset_type == "Hardware":
                append_to_db("hardware_assets")
            elif self.asset_type == "Software":
                append_to_db("software_assets")
            else:
                append_to_db("furniture_assets")
            self.window.after(3000, loading_label.destroy)
