from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint
from datetime import datetime
import sqlite3

todays_date = datetime.now().date()
# Arrays for data

priceId_arr = []
update_id = []
update_price = []
update_date = []

id = 1
priceId = 1
housesTypeId = "1"
flatsTypeId = "2"
landsTypeId = "3"

# Scraping data (houses and villas)

html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-domy_vily.html')
bs = BeautifulSoup(html.read(), 'html.parser')
allPages = bs.find_all(class_='paginator__list-item')

# osmý prvek listu je vždy poslední stránka

lastPageStr1 = allPages[8].find('a').get_text()
lastPageInt1 = int(lastPageStr1)

conn = sqlite3.connect('StonawskiDB3.db')
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()
unique_numbers = c.execute('SELECT UNIQUE_RE_NUMBER FROM REAL_ESTATE').fetchall()

priceIdList = c.execute('SELECT ID FROM PRICE').fetchall()
for i in priceIdList:
    priceId = priceId + 1

print(priceId)

for page in range(1, lastPageInt1):
    if page == 1:
        html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-domy_vily.html')
    else:
        html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-domy_vily.html?stranka=' + str(page))

    bs = BeautifulSoup(html.read(), 'html.parser')
    allItems = bs.find_all(class_='advert-list-items__item')

    sleep(randint(2, 10))

    for item in allItems:
        href = item.a['href']

        html2 = urlopen(href)
        bs2 = BeautifulSoup(html2.read(), 'html.parser')
        unique = bs2.find(class_='advert-description__short-props')

        table = unique.find_all('td')
        pocetTD = 0
        for i in table:
            pocetTD = pocetTD + 1

        unique_number = table[pocetTD - 1].get_text()
        realityID = c.execute('SELECT ID FROM REAL_ESTATE WHERE UNIQUE_RE_NUMBER = ?', (unique_number,)).fetchall()
        if realityID:
            priceId_arr = priceId_arr + [priceId]
            update_id = update_id +[realityID[0]]
            update_date = update_date + [todays_date]
            update_price = update_price + [item.find(class_='advert-list-items__content-price-price').get_text()]
            priceId = priceId + 1

# Second part - scraping flats
html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-bytu.html')
bs = BeautifulSoup(html.read(), 'html.parser')
allPages = bs.find_all(class_='paginator__list-item')

lastPageStr1 = allPages[8].find('a').get_text()
lastPageInt1 = int(lastPageStr1)

for page in range(1, lastPageInt1):
    if page == 1:
        html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-bytu.html')
    else:
        html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-bytu.html?stranka=' + str(page))

    bs = BeautifulSoup(html.read(), 'html.parser')
    allItems = bs.find_all(class_='advert-list-items__item')

    sleep(randint(2, 10))

    for item in allItems:
        href = item.a['href']

        html2 = urlopen(href)
        bs2 = BeautifulSoup(html2.read(), 'html.parser')
        unique = bs2.find(class_='advert-description__short-props')

        table = unique.find_all('td')
        pocetTD = 0
        for i in table:
            pocetTD = pocetTD + 1

        unique_number = table[pocetTD - 1].get_text()
        realityID = c.execute('SELECT ID FROM REAL_ESTATE WHERE UNIQUE_RE_NUMBER = ?', (unique_number,)).fetchall()
        if realityID:
            priceId_arr = priceId_arr + [priceId]
            update_id = update_id + [realityID[0]]
            update_date = update_date + [todays_date]
            update_price = update_price + [item.find(class_='advert-list-items__content-price-price').get_text()]
            priceId = priceId + 1

# Last part - scraping lands
html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-pozemky.html')
bs = BeautifulSoup(html.read(), 'html.parser')
allPages = bs.find_all(class_='paginator__list-item')

lastPageStr1 = allPages[8].find('a').get_text()
lastPageInt1 = int(lastPageStr1)

for page in range(1, lastPageInt1):
    if page == 1:
        html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-pozemky.html')
    else:
        html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-pozemky.html?stranka=' + str(page))

    bs = BeautifulSoup(html.read(), 'html.parser')
    allItems = bs.find_all(class_='advert-list-items__item')

    sleep(randint(2, 10))

    for item in allItems:
        href = item.a['href']

        html2 = urlopen(href)
        bs2 = BeautifulSoup(html2.read(), 'html.parser')
        unique = bs2.find(class_='advert-description__short-props')

        table = unique.find_all('td')
        pocetTD = 0
        for i in table:
            pocetTD = pocetTD + 1

        unique_number = table[pocetTD - 1].get_text()
        realityID = c.execute('SELECT ID FROM REAL_ESTATE WHERE UNIQUE_RE_NUMBER = ?', (unique_number,)).fetchall()
        if realityID:
            priceId_arr = priceId_arr + [priceId]
            update_id = update_id +[realityID[0]]
            update_date = update_date + [todays_date]
            update_price = update_price + [item.find(class_='advert-list-items__content-price-price').get_text()]
            priceId = priceId + 1


Update_Price_frame = pd.DataFrame(
    {
        'ID': priceId_arr,
        'RE_ID': update_id,
        'RE_PRICE': update_price,
        'UPDATE_DATE': update_date
    }
)

Update_Price_frame.to_sql('PRICE', conn, if_exists='append', index=False)
conn.close()
