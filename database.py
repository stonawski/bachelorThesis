import sqlite3

conn = sqlite3.connect('Database.db')  # You can create a new database by changing the name within the quotes
c = conn.cursor()  # The database will be saved in the location where your 'py' file is saved

# Create table - CLIENTS
c.execute('''CREATE TABLE HOUSES_AND_VILLAS
             ([index] INTEGER PRIMARY KEY,[HouseInfo] text, [HouseAddress] text, [HousePrice] text)''')
c.execute('''CREATE TABLE FLATS
             ([index] INTEGER PRIMARY KEY,[FlatInfo] text, [FlatAddress] text, [FlatPrice] text)''')
c.execute('''CREATE TABLE LANDS
             ([index] INTEGER PRIMARY KEY,[LandInfo] text, [LandAddress] text, [LandPrice] text)''')

conn.commit()
