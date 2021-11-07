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


def scrape_price(url, css_classes):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}

    html_page = requests.get(url, headers).text

    soup = BeautifulSoup(html_page, 'lxml')

    css_classes_list = css_classes.split(', ')
    for css_class in css_classes_list:
        html_element = soup.find(class_=css_class)
        if html_element is None:
            continue
        else:
            raw_price = html_element.text

            # remove whitespace and letters from the string and convert to an integer
            product_price = int(''.join([char for char in raw_price if char.isdigit()]))

            return product_price

    return None
