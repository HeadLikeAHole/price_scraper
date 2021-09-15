import smtplib
import os
import requests
from bs4 import BeautifulSoup


def send_mail():
    server = smtplib.SMTP_SSL('smtp.yandex.com', 465)
    # server.starttls()

    server.login('igorwho@yandex.ru', 'spellbound2010')

    subject = 'The price went down'
    body = 'Check the link https://www.lamoda.ru/p/rtlaao673801/shoes-nike-krossovki/'

    msg = f'Subject: {subject} \n\n{body}'

    server.sendmail('igorwho@yandex.ru', 'igorwho@yandex.ua', msg)

    print('Message has been sent!')

    server.quit()


URL = 'https://www.lamoda.ru/p/rtlaao673801/shoes-nike-krossovki/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}

desired_price = 10000

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

price_str = soup.find(class_='product-prices__price').getText()

# remove whitespace and letters and convert to integer
product_price = int(''.join([i for i in price_str if i.isdigit()]))

if product_price <= desired_price:
    send_mail()
