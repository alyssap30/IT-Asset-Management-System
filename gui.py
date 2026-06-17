import tkinter as tk
from tkinter import ttk
import sqlite3
# Import choices and database variables
from config import types_of_assets, status_options, database_filters, month_options, db_file, hardware_asset_names, software_asset_names, furniture_asset_names, type_of_asset_conversion, columns_hardware, columns_software_and_furniture
from database import query_execution

# Database display Class Declaration
class DeleteUpdateGUI:
    def __init__(self, window, delete_or_update, db_name):
        self.window = window
        self.delete_or_update = delete_or_update
        self.db_name = db_name
        self.window.title("Asset Inventory Database")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.window, text = f"{self.delete_or_update} A Row from {self.db_name} Table", bg = "#5285A1", fg = "white", width= 100, font = ("Arial", 20)).pack(pady= 3)
        tk.Label(self.window, text = f"Please Select a row to {self.delete_or_update.lower()}").pack()
        if self.db_name == "Hardware":
            self.table_row_inp = ttk.Combobox(self.window, values = hardware_asset_names)
        elif self.db_name == "Software":
            self.table_row_inp = ttk.Combobox(self.window, values = software_asset_names)
        elif self.db_name == "Office Furniture":
            self.table_row_inp = ttk.Combobox(self.window, values = furniture_asset_names)   
        self.table_row_inp.pack()
        self.submit_button = tk.Button(self.window, text = "Submit", command=self.manipulating_data)
        self.submit_button.pack()
    
    def manipulating_data(self):
        self.row_name = self.table_row_inp.get()
        if self.delete_or_update == "Delete":
            query_execution(f"DELETE FROM {type_of_asset_conversion[self.db_name]} WHERE assetName = '{self.row_name}'")
            tk.Label(self.window, text =f"Deleted row '{self.row_name}'", fg= 'green').pack()
        elif self.delete_or_update == "Update":
            self.submit_button.destroy()
            tk.Label(self.window, text = "Choose a column to update:").pack()
            if self.db_name == 'Hardware':
                self.column_inp = ttk.Combobox(self.window, values= columns_hardware, state='readonly')
            elif self.db_name in ['Software', 'Office Furniture']:
                self.column_inp = ttk.Combobox(self.window, values= columns_software_and_furniture, state='readonly')
            self.column_inp.set(columns_hardware[0])
            self.column_inp.pack()
            tk.Label(self.window, text='Input new value below').pack()
            self.new_value_inp = tk.Entry(self.window)
            self.new_value_inp.pack()
            tk.Button(self.window, text = f"Update {self.row_name}", command=self.updating_record).pack()
        
    def updating_record(self):
        if hasattr(self, 'column_error_label'):
            self.column_error_label.destroy()
        if self.column_inp.get() == columns_hardware[0]:
            self.column_error_label = tk.Label(self.window, text = "Please select a column to update", fg = "red") 
            self.column_error_label.pack()
            return
        query_execution(f"UPDATE {type_of_asset_conversion[self.db_name]} SET {self.column_inp.get()} = '{self.new_value_inp.get()}' WHERE assetName = '{self.row_name}'")
        tk.Label(self.window, text =f"Updateed row '{self.row_name}'", fg= 'green').pack()
class DatabaseGUI:
    def __init__(self, window, database_type, filter):
        self.window = window
        self.database_type = database_type
        self.filter = filter
        self.window.title("Asset Inventory Database")
        self.window.geometry("1000x300")
        self.window.resizable(False, False)
        self.create_widgets()
        self.data_fetching_from_db()
    
    def create_widgets(self):
        tk.Label(self.window, text = f"Full {self.database_type} Asset Inventory", bg = "#5285A1", fg = "white", width= 100, font = ("Arial", 20)).pack(pady= 3)
        table_columns = ['Name', 'Type', 'Status', 'Renewal Date']
        table_columns.append('IP Address') if self.database_type == 'Hardware' else None
        # Initialising Table + Headings
        self.table = ttk.Treeview(self.window, columns=table_columns, show='headings')
        self.table.heading("Name", text= 'Asset Name')
        self.table.heading("Type", text= 'Asset Type')
        self.table.heading("Status", text='Asset Status')
        self.table.heading("Renewal Date", text='Renewal Date')
        self.table.heading("IP Address", text='IP Address') if self.database_type == 'Hardware' else None
        self.table.pack()
    
    def data_fetching_from_db(self):
        connect = sqlite3.connect(db_file)
        cursor = connect.cursor()
        table_name = type_of_asset_conversion[self.database_type]
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            self.table.insert('', 'end', values=row)
            if table_name == "hardware_assets":
                if row[0] not in hardware_asset_names:
                    hardware_asset_names.append(row[0])
            elif table_name == "software_assets":
                if row[0] not in software_asset_names:
                    software_asset_names.append(row[0])
            elif table_name == "furniture_assets":
                if row[0] not in furniture_asset_names:
                    furniture_asset_names.append(row[0])
        connect.close()

