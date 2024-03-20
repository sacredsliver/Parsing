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


with open(NAME + '.json') as f:
    data = json.load(f)

print(f"{len(data)} docs is loaded from file {NAME}.json in {time.time() - start_time:.2f} seconds")
print(f'Going to upload it to MongoDB Atlas cloud server')

upload_time = time.time()
collection.insert_many(data)
uploaded_docs = collection.count_documents({})

print(f"{uploaded_docs} docs is uploaded to MongoDB in {time.time() - upload_time:.2f} seconds")
print(f"Total time: {time.time() - start_time:.2f} seconds. {len(data) - uploaded_docs} docs is not uploaded")



