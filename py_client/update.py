import requests

endpoint = 'http://localhost:8000/api/products/1/update/'

data = {
    'title': 'This is amazing',
    'content': 'This is item 2'
}
get_response = requests.put(endpoint, json=data)
print(get_response.json())