#!/usr/bin/env python
# Данный скрипт является логическим продолжением темы второго семинара задачи № 2,
# где мы парсили публикации с сайта https://gb.ru/posts с помощью BeautifulSoup.
# В данной работе я скрейпил уже страницы форума https://gb.ru/topics, с помощью XPath.
# На страницах информация представлена в виде таблиц. Далее, произвожу парсинг, извлекая
# информацию о каждой теме. Извлечённая информация сохраняется в csv-файл. 
import requests # библиотека для загрузки данных из интернета
import csv # библиотека для работы с файлами csv
from lxml import html # html-парсер
from fake_useragent import UserAgent as ua # библиотека для загрузки случайного user-agent
from datetime import datetime # библиотека для работы с форматами дат, нужна для преобразования из строк
import locale # библиотека для работы с локализацией, необходима для правильного преобразования русских месяцев
locale.setlocale(locale.LC_TIME, 'ru_RU.utf8') # указываю русскую локализацию, для преобразования месяцев

url = 'https://gb.ru' # адрес сайта ГБ
file = '/topics' # страницы форума, часть ссылки на форум
headers = {'User-Agent': ua().random} # заголовки со случайным user-agent, для сокрытия скрейпинга

page = 1 # номер страницы форума
params = {
    "page": page, # номер страницы, передаваемый как параметр
}
session = requests.Session() # создание сессии, для сокрытия скрейпинга

items_list = [] # список словарей с информацией о темах
while True: # цикл для парсинга всех страниц форума
    # получение данных с сайта
    response = session.get(f"{url}{file}?page={page}", headers=headers)
    # преобразования данных и строки в объект lxml
    dom = html.fromstring(response.text)
    # парсинг всех блоков (ячеек) из табличной информации на странице форума
    items = dom.xpath('//div[@class="topics-list__item topic-item"]')
    if not items: # условие выхода из цикла, если не было найдено ни одной темы
        break
    # добавление в список словарей информации о каждой теме
    for item in items:
        item_info = {} # создание словаря с информацией о теме
        # парсинг имени автора, преобразование в список строк и получение первой записи, т.к. автор один
        item_info['author'] = item.xpath('.//a[@class="topic-item-statistics__user-name"]/text()')[0]
        # парсинг ссылки на автора, преобразование в строку, на выходе полная ссылка на профиль автора форума
        item_info['author_link'] = url+item.xpath('.//a[@class="topic-item-statistics__img-wrapper"]/@href')[0]
        try: # "ловля" исключений, в случае если нет информации о количестве ответов
            # если количество ответов есть, то сохраняем его в качестве целого числа
            item_info['count_answer'] = int(item.xpath('.//div[@class="topic-answers__counter topic-answers__counter_color_green"]/text()')[0])
        except: # если информации о количестве ответов нет, то сохраняем ноль ответов, как целое число
            item_info['count_answer'] = 0
        # парсинг описания временного интервала, прошедшего с последнего ответа в теме, как строка
        item_info['last_answer'] = item.xpath('.//div[@class="topic-item-statistics__text topic-item-statistics__text_color_muted"]/text()')[0]
        # теги присвоенные теме в виде списка, т.к. тегов бывает несколько
        item_info['tags'] = item.xpath('.//a[@class="topic-item__tag-link"]/text()')
        # парсинг времени создания темы, преобразование в строку. В строке удаляем букву "в", 
        # удаляем лишние символы и первую букву в месяце делаем прописной, для преобразования в формат даты
        time_str = item.xpath('.//div[@class="topic-item__date"]/text()')[0].replace(' в ', ' ').strip().title()
        # преобразование в формат даты из заданному шаблона с преобразованием в выходной формат даты 2000-01-01 00:00
        item_info['time'] = datetime.strptime(time_str, '%d %B %Y %H:%M').strftime('%Y-%m-%d %H:%M')
        # парсинг названия темы, преобразование в строку, т.к тема одна берем первый элемент списка
        item_info['topic'] = item.xpath('.//a[@class="topic-item__title"]/text()')[0]
        # парсинг ссылки на тему, преобразование в строку
        item_info['topic_link'] = url+item.xpath('.//a[@class="topic-item__title"]/@href')[0]
        # добавление словаря в список словарей с информацией о каждой теме
        items_list.append(item_info)
    print(f"Обработана страница № {page}") # вывод на экран номера обработанной страницы
    page += 1 # увеличение номера обработанной страницы на единицу

# сохранение полученной информации в CSV файл
csv_file = 'gb_topics.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=items_list[0].keys()) # первая строка файла будет иметь названия полей
    writer.writeheader() # запись в первую строку названия полей
    writer.writerows(items_list) # запись в файл остальной информации

# вывод на экран информации о csv-файле, общем количестве обработанных страниц и тем
print(f"Сохранено {page} страниц форума {url+file} с количеством тем {len(items_list)} в файл {csv_file}")

