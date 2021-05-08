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

plocha = []
druh = []
site = []
komunikace = []

html = urlopen('https://reality.idnes.cz/s/domy/olomoucky-kraj/')
bs = BeautifulSoup(html.read(), 'html.parser')
allPages = bs.find_all(class_='paging__item')



# Page count on the site (eighth element of list is always the last page)
lastPageStr1 = allPages[7].find('span').get_text()
lastPageInt1 = int(lastPageStr1)
halfPage = lastPageInt1 / 2

print(lastPageInt1)

# Declaring needed variables
conn = sqlite3.connect('IDNES.db')
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()
idList = c.execute('SELECT ID FROM REAL_ESTATE').fetchall()
id = 0
for i in idList:
    id = id + 1

print(id)
housesTypeId = "1"
flatsTypeId = "2"
landsTypeId = "3"


# Scraping through pages
for page in range(1, lastPageInt1-1):
    if page == 1:
        html = urlopen('https://reality.idnes.cz/s/pozemky/olomoucky-kraj/')
    else:
        html = urlopen('https://reality.idnes.cz/s/pozemky/olomoucky-kraj/?page=' + str(page))

    bs = BeautifulSoup(html.read(), 'html.parser')
    allItems = bs.find_all(class_='c-list-products__item')

    sleep(randint(60, 100))

    for item in allItems:
        sleep(randint(20, 30))
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

        for label in labels:
            if label.get_text() == 'Číslo zakázky':
                unique_code = unique_code + [table[labelNumber].get_text()]
                uc = 1
            if labelNumber > 0 and uc == 0:
                break
            if label.get_text() == 'Site':
                site = site + [table[labelNumber].get_text()]
                pol = 1
            if label.get_text() == 'Druh':
                druh = druh + [table[labelNumber].get_text()]
                dr = 1
            if label.get_text() == 'Plocha pozemku':
                plocha = plocha + [table[labelNumber].get_text()]
                up = 1
            if label.get_text() == 'Komunikace':
                komunikace = komunikace + [table[labelNumber].get_text()]
                ty = 1
            labelNumber = labelNumber + 1
        if uc != 0:
            if pol == 0:
                site = site + [' ']
            if dr == 0:
                druh = druh + [' ']
            if up == 0:
                plocha = plocha + [' ']
            if ty == 0:
                 komunikace = komunikace + [' ']

            id_arr = id_arr + [id]
            real_estate = real_estate + [housesTypeId]
            address = address + [item.find(class_='c-list-products__info').get_text()]
            location = location + [' ']
            re_id = re_id + [id]
            re_date = re_date + [todays_date]
            price = price + [item.find(class_='c-list-products__price').get_text()]
            informations = informations + [item.find(class_='c-list-products__title').get_text()]
            id = id + 1



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
LandInf_frame = pd.DataFrame(
    {
        'ID': id_arr,
        'INF_ID': re_id,
        'RE_PLOCHA': plocha,
        'RE_DRUH': druh,
        'RE_SITE': site,
        'RE_KOMUNIKACE': komunikace
    }
)

# Importing data into database

conn = sqlite3.connect('IDNES.db')
c = conn.cursor()

RE_frame.to_sql('REAL_ESTATE', conn, if_exists='replace', index=False)
Addrss_frame.to_sql('ADDRESS', conn, if_exists='replace', index=False)
Price_frame.to_sql('PRICE', conn, if_exists='replace', index=False)
Info_frame.to_sql('INFORMATION', conn, if_exists='replace', index=False)
LandInf_frame.to_sql('LANDINFO', conn, if_exists='replace', index=False)

conn.close()