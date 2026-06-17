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