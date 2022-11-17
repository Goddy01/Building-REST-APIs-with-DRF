import requests

endpoint = 'http://localhost:8000/api/products/mixins/1/update/'

data = {
    'title': 'Mixins',
}
get_response = requests.patch(endpoint, json=data)
print(get_response.json())