import os
import re
import smtplib

from bs4 import BeautifulSoup
import requests


def send_email(subject, body, recipient):
    server = smtplib.SMTP_SSL('smtp.yandex.com', 465)

    server.login(os.environ.get('EMAIL_HOST_USER'), os.environ.get('EMAIL_HOST_PASSWORD'))

    message = f'Subject: {subject} \n\n{body}'

    server.sendmail(os.environ.get('EMAIL_HOST_USER'), recipient, message)

    print('Email has been sent!')

    server.quit()


def extract_store_name(url):
    result = re.search(r'www\.(\w+)\.', url)

    if result is not None:
        return result.group(1)

    return None


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


def scrape_price(product):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}

    html_page = requests.get(product.url, headers).text

    soup = BeautifulSoup(html_page, 'lxml')

    css_classes_list = product.store.css_classes.split(', ')
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
