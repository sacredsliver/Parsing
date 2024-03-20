from clickhouse_driver import Client
import json
import time
from tokens import CLICKHOUSE_USER, CLICKHOUSE_PASS, CLICKHOUSE_HOST
NAME = 'books'

start_time = time.time()
# Подключение к серверу ClickHouse
client = Client(host = CLICKHOUSE_HOST,
                user=CLICKHOUSE_USER,
                secure = True, 
                port = 9440,
                password = CLICKHOUSE_PASS)
 
# Создание базы данных (если она не существует)
client.execute("DROP DATABASE IF EXISTS library")
client.execute("CREATE DATABASE IF NOT EXISTS library")
client.execute("DROP TABLE IF EXISTS library.books")
client.execute('''
CREATE TABLE IF NOT EXISTS library.books (
    id UInt64,
    name String,
    price Float64,
    availability String,
    available Int64,
    description Text
) ENGINE = MergeTree()
ORDER BY name
''')
table_time = time.time()
print(f"Таблица создана успешно. За: {table_time - start_time:.2f} секунд")

print(f'Загрузка данных в память...')
with open(NAME + '.json', 'r') as file:
    books = json.load(file)

memory_time = time.time()
print(f"{len(books)} документов из {NAME}.json загружены в память. За: {memory_time - table_time:.2f} секунд")


count = 0
books_values = []
for book in books:
    books_values.append((count,
    book['name'] or "",
    book['price'] or "",
    book['availability'] or "",
    book['available'] or "",
    book['description'] or ""))
    count += 1

print(f"{count} строк преобразовано в кортеж. За: {time.time() - memory_time:.2f} секунд")

click_time = time.time()
print(f'Загрузка данных в ClickHouse...')
client.execute("""
    INSERT INTO library.books (
        id, name, price,
        availability, available, description
    ) VALUES""", books_values)

print(f"{count} строк загружено в таблицу {NAME} ClickHouse. За: {time.time() - click_time:.2f} секунд")

rows_count = client.execute("SELECT count() FROM library.books")
print(f"Количество строк в таблице library.books: {rows_count[0][0]}")
print(f"Не загруженных данных: {len(books) - rows_count[0][0]}")

print(f"Общее время работы программы: {time.time() - start_time:.2f} секунд")