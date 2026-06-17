import os

# Comboboxes Values
types_of_assets = ["--Please Select A Type of Asset--", "Hardware", "Software", "Office Furniture"]
status_options = ["--Please Select A Status--", "Active", "Under Maintence", "Temporary Deactivated", "Inactive"]
database_filters = ["--Please Select A Filter--", "Date", "Status", "Type"]
month_options = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Database Variables 
script_dir = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(script_dir, "asset_inventory.db")
sql_file = os.path.join(script_dir, "database_inventory.sql")
type_of_asset_conversion = {
            "Hardware": "hardware_assets",
            "Software": "software_assets",
            "Office Furniture": "furniture_assets"}
columns_hardware = ['assetName', 'assetType', 'ipAdress', 'assetStatus', 'assetRenewalDate']
columns_software_and_furniture = ['assetName', 'assetType', 'assetStatus', 'assetRenewalDate']
# Database Values storage for data manipulation
hardware_asset_names = []
software_asset_names = []
furniture_asset_names = []

#Python Projects /IT Asset System/
