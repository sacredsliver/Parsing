import csv
import json
from pymongo import MongoClient
from auchan.tokens import ATLAS_USER, ATLAS_PASS, ATLAS_HOST

uri = f"mongodb+srv://{ATLAS_USER}:{ATLAS_PASS}@cluster0.{ATLAS_HOST}.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

def download(dbname: str, collection: str)->list:
    db = client[dbname]
    collection = db[collection]
    documents = list(collection.find())
    return documents


def upload(dbname: str, collection: str, dicts_list: list)->int:
    counter = len(dicts_list)
    if counter == 0: return 0
    db = client[dbname]
    collection = db[collection]
    collection.insert_many(dicts_list)
    print(f"{counter} документов записано в БД {dbname} коллекцию {collection}")
    return counter


def unique(dicts_list: list)->list:
    return list({v["_id"]:v for v in dicts_list}.values())


def csv_file(keyword: str, dicts_list: list, delimiter='\t', encoding='utf-8', headers=False)->int:
    counter = len(dicts_list)
    if counter == 0: return 0
    with open(f"{keyword}.md", 'w', newline='\n', encoding=encoding) as f:
        fieldnames = dicts_list[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        if headers: writer.writeheader()
        writer.writerows(dicts_list)
    print(f"{counter} строк записано в {keyword}.md")
    return counter


def json_file(keyword: str, dicts_list: list)->int:
    counter = len(dicts_list)
    if counter == 0: return 0
    with(open(keyword + ".json", "w")) as file:
        json.dump(dicts_list, file, ensure_ascii=False, indent=4)
    print(f"{counter} словарей записано в файл {keyword}.json")
    return counter


if __name__ == '__main__':
    DB = 'auchan'
    COLLECTION = 'smartphones'
    downloaded_list = download(DB, COLLECTION)
    print(len(downloaded_list))
    print(type(downloaded_list))