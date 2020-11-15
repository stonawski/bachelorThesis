from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint
import sqlite3

# Arrays for data
house_info = []
house_address = []
house_price = []

# Scraping data (houses and villas)
for page in range(1, 17):
    if page == 1:
        html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-domy_vily.html')
    else:
        html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-domy_vily.html?stranka=' + str(page))

    bs = BeautifulSoup(html.read(), 'html.parser')
    allItems = bs.find_all(class_='advert-list-items__item')

    sleep(randint(2, 10))

    house_info = house_info + [item.find(class_='advert-list-items__content').h2.a.get_text() for item in allItems]
    house_address = house_address + [item.find(class_='advert-list-items__content-address').get_text() for item in allItems]
    house_price = house_price + [item.find(class_='advert-list-items__content-price-price').get_text() for item in allItems]

# Putting data into dataframe
Houses = pd.DataFrame(
    {
        'HouseInfo': house_info,
        'HouseAddress': house_address,
        'HousePrice': house_price
    })

# Arrays for data
flat_info = []
flat_address = []
flat_price = []

# Scraping data (flats)
for page in range(1, 17):
    if page == 1:
        html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-bytu.html')
    else:
        html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-bytu.html?stranka=' + str(page))

    bs = BeautifulSoup(html.read(), 'html.parser')
    allItems = bs.find_all(class_='advert-list-items__item')

    sleep(randint(2, 10))

    flat_info = flat_info + [item.find(class_='advert-list-items__content').h2.a.get_text() for item in allItems]
    flat_address = flat_address + [item.find(class_='advert-list-items__content-address').get_text() for item in allItems]
    flat_price = flat_price + [item.find(class_='advert-list-items__content-price-price').get_text() for item in allItems]

# Putting data into dataframe
Flats = pd.DataFrame(
    {
        'FlatInfo': flat_info,
        'FlatAddress': flat_address,
        'FlatPrice': flat_price
    })

# Arrays for data
land_info = []
land_address = []
land_price = []

# Scraping data (lands)
for page in range(1, 21):
    if page == 1:
        html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-pozemky.html')
    else:
        html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-pozemky.html?stranka=' + str(page))

    bs = BeautifulSoup(html.read(), 'html.parser')
    allItems = bs.find_all(class_='advert-list-items__item')

    sleep(randint(2, 10))

    land_info = land_info + [item.find(class_='advert-list-items__content').h2.a.get_text() for item in allItems]
    land_address = land_address + [item.find(class_='advert-list-items__content-address').get_text() for item in allItems]
    land_price = land_price + [item.find(class_='advert-list-items__content-price-price').get_text() for item in allItems]

# Putting data into dataframe
Lands = pd.DataFrame(
    {
        'LandInfo': land_info,
        'LandAddress': land_address,
        'LandPrice': land_price
    })

# Importing data into database

conn = sqlite3.connect('Database.db')
c = conn.cursor()

Houses.to_sql('HOUSES_AND_VILLAS', conn, if_exists='append')
Flats.to_sql('FLATS', conn, if_exists='append')
Lands.to_sql('LANDS', conn, if_exists='append')
