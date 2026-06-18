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
            self.table_row_inp = ttk.Combobox(self.window, values = hardware_asset_names, state= 'readonly')
        elif self.db_name == "Software":
            self.table_row_inp = ttk.Combobox(self.window, values = software_asset_names, state= 'readonly')
        elif self.db_name == "Office Furniture":
            self.table_row_inp = ttk.Combobox(self.window, values = furniture_asset_names, state= 'readonly') 
        self.table_row_inp.set(hardware_asset_names[0]) 
        self.table_row_inp.pack()
        
        if self.delete_or_update == "Update":
            tk.Label(self.window, text = "Choose a column to update:").pack()
            if self.db_name == 'Hardware':
                self.column_inp = ttk.Combobox(self.window, values= columns_hardware, state='readonly')
            elif self.db_name in ['Software', 'Office Furniture']:
                self.column_inp = ttk.Combobox(self.window, values= columns_software_and_furniture, state='readonly')
            self.column_inp.set(columns_hardware[0])
            self.column_inp.pack() 
        self.submit_button = tk.Button(self.window, text = "Submit", command=self.manipulating_data)
        self.submit_button.pack()

    def prevent_error_stacking(self):
        if hasattr(self, 'column_error_label'):
            self.column_error_label.destroy()
        if hasattr(self, 'new_value_error'):
            self.new_value_error.destroy()
        if hasattr(self, 'row_error_label'):
            self.row_error_label.destroy()
        
    def manipulating_data(self):
        self.prevent_error_stacking()
        self.row_name = self.table_row_inp.get()
        self.column_var = self.column_inp.get()

        if self.row_name == hardware_asset_names[0]:
            self.row_error_label = tk.Label(self.window, text = f"Please select a row to {self.delete_or_update.lower()}")
            self.row_error_label.pack()
        else:
            # Deletes selected row from SQL Database
            if self.delete_or_update == "Delete":
                query_execution(f"DELETE FROM {type_of_asset_conversion[self.db_name]} WHERE assetName = '{self.row_name}'")
                # Removes select row from asset name lists
                if self.db_name == 'Hardware':
                    hardware_asset_names.remove(self.row_name)
                elif self.db_name == 'Software':
                    software_asset_names.remove(self.row_name)
                elif self.db_name == 'Office Furniture':
                    furniture_asset_names.remove(self.row_name)
                # Comfirm Deletion was successful to users 
                tk.Label(self.window, text =f"Deleted row '{self.row_name}' Successfully", fg= 'green').pack()
            
            # Updating a Row Commands
            elif self.delete_or_update == "Update":
                # Ensures default value isn't selected 
                if self.column_var == columns_hardware[0]:
                    self.column_error_label = tk.Label(self.window, text = 'Please select a column name', fg = 'red')
                    self.column_error_label.pack()
                    return
                tk.Label(self.window, text=f'Input new {self.column_var} below').pack()
                # Displays IP address fields for new value input
                if self.column_var == 'ipAddress':
                    self.ip_frame = tk.Frame(self.window)
                    self.ip_frame.pack()
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
                # Displays status field for new value input
                elif self.column_var == 'assetStatus':
                    self.status_input = ttk.Combobox(self.window, values = status_options, state = "readonly")
                    self.status_input.set(status_options[0])
                    self.status_input.pack()
                # Displays Renewal date fields for new value input
                elif self.column_var == 'assetRenewalDate':
                    self.date_frame = tk.Frame(self.window)
                    self.date_frame.pack()
                    # Day selection Field
                    self.renewal_day_inp = tk.Spinbox(self.date_frame, width= 3, from_=1, to=31, state='readonly')
                    self.renewal_day_inp.pack(side = tk.LEFT, padx = 5)
                    # Month Selection Field
                    tk.Label(self.date_frame, text = "/").pack(side= tk.LEFT, padx=5)
                    self.renewal_month_inp = ttk.Combobox(self.date_frame, width= 9, values = month_options, state='readonly')
                    self.renewal_month_inp.pack(side = tk.LEFT, padx = 5)
                    # Year Selection Field
                    tk.Label(self.date_frame, text = "/").pack(side= tk.LEFT, padx=5)
                    self.renewal_year_inp = tk.Spinbox(self.date_frame, width= 4, from_=2026, to=2100, state='readonly')
                    self.renewal_year_inp.pack(side = tk.LEFT, padx = 5)
                tk.Button(self.window, text = f"Update {self.table_row_inp.get()} {self.row_name}", command=self.updating_record).pack()
            self.submit_button.destroy()
            self.column_inp.pack_forget()

    def updating_record(self):
        self.prevent_error_stacking()
        # Combines the inputted values for IP address into a formatted string
        asset_ip_address_var1 = self.ip_address_inp1.get().strip() if self.db_name == "Hardware" else "N/A"
        asset_ip_address_var2 = self.ip_address_inp2.get().strip() if self.db_name == "Hardware" else "N/A"
        asset_ip_address_var3 = self.ip_address_inp3.get().strip() if self.db_name == "Hardware" else "N/A"
        asset_ip_address_var4 = self.ip_address_inp4.get().strip() if self.db_name == "Hardware" else "N/A"
        asset_ip_address_var = f'{asset_ip_address_var1}.{asset_ip_address_var2}.{asset_ip_address_var3}.{asset_ip_address_var4}'
        asset_renewal_date = f"{self.renewal_day_inp.get()}/{self.renewal_month_inp.get()}/{self.renewal_year_inp.get()}"
        # Asset IP Address Validation (Hardware Assets Only)
        if self.column_inp == "ipAddress":
            if asset_ip_address_var == "": # Presence Check
                self.new_value_error = tk.Label(self.window, text = "Please Enter Asset IP Address", fg = "red")
                self.new_value_error.pack()
            elif len(asset_ip_address_var) < 11: # Length Check
                self.new_value_error = tk.Label(self.window, text = "IP Address must be 8 digits minumum", fg = "red")
                self.new_value_error.pack()
            elif len(asset_ip_address_var) > 16: # Length Check
                self.new_value_error = tk.Label(self.window, text = "IP Address must be 12 digits maximum", fg = "red")
                self.new_value_error.pack()
            elif not asset_ip_address_var1.isdigit() or not asset_ip_address_var2.isdigit() or not asset_ip_address_var3.isdigit() or not asset_ip_address_var4.isdigit():
                self.new_value_error =  tk.Label(self.window, text = "IP Address can only be digits", fg = "red")
                self.new_value_error.pack()
            else:
                self.new_value == asset_ip_address_var
        # Asset Status Validation
        elif self.column_inp == "assetStatus":
            if self.status_input.get() == status_options[0]: # Ensures default value can't be submitted
                self.new_value_error = tk.Label(self.window, text = "Please Select Asset Status", fg = "red")
                self.new_value_error.pack()
        # Asset Renewal Date Validation
        elif self.column_inp == "assetRenewalDate":
            # Asset Renewal Date Validation
            self.renewal_date_error = tk.Label(self.window, text = "Error: Invalid Date")
            if self.renewal_month_inp == "February":
                if self.renewal_year_inp % 4 != 0:
                    if self.renewal_day_inp <= '29':
                        self.renewal_date_error.pack()
                else:
                    if self.renewal_day_inp <= '30':
                        self.renewal_date_error.pack()
            elif self.renewal_month_inp in ['April', 'June', 'September', 'November']:
                if self.renewal_day_inp == '31':
                        self.renewal_date_error.pack()
            self.new_value = asset_renewal_date

        if self.column_inp.get() == columns_hardware[0]:
            self.column_error_label = tk.Label(self.window, text = "Please select a column to update", fg = "red") 
            self.column_error_label.pack()
            return
        query_execution(f"UPDATE {type_of_asset_conversion[self.db_name]} SET {self.column_var} = '{self.new_value}' WHERE assetName = '{self.row_name}'")
        tk.Label(self.window, text =f"Updated row '{self.row_name}'", fg= 'green').pack()
    
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
        self.window.geometry("400x350")
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

    def label_stacking_prevention(self):
        if hasattr(self, 'type_of_asset_error_label'):
            self.type_of_asset_error_label.destroy()
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
            self.subfilter_inp = ttk.Combobox(self.expanded_filter_frame, values = ["--Please Select a filter--", 'Calculate days until renewal', 'Renewal in next 3 months', 'Renewal in next year', 'Renewal in new 5 years'], state= 'readonly')
            self.subfilter_inp.pack()
        elif self.filter_inp.get() == "Status":
            self.subfilter_inp = ttk.Combobox(self.expanded_filter_frame, values = ["--Please Select A Filter--", "Active", "Under Maintence", "Temporary Deactivated", "Inactive"], state= 'readonly')
            self.subfilter_inp.pack()
        elif self.filter_inp.get() == "Type":
            self.subfilter_inp = ttk.Combobox(self.expanded_filter_frame, values = ['--Please Select a Filter--', hardware_asset_names, software_asset_names, furniture_asset_names], state= 'readonly')
            self.subfilter_inp.pack()
        self.subfilter_inp.set("--Please select a filter--")