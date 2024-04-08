#!/usr/bin/env python3
from auchan import *
import time

def main(keyword):
    goods_list = scraper.goods(keyword)
    return goods_list

if __name__ == "__main__":
    start_time = time.time()
    print("\033c")
    keyword = input("Введите ключевое слово для поиска товаров: ")
    big_list = main(keyword)
    unique_list = db.unique(big_list)
    print("\033c")
    db.csv_file(keyword, big_list)
    db.json_file(keyword, unique_list)
    # db.upload("auchan", keyword, main_list) 
    print(f"Время выполнения: {time.time() - start_time:.2f} секунд")
