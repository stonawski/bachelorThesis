import sqlite3

conn = sqlite3.connect('StonawskiDB3.db')  # You can create a new database by changing the name within the quotes
c = conn.cursor()  # The database will be saved in the location where your 'py' file is saved

c.execute('''CREATE TABLE IF NOT EXISTS TYPE
(
ID INTEGER PRIMARY KEY,
RE_TYPE TEXT
)
''')

c.execute('''
INSERT INTO TYPE (RE_TYPE) VALUES
('House/Villa'),
('Flat'),
('Land')        
''')

c.execute('''CREATE TABLE IF NOT EXISTS REAL_ESTATE
(
ID INTEGER PRIMARY KEY,
UNIQUE_RE_NUMBER TEXT,
TYP_ID INT,
FOREIGN KEY (TYP_ID) REFERENCES TYPE (ID)
)
''')

c.execute('''CREATE TABLE IF NOT EXISTS ADDRESS
(
ID INTEGER PRIMARY KEY,
RE_ID INT,
ADDRSS TEXT,
LOCATION TEXT,
FOREIGN KEY (RE_ID) REFERENCES REAL_ESTATE (ID)
)
''')

c.execute('''CREATE TABLE IF NOT EXISTS PRICE
(
ID INTEGER PRIMARY KEY,
RE_ID INT,
RE_PRICE TEXT,
UPDATE_DATE DATE,
FOREIGN KEY (RE_ID) REFERENCES REAL_ESTATE (ID)
)
''')

c.execute('''CREATE TABLE IF NOT EXISTS INFORMATION 
(
ID INTEGER PRIMARY KEY,
RE_ID INT,
RE_INFO TEXT,
FOREIGN KEY (RE_ID) REFERENCES REAL_ESTATE (ID)
)
''')
conn.commit()
