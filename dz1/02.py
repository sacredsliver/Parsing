# https://developers.google.com/youtube/v3/docs/search/list
from tokens import GOOGLE # google api key
import json
import requests

url = "https://www.googleapis.com/youtube/v3/search"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Accept":  "*/*"
}

params = {
    "key": GOOGLE,
    "part": "id, snippet",
    "maxResults": 10,
    "order": "rating",
    "q": "geekbrains",
    "order": "rating"
}

response = requests.get(url, params=params, headers=headers)

if response.ok:
    data = json.loads(response.text)
    count = 1
    for item in data["items"]:
        print(count, item["snippet"]["title"])
        print(f'https://www.youtube.com/watch?v={item["id"]["videoId"]}\n')
        count+=1
else:
    print("Error")
