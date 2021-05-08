from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint
from datetime import datetime
import sqlite3

# Date of scraping
todays_date = datetime.now().date()

# Data containers
id_arr = []
real_estate = []
unique_code = []
re_id = []
types = []
address = []
location = []
re_date = []
type = []
price = []
informations = []

priceId_arr = []
update_id = []
update_date = []
update_price = []
priceId = []

# First scrape - Houses and Villas

poloha = []
druh = []
typ = []
uplocha = []

conn = sqlite3.connect('FinalDB.db')
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()
id = 0
priceId = 0
idList = c.execute('SELECT ID FROM REAL_ESTATE').fetchall()
for i in idList:
    id = id + 1
priceIdList = c.execute('SELECT ID FROM PRICE').fetchall()
for i in priceIdList:
    priceId = priceId + 1

print(id)
print(priceId)



html = urlopen('https://reality.idnes.cz/s/domy/olomoucky-kraj/')
bs = BeautifulSoup(html.read(), 'html.parser')
allPages = bs.find_all(class_='paging__item')



# Page count on the site (eighth element of list is always the last page)
lastPageStr1 = allPages[7].find('span').get_text()
lastPageInt1 = int(lastPageStr1)
halfPage = lastPageInt1 / 2

print(lastPageInt1)

# Declaring needed variables
housesTypeId = "1"
flatsTypeId = "2"
landsTypeId = "3"


# Scraping through pages
for page in range(1, lastPageInt1-1):
    if page == 1:
        html = urlopen('https://reality.idnes.cz/s/domy/olomoucky-kraj/')
    else:
        html = urlopen('https://reality.idnes.cz/s/domy/olomoucky-kraj/?page=' + str(page))

    bs = BeautifulSoup(html.read(), 'html.parser')
    allItems = bs.find_all(class_='c-list-products__item')

    sleep(randint(60, 100))

    for item in allItems:
        sleep(randint(10, 20))
        href = 'https://reality.idnes.cz/' + item.a['href']
        html2 = urlopen(href)
        bs2 = BeautifulSoup(html2.read(), 'html.parser')
        details = bs2.find(class_='b-definition-columns')
        table = details.find_all('dd')
        labels = details.find_all('dt')
        labelNumber = 0
        pol = 0
        dr = 0
        ty = 0
        up = 0
        uc = 0
        unique_number = ''
        for label in labels:
            if label.get_text() == 'Číslo zakázky':
                unique_number = table[labelNumber].get_text()
                unique_code = unique_code + [table[labelNumber].get_text()]
                uc = 1
                realityID = c.execute('SELECT ID FROM REAL_ESTATE WHERE UNIQUE_RE_NUMBER = ?',
                                      (unique_number,)).fetchall()
                if not realityID:
                    if labelNumber > 0 and uc == 0:
                        break
                    if label.get_text() == 'Poloha domu':
                        poloha = poloha + [table[labelNumber].get_text()]
                        pol = 1
                    if label.get_text() == 'Konstrukce budovy':
                        druh = druh + [table[labelNumber].get_text()]
                        dr = 1
                    if label.get_text() == 'Počet podlaží':
                        typ = typ + [table[labelNumber].get_text()]
                        ty = 1
                    if label.get_text() == 'Užitná plocha':
                        uplocha = uplocha + [table[labelNumber].get_text()]
                        up = 1
                    labelNumber = labelNumber + 1

                    if pol == 0:
                        poloha = poloha + [' ']
                    if dr == 0:
                        druh = druh + [' ']
                    if ty == 0:
                        typ = typ + [' ']
                    if up == 0:
                        uplocha = uplocha + [' ']

                    id_arr = id_arr + [id]
                    real_estate = real_estate + [housesTypeId]
                    address = address + [item.find(class_='c-list-products__info').get_text()]
                    location = location + [' ']
                    re_id = re_id + [id]
                    re_date = re_date + [todays_date]
                    price = price + [item.find(class_='c-list-products__price').get_text()]
                    informations = informations + [item.find(class_='c-list-products__title').get_text()]
                    id = id + 1
                if realityID:
                    priceId_arr = priceId_arr + [priceId]
                    update_id = update_id + [realityID[0]]
                    update_date = update_date + [todays_date]
                    update_price = update_price + [
                        item.find(class_='advert-list-items__content-price-price').get_text()]
                    priceId = priceId + 1



RE_frame = pd.DataFrame(
    {
        'ID': id_arr,
        'TYP_ID': real_estate,
        'UNIQUE_RE_NUMBER': unique_code
    }
)
Addrss_frame = pd.DataFrame(
    {
        'ID': id_arr,
        'RE_ID': re_id,
        'ADDRSS': address,
        'LOCATION': location
    }
)
Price_frame = pd.DataFrame(
    {
        'ID': id_arr,
        'RE_ID': re_id,
        'RE_PRICE': price,
        'UPDATE_DATE': re_date
    }
)
Info_frame = pd.DataFrame(
    {
        'ID': id_arr,
        'RE_ID': re_id,
        'RE_INFO': informations
    }
)
HouseInf_frame = pd.DataFrame(
    {
        'ID': id_arr,
        'INF_ID': re_id,
        'RE_POLOHA': poloha,
        'RE_DRUH': druh,
        'RE_TYP': typ,
        'RE_UPLOCHA': uplocha
    }
)
Update_Price_frame = pd.DataFrame(
    {
        'ID': priceId_arr,
        'RE_ID': update_id,
        'RE_PRICE': update_price,
        'UPDATE_DATE': update_date
    }
)

# Importing data into database

conn = sqlite3.connect('FinalDB.db')
c = conn.cursor()

RE_frame.to_sql('REAL_ESTATE', conn, if_exists='append', index=False)
Addrss_frame.to_sql('ADDRESS', conn, if_exists='append', index=False)
Price_frame.to_sql('PRICE', conn, if_exists='append', index=False)
Info_frame.to_sql('INFORMATION', conn, if_exists='append', index=False)
HouseInf_frame.to_sql('HOUSEINFO', conn, if_exists='append', index=False)
Update_Price_frame.to_sql('PRICE', conn, if_exists='append', index=False)

conn.close()

