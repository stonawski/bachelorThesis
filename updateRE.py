from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint
from datetime import datetime
import sqlite3


todays_date = datetime.now().date()
# Arrays for data
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
priceId_arr_new = []
informations = []


id = 1
priceId = 1
housesTypeId = "1"
flatsTypeId = "2"
landsTypeId = "3"

# Scraping data (houses and villas)

poloha = []
druh = []
typ = []
uplocha = []

html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-domy_vily.html')
bs = BeautifulSoup(html.read(), 'html.parser')
allPages = bs.find_all(class_='paginator__list-item')

# osmý prvek listu je vždy poslední stránka

lastPageStr1 = allPages[8].find('a').get_text()
lastPageInt1 = int(lastPageStr1)

conn = sqlite3.connect('FinalDB.db')
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()
unique_numbers = c.execute('SELECT UNIQUE_RE_NUMBER FROM REAL_ESTATE').fetchall()
idList = c.execute('SELECT ID FROM REAL_ESTATE').fetchall()
for i in idList:
    id = id + 1

priceIdList = c.execute('SELECT ID FROM PRICE').fetchall()
for i in priceIdList:
    priceId = priceId + 1

print(id)
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
        if not realityID:
            cls = bs2.find(class_='block breadcrumb')
            li = cls.find_all('li')
            pocetLI = 0
            for i in li:
                pocetLI = pocetLI + 1

            lctn = li[pocetLI - 1].a.get_text()

            inf = bs2.find_all(class_='detail-information__data-item')
            pol = 0
            dr = 0
            ty = 0
            up = 0
            for info in inf:
                span = info.find_all('span')
                if span[0].get_text() == 'Poloha objektu:':
                    poloha = poloha + [span[1].get_text()]
                    pol = 1
                elif span[0].get_text() == 'Druh objektu:':
                    druh = druh + [span[1].get_text()]
                    dr = 1
                elif span[0].get_text() == 'Typ domu:':
                    typ = typ + [span[1].get_text()]
                    ty = 1
                elif span[0].get_text() == 'Užitná plocha:':
                    uplocha = uplocha + [span[1].get_text()]
                    up = 1
            if pol == 0:
                poloha = poloha + [' ']
            if dr == 0:
                druh = druh + [' ']
            if ty == 0:
                typ = typ + [' ']
            if up == 0:
                uplocha = uplocha + [' ']

            unique_code = unique_code + [unique_number]
            id_arr = id_arr + [id]
            real_estate = real_estate + [housesTypeId]
            address = address + [item.find(class_='advert-list-items__content-address').get_text()]
            location = location + [lctn]
            re_id = re_id + [id]
            re_date = re_date + [todays_date]
            price = price + [item.find(class_='advert-list-items__content-price-price').get_text()]
            informations = informations + [item.find(class_='advert-list-items__content').h2.a.get_text()]
            priceId_arr_new = priceId_arr_new + [priceId]
            priceId = priceId + 1
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
        'ID': priceId_arr_new,
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


RE_frame.to_sql('REAL_ESTATE', conn, if_exists='append', index=False)
Addrss_frame.to_sql('ADDRESS', conn, if_exists='append', index=False)
Price_frame.to_sql('PRICE', conn, if_exists='append', index=False)
Info_frame.to_sql('INFORMATION', conn, if_exists='append', index=False)
HouseInf_frame.to_sql('HOUSEINFO', conn, if_exists='append', index=False)

# Second part - scraping flats

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
priceId_arr_new = []
informations = []

