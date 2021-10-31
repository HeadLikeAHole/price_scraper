import requests
from bs4 import BeautifulSoup

url = 'https://www.ozon.ru/product/elektricheskaya-zubnaya-shchetka-pribor-dlya-chistki-zubov-chernika-brand-shop-297569126/?asb=6tD3aQfPicHEhTIQLFWhoZQU6wwuvkLZOVm8QmEwZmI%253D&asb2=6dJiDATFK-3ktYwAhPenSeHL8aljAw89Ry2Xb7rvNpY&sh=WUG4oA9-'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

html_element = soup.find(class_='c2h3 c2h9 c2e7')
raw_price = html_element.getText()
print(type(page))
# remove whitespace and letters from the string and convert to an integer
# product_price = int(''.join([char for char in raw_price if char.isdigit()]))