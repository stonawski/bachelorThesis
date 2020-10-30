from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint

realEstate_info = []
address = []
price = []

for page in range(1, 17):
    if(page == 1):
        html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-domy_vily.html')
    else:
        html = urlopen('https://realitymix.cz/vyhledavani/olomoucky/prodej-domy_vily.html?stranka=' + str(page))

    bs = BeautifulSoup(html.read(), 'html.parser')
    allItems = bs.find_all(class_='advert-list-items__item')

    sleep(randint(2, 10))

    realEstate_info = realEstate_info + [item.find(class_='advert-list-items__content').h2.a.get_text() for item in allItems]
    address = address + [item.find(class_='advert-list-items__content-address').get_text() for item in allItems]
    price = price + [item.find(class_='advert-list-items__content-price-price').get_text() for item in allItems]

# print(realEstate_info)
# print(address)
# print(price)

real_estate = pd.DataFrame(
    {
        'RealEstateInfo': realEstate_info,
        'Address': address,
        'Price': price
    })
print(real_estate)
real_estate.to_csv('domy_vily.csv')