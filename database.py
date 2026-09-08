# database.py imports 
import sqlite3
from config import db_file, sql_file  # Import variables from config
from tkinter import messagebox

def accessing_sql_db():
    connect = sqlite3.connect(db_file)
    cursor = connect.cursor()
    try:
        with open(sql_file, 'r') as script_file:
            sql_script = script_file.read() 
        cursor.executescript(sql_script)
        connect.commit()
    except (sqlite3.Error, FileNotFoundError, sqlite3.OperationalError) as e:
        print(f"Database Initialization Error: {e}")
        cursor.execute("CREATE TABLE IF NOT EXISTS hardware_assets (assetName TEXT, assetType TEXT, assetStatus TEXT, ipAddress TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS software_assets (assetName TEXT, assetType TEXT, assetStatus TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS furniture_assets (assetName TEXT, assetType TEXT, assetStatus TEXT)")
        connect.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Duplicate Asset", "The asset name must be unique")
    finally:
        connect.close()

def query_execution(query):
    connect = sqlite3.connect(db_file)
    cursor = connect.cursor()
    cursor.execute(query)
    connect.commit()
    connect.close()