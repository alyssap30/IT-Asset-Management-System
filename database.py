# database.py
import sqlite3
from config import db_file, sql_file  # Import variables from config

def accessing_sql_db():
    connect = sqlite3.connect(db_file)
    cursor = connect.cursor()
    try:
        with open(sql_file, 'r') as script_file:
            sql_script = script_file.read() 
        cursor.executescript(sql_script)
        connect.commit()
    except sqlite3.Error as e:
        print(f"Database Initialization Error: {e}")
    except FileNotFoundError:
        cursor.execute("CREATE TABLE IF NOT EXISTS hardware_assets (assetName TEXT, assetType TEXT, assetStatus TEXT, ipAddress TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS software_assets (assetName TEXT, assetType TEXT, assetStatus TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS furniture_assets (assetName TEXT, assetType TEXT, assetStatus TEXT)")
        connect.commit()
    finally:
        connect.close()