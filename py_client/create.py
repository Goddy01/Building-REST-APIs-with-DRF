import requests

endpoint = 'http://localhost:8000/api/products/create/'

data = {'title': 'Monday'}
get_response = requests.post(endpoint, json=data)

print(get_response.json())