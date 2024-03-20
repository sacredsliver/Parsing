import json
import time
from pymongo import MongoClient
from tokens import ATLAS_USER, ATLAS_PASS, ATLAS_HOST
NAME = 'books'

start_time = time.time()
uri = f"mongodb+srv://{ATLAS_USER}:{ATLAS_PASS}@cluster0.{ATLAS_HOST}.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['library']
collection = db[NAME]

# Получение количества документов в коллекции с помощью функции count_documents()
count = collection.count_documents({})
print(f'Число записей в базе {NAME}: {count}')

# Получение одного документа с помощью find_one()
document = collection.find_one()
print(f'Типовой документ иммеет поля: {document.keys()}')

# Поиск документов с одинаковыми значениями name
duplicates = collection.aggregate([
    {"$group": {"_id": {"name": "$name", "price": "$price", "availability": "$availability"}, "count": {"$sum": 1}}},
    {"$match": {"count": {"$gt": 1}}}
])

# Найти самую дешевую книгу
cheapest = collection.aggregate([
    {"$group": {"_id": "$name", "min_price": {"$min": "$price"}}},
    {"$sort": {"min_price": 1}}
])
cheapest = list(cheapest)[0]
print(f'Самая дешевая книга: {cheapest["_id"]} стоит £{cheapest["min_price"]:.2f}')


# Найти самую дорогую книгу
most_expensive = collection.aggregate([
    {"$group": {"_id": "$name", "max_price": {"$max": "$price"}}},
    {"$sort": {"max_price": -1}}
])
most_expensive = list(most_expensive)[0]
print(f'Самая дорогая книга: {most_expensive["_id"]} стоит £{most_expensive["max_price"]:.2f}')

# Найти книгу, которой больше всего в наличии (на складе)
most_available = collection.aggregate([
    {"$group": {"_id": "$name", "count": {"$max": "$available"}}},
    {"$sort": {"count": -1}}
])
most_available = list(most_available)[0]
print(f'Больше всего книг в наличие: {most_available["_id"]} их {most_available["count"]} шт.')
