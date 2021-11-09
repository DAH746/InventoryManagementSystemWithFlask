import sqlite3

conn = sqlite3.connect("InventoryDatabase.db")
print("Opened database successfully")

conn.execute('CREATE TABLE Inventory (prod_ID TEXT, prod_name TEXT, desc TEXT, quantity TEXT, auth TEXT, pic_id TEXT)')
print("Table created successfully")
conn.close()