dispoziceB = []
druhObjektu = []
podlahovaPl = []

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
        if not realityID:
            cls = bs2.find(class_='block breadcrumb')
            li = cls.find_all('li')
            pocetLI = 0
            for i in li:
                pocetLI = pocetLI + 1

            lctn = li[pocetLI - 1].a.get_text()

            inf = bs2.find_all(class_='detail-information__data-item')
            disb = 0
            dr = 0
            pp = 0

            for info in inf:
                span = info.find_all('span')
                if span[0].get_text() == 'Dispozice bytu:':
                    dispoziceB = dispoziceB + [span[1].get_text()]
                    disb = 1
                elif span[0].get_text() == 'Celková podlahová plocha:':
                    podlahovaPl = podlahovaPl + [span[1].get_text()]
                    pp = 1
                elif span[0].get_text() == 'Druh objektu:':
                    druhObjektu = druhObjektu + [span[1].get_text()]
                    dr = 1

            if disb == 0:
                dispoziceB = dispoziceB + [' ']
            if dr == 0:
                podlahovaPl = podlahovaPl + [' ']
            if pp == 0:
                druhObjektu = druhObjektu + [' ']

            unique_code = unique_code + [unique_number]
            id_arr = id_arr + [id]
            real_estate = real_estate + [flatsTypeId]
            address = address + [item.find(class_='advert-list-items__content-address').get_text()]
            location = location + [lctn]
            re_id = re_id + [id]
            re_date = re_date + [todays_date]
            price = price + [item.find(class_='advert-list-items__content-price-price').get_text()]
            informations = informations + [item.find(class_='advert-list-items__content').h2.a.get_text()]
            priceId_arr_new = priceId_arr_new + [priceId]
            priceId = priceId + 1
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
FlatInf_frame = pd.DataFrame(
    {
        'ID': id_arr,
        'INF_ID': re_id,
        'RE_DISPOZICE': dispoziceB,
        'RE_DRUH': druhObjektu,
        'RE_PPLOCHA': podlahovaPl
    }
)

RE_frame.to_sql('REAL_ESTATE', conn, if_exists='append', index=False)
Addrss_frame.to_sql('ADDRESS', conn, if_exists='append', index=False)
Price_frame.to_sql('PRICE', conn, if_exists='append', index=False)
Info_frame.to_sql('INFORMATION', conn, if_exists='append', index=False)
FlatInf_frame.to_sql('FLATINFO', conn, if_exists='append', index=False)

# Last part - scraping lands

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
        if not realityID:
            cls = bs2.find(class_='block breadcrumb')
            li = cls.find_all('li')
            pocetLI = 0
            for i in li:
                pocetLI = pocetLI + 1

            lctn = li[pocetLI - 1].a.get_text()

            inf = bs2.find_all(class_='detail-information__data-item')
            pl = 0
            dr = 0
            st = 0
            kom = 0

            for info in inf:
                span = info.find_all('span')
                if span[0].get_text() == 'Celková plocha:':
                    plocha = plocha + [span[1].get_text()]
                    pl = 1
                elif span[0].get_text() == 'Druh pozemku:':
                    druh = druh + [span[1].get_text()]
                    dr = 1
                elif span[0].get_text() == 'Inženýrské sítě:':
                    site = site + [span[1].get_text()]
                    st = 1
                elif span[0].get_text() == 'Komunikace:':
                    komunikace = komunikace + [span[1].get_text()]
                    kom = 1

            if pl == 0:
                plocha = plocha + [' ']
            if dr == 0:
                druh = druh + [' ']
            if st == 0:
                site = site + [' ']
            if kom == 0:
                komunikace = komunikace + [' ']

            unique_code = unique_code + [unique_number]
            id_arr = id_arr + [id]
            real_estate = real_estate + [landsTypeId]
            address = address + [item.find(class_='advert-list-items__content-address').get_text()]
            location = location + [lctn]
            re_id = re_id + [id]
            re_date = re_date + [todays_date]
            price = price + [item.find(class_='advert-list-items__content-price-price').get_text()]
            informations = informations + [item.find(class_='advert-list-items__content').h2.a.get_text()]
            priceId_arr_new = priceId_arr_new + [priceId]
            priceId = priceId + 1
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
        'ID': priceId_arr_new,
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

RE_frame.to_sql('REAL_ESTATE', conn, if_exists='append', index=False)
Addrss_frame.to_sql('ADDRESS', conn, if_exists='append', index=False)
Price_frame.to_sql('PRICE', conn, if_exists='append', index=False)
Info_frame.to_sql('INFORMATION', conn, if_exists='append', index=False)
LandInf_frame.to_sql('LANDINFO', conn, if_exists='append', index=False)
conn.close()