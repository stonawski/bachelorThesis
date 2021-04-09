import pandas as pd
import sqlite3

conn = sqlite3.connect("FinalDB.db")
# TableRE = pd.read_sql_query("select * from REAL_ESTATE;", conn)
# TableADD = pd.read_sql_query("select * from ADDRESS;", conn)
# TablePR = pd.read_sql_query("select * from PRICE;", conn)

df = pd.read_sql_query(
    "SELECT REAL_ESTATE.UNIQUE_RE_NUMBER, ADDRESS.ADDRSS, ADDRESS.LOCATION, PRICE.RE_PRICE, INFORMATION.RE_INFO FROM REAL_ESTATE INNER JOIN ADDRESS, PRICE, INFORMATION ON REAL_ESTATE.TYP_ID=1 AND REAL_ESTATE.ID=ADDRESS.RE_ID AND REAL_ESTATE.ID=PRICE.RE_ID AND REAL_ESTATE.ID=INFORMATION.RE_ID", conn)


for i in range(len(df)):
    print(df.UNIQUE_RE_NUMBER[i])
    print(df.ADDRSS[i])
    print(df.LOCATION[i])
    print(df.RE_PRICE[i])