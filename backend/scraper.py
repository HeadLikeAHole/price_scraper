import re

from bs4 import BeautifulSoup
import requests


# css classes by which prices are searched
CSS_CLASSES = {
    'wildberries': [
        'price-block__final-price',
        'price-block__commission-current-price'
    ],
    'lamoda': [
        'product-prices-root'
    ],
}


def extract_store_name(url):
    result = re.search(r'www\.(\w+)\.', url)

    if result is not None:
        return result.group(1)


def scrape_price(url):
    store_name = extract_store_name(url)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}

    html_page = requests.get(url, headers).text

    soup = BeautifulSoup(html_page, 'lxml')

    for class_ in CSS_CLASSES[store_name]:
        if soup.find(class_=class_) is None:
            continue
        else:
            raw_price = soup.find(class_=CSS_CLASSES[store_name]).text

            # remove whitespace and letters from the string and convert to an integer
            product_price = int(''.join([char for char in raw_price if char.isdigit()]))

            return product_price

    return None
