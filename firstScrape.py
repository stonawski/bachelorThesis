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

# First scrape - Houses and Villas
html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-domy_vily.html')
bs = BeautifulSoup(html.read(), 'html.parser')
allPages = bs.find_all(class_='paginator__list-item')

# Page count on the site (eighth element of list is always the last page)
lastPageStr1 = allPages[8].find('a').get_text()
lastPageInt1 = int(lastPageStr1)

# Declaring needed variables
id = 1
housesTypeId = "1"
flatsTypeId = "2"
landsTypeId = "3"

# Scraping through pages
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

        cls = bs2.find(class_='block breadcrumb')
        li = cls.find_all('li')
        pocetLI = 0
        for i in li:
            pocetLI = pocetLI + 1

        lctn = li[pocetLI-1].a.get_text()

        # adding scraped data into arrays

        unique_code = unique_code + [unique_number]
        id_arr = id_arr + [id]
        real_estate = real_estate + [housesTypeId]
        address = address + [item.find(class_='advert-list-items__content-address').get_text()]
        location = location + [lctn]
        re_id = re_id + [id]
        re_date = re_date + [todays_date]
        price = price + [item.find(class_='advert-list-items__content-price-price').get_text()]
        informations = informations + [item.find(class_='advert-list-items__content').h2.a.get_text()]
        id = id + 1

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

        cls = bs2.find(class_='block breadcrumb')
        li = cls.find_all('li')
        pocetLI = 0
        for i in li:
            pocetLI = pocetLI + 1

        lctn = li[pocetLI - 1].a.get_text()

        unique_code = unique_code + [unique_number]
        real_estate = real_estate + [flatsTypeId]
        id_arr = id_arr + [id]
        address = address + [item.find(class_='advert-list-items__content-address').get_text()]
        location = location + [lctn]
        re_id = re_id + [id]
        re_date = re_date + [todays_date]
        price = price + [item.find(class_='advert-list-items__content-price-price').get_text()]
        informations = informations + [item.find(class_='advert-list-items__content').h2.a.get_text()]
        id = id + 1

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

        cls = bs2.find(class_='block breadcrumb')
        li = cls.find_all('li')
        pocetLI = 0
        for i in li:
            pocetLI = pocetLI + 1

        lctn = li[pocetLI - 1].a.get_text()

        unique_code = unique_code + [unique_number]
        id_arr = id_arr + [id]
        real_estate = real_estate + [landsTypeId]
        address = address + [item.find(class_='advert-list-items__content-address').get_text()]
        location = location + [lctn]
        re_id = re_id + [id]
        re_date = re_date + [todays_date]
        price = price + [item.find(class_='advert-list-items__content-price-price').get_text()]
        informations = informations + [item.find(class_='advert-list-items__content').h2.a.get_text()]
        id = id + 1

# Putting data into dataframe

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

# Importing data into database

conn = sqlite3.connect('StonawskiDB3.db')
c = conn.cursor()

RE_frame.to_sql('REAL_ESTATE', conn, if_exists='replace', index=False)
Addrss_frame.to_sql('ADDRESS', conn, if_exists='replace', index=False)
Price_frame.to_sql('PRICE', conn, if_exists='replace', index=False)
Info_frame.to_sql('INFORMATION', conn, if_exists='replace', index=False)

conn.close()