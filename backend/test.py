from bs4 import BeautifulSoup
import requests


url = 'https://www.ozon.ru/product/smartfon-lenovo-k13-2-32gb-siniy-298657201/?sh=Ofov5wpy'

html_page = requests.get(url).text

print(html_page)

soup = BeautifulSoup(html_page, 'lxml')

# raw_price = soup.find(class_='c2h5').text

# remove whitespace and letters from the string and convert to an integer
# product_price = int(''.join([char for char in raw_price if char.isdigit()]))

# return product_price