# Database Window Class Declaration
class ViewDataBaseGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Asset Database Selection")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text = "IT Asset Management System Database", bg = "#5285A1", fg = "white", width= 100, font = ("Arial", 20)).pack(pady= 3)
        tk.Label(self.window, text = f"View Full Database", bg = "#6DA9C9", fg = "white", width= 100, font = ("Arial", 17)).pack()
        # User Selection for which Database they would like to view 
        tk.Label(self.window, text = "Database Name:").pack()
        self.type_of_asset_inp = ttk.Combobox(self.window, values = types_of_assets, width= 25, state= 'readonly')
        self.type_of_asset_inp.set(types_of_assets[0])
        self.type_of_asset_inp.pack()
        # Opens a new window to display full database bases on user interation
        tk.Button(self.window, text = "View Database", command=self.view_unfiltered_db).pack()
        
        # Users can filter their results rather than setting the full database
        tk.Label(self.window, text = f"View Filtered Database", bg = "#6DA9C9", fg = "white", width= 100, font = ("Arial", 17)).pack()
        tk.Label(self.window, text = "Filter By").pack()
        self.filter_inp = ttk.Combobox(self.window, values=database_filters, state = 'readonly')
        self.filter_inp.set(database_filters[0])
        self.filter_inp.pack()
        tk.Button(self.window, text = "Submit", command=self.expanded_filter_handing).pack()

        # Users Can delete or update a record
        tk.Label(self.window, text = f"Delete or Update a record", bg = "#6DA9C9", fg = "white", width= 100, font = ("Arial", 17)).pack()
        tk.Label(self.window, text = "Database Name").pack()
        self.type_of_asset_inp2 = ttk.Combobox(self.window, values = types_of_assets, width= 25, state= 'readonly')
        self.type_of_asset_inp2.set(types_of_assets[0])
        self.type_of_asset_inp2.pack()
        # User chooses how the data will be manipulated
        tk.Label(self.window, text = "Delete or Update a record").pack()
        self.delete_or_update_inp = ttk.Combobox(self.window, values = ['--Please Select an Option--', "Delete", "Update"], width= 25, state= 'readonly')
        self.delete_or_update_inp.set('--Please Select an Option--')
        self.delete_or_update_inp.pack()
        tk.Button(self.window, text="Submit", command=self.delete_or_update).pack()

    def label_stacking_prevention(self):
        if hasattr(self, 'type_of_asset_error_label'):
            self.type_of_asset_error_label.destroy()
        if hasattr(self, 'type_of_asset_error_label2'):
            self.type_of_asset_error_label2.destroy()
        if hasattr(self, 'data_manipulation_error_label'):
            self.data_manipulation_error_label.destroy()
        if hasattr(self, 'filter_error_label'):
            self.filter_error_label.destroy()
        if hasattr (self, 'expanded_filter_frame'):
            self.expanded_filter_frame.destroy()
        
    def view_unfiltered_db(self):
        self.label_stacking_prevention()
        # Checks if the combobox value is it's default value
        if self.type_of_asset_inp.get() == types_of_assets[0]:
            self.type_of_asset_error_label = tk.Label(self.window, text="Please select a type of asset", fg="red")
            self.type_of_asset_error_label.pack()
        # If it isn't the Adding an Asset Window is opened
        else:
            new_window = tk.Toplevel(self.window)
            DatabaseGUI(new_window, self.type_of_asset_inp.get(), "N/A")

    def expanded_filter_handing(self):
        self.label_stacking_prevention()
        self.expanded_filter_frame = tk.Frame(self.window)
        self.expanded_filter_frame.pack()
        tk.Label(self.expanded_filter_frame, text = f"Expanded Filter", bg = "#6DA9C9", fg = "white", width= 100, font = ("Arial", 17)).pack()
        tk.Label(self.expanded_filter_frame, text = "Expanded Filter Selection:").pack()
        
        if self.filter_inp.get() == database_filters[0]:
            self.filter_error_label = tk.Label(self.expanded_filter_frame, text = "Please select a filter", fg = 'red')
            self.filter_error_label.pack()
        if self.filter_inp.get() == "Date":
            self.subfilter_inp = ttk.Combobox(self.expanded_filter_frame, values = ["--Please select a filter--", 'Calculate days until renewal', 'Renewal in next 3 months', 'Renewal in next year', 'Renewal in new 5 years'], state= 'readonly')
            self.subfilter_inp.pack()
        elif self.filter_inp.get() == "Status":
            self.subfilter_inp = ttk.Combobox(self.expanded_filter_frame, values = ["--Please Select A Filter--", "Active", "Under Maintence", "Temporary Deactivated", "Inactive"], state= 'readonly')
            self.subfilter_inp.pack()
        elif self.filter_inp.get() == "Type":
            self.subfilter_inp = ttk.Combobox(self.expanded_filter_frame, values = ['--Please Select a Filter--', hardware_asset_names, software_asset_names, furniture_asset_names], state= 'readonly')
            self.subfilter_inp.pack()
        self.subfilter_inp.set("--Please select a filter--")

    def delete_or_update(self):
        self.label_stacking_prevention()
        # Checks if the combobox value is it's default value
        if self.type_of_asset_inp2.get() == types_of_assets[0]:
            self.type_of_asset_error_label2 = tk.Label(self.window, text="Please select an type of asset", fg="red")
            self.type_of_asset_error_label2.pack()
        if self.delete_or_update_inp.get() == '--Please Select an Option--':
            self.data_manipulation_error_label = tk.Label(self.window, text="Please select an option", fg="red")
            self.data_manipulation_error_label.pack()
            # If it isn't the Adding an Asset Window is opened
        if not self.delete_or_update_inp.get() == '--Please Select an Option--' and self.type_of_asset_inp2.get() != types_of_assets[0]:
            new_window = tk.Toplevel(self.window)
            DeleteUpdateGUI(new_window, self.delete_or_update_inp.get(), self.type_of_asset_inp2.get())
            
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
            elif len(asset_ip_address_var) < 12:
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