import os
import smtplib
import requests
from bs4 import BeautifulSoup
from models import User, Product


def send_email(title, link, recipient):
    server = smtplib.SMTP_SSL('smtp.yandex.com', 465)

    server.login(os.environ.get('EMAIL_USERNAME'), os.environ.get('EMAIL_PASSWORD'))

    subject = 'Price Drop!'
    body = 'Check the link of the product https://www.lamoda.ru/p/rtlaao673801/shoes-nike-krossovki/'

    message = f'Subject: {subject} \n\n{body}'

    server.sendmail(os.environ.get('EMAIL_USERNAME'), recipient, message)

    print('Message has been sent!')

    server.quit()


def check_price(user_id=None, product_id=None):
    
    URL = 'https://www.lamoda.ru/p/rtlaao673801/shoes-nike-krossovki/'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}

    desired_price = 10000

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    price_str = soup.find(class_='product-prices__price').getText()

    # remove whitespace and letters and convert to integer
    product_price = int(''.join([i for i in price_str if i.isdigit()]))

    if product_price <= desired_price:
        send_email()
