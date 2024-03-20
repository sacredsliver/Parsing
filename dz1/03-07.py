from tokens import TOKEN4SQUARE
import requests
import json

category = input("Введите название категории для поиска: ")

url = "https://api.foursquare.com/v3/places/search"

params = {
    # "near": "London",
    "limit": 10,
  	"query": category
}

headers = {
    "Accept": "application/json",
    "Authorization": TOKEN4SQUARE
}

response = requests.get(url, params=params, headers=headers)
data = json.loads(response.text)

if response.ok:
    for res in data["results"]:
        print(res['name'])
        print(res['fsq_id'])
        print(res['location']['formatted_address'], end='\n\n')
else:
    print("Error")
