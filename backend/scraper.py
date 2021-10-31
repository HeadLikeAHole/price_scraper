import re

from bs4 import BeautifulSoup
import requests


# css classes by which prices are searched
CSS_CLASSES = {
    'ozon': 'product-prices__price'
}


def extract_store_name(url):
    result = re.search(r'www\.(\w+)\.', url)

    if result is not None:
        return result.group(1)


def scrape_price(url):
    store_name = extract_store_name(url)

    html_page = requests.get(url).text

    soup = BeautifulSoup(html_page, 'lxml')

    raw_price = soup.find(class_=CSS_CLASSES[store_name]).text

    # remove whitespace and letters from the string and convert to an integer
    product_price = int(''.join([char for char in raw_price if char.isdigit()]))

    return product_price
