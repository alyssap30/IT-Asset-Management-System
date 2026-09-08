# config Imports
import os

# Comboboxes Values
types_of_assets = ["--Please Select A Type of Asset--", "Hardware", "Software", "Office Furniture"]
status_options = ["--Please Select A Status--", "Active", "Under Maintence", "Temporary Deactivated", "Inactive"]
database_filters = ["--Please Select a Filter--", "assetStatus"]
month_options = {"January": 1, "February": 2, "March": 3, "April" : 4, "May": 5, "June": 6, "July": 7, "August": 8, 
                 "September": 9, "October": 10, "November": 11, "December": 12}
columns_hardware = ['--Please select a column name--', 'ipAddress', 'assetStatus', 'assetRenewalDate']
columns_software_and_furniture = ['--Please select a column name--', 'assetStatus', 'assetRenewalDate']

# Database Variables 
script_dir = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(script_dir, "asset_inventory.db")
sql_file = os.path.join(script_dir, "database_inventory.sql")
type_of_asset_conversion = {"Hardware": "hardware_assets", "Software": "software_assets", "Office Furniture": "furniture_assets"}

# Database Values storage for data manipulation
hardware_asset_names = ['--Please Select a Row Name--', 'Server0']
software_asset_names = ['--Please Select a Row Name--', 'VS Code']
furniture_asset_names = ['--Please Select a Row Name--']