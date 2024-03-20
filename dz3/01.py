# http://books.toscrape.com
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

start_time = time.time()
ua = UserAgent()
url = 'http://books.toscrape.com'
path = '/catalogue/'
headers = {'User-Agent': ua.random}
session = requests.session()

all_books = []
count = 1
while True:
    page = f'page-{count}.html'
    response = session.get(url+path+page, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all('article', {'class': 'product_pod'})
    if not books:
        break
    for book in books:
        book_info = dict()
        name_link = book.find('h3')
        book_info['name'] = name_link.getText()
        book_info['price'] = float(book.find('p', {'class': 'price_color'}).getText()[2:])
        book_info['availability'] = book.find('p', {'class': 'instock availability'}).getText().strip()
        if book_info['availability'] == 'In stock':
            spoon = BeautifulSoup(session.get(url+path+name_link.find('a').get('href'), headers=headers).text, "html.parser")
            book_info['available'] = int(spoon.find('p', {'class': 'instock availability'}).getText().strip().replace('In stock (', '').replace(' available)', ''))
            description = spoon.find('div', {'id': 'product_description'})
            try:
                book_info['description'] = description.find_next('p').getText()
            except:
                book_info['description'] = None
        else:
            book_info['available'] = 0
        all_books.append(book_info)
    print("\033c")
    print(f"Обрабатываем страницу № {count}, прошло {time.time() - start_time:.2f} секунд")
    count += 1
filename = 'books.json'
with open(filename, 'w') as file:
    json.dump(all_books, file)

end_time = time.time()
print(f"Обработано за {end_time - start_time:.2f} секунд {len(all_books)} книг, сохранено в {filename}")
 