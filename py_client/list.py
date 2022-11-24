import requests
from getpass import getpass

auth_endpoint = 'http://localhost:8000/api/auth/'

username = input('Username: ')
password = getpass()
get_auth_response = requests.post(auth_endpoint, json={'username': username, 'password': password})
# print(get_auth_response.json())

if get_auth_response.status_code == 200:
    token = get_auth_response.json()['token']
    headers = {
        'Authorization': f'Bearer {token}'
    }
    endpoint = 'http://localhost:8000/api/products/list/'

    get_response = requests.get(endpoint, headers=headers)
    data = (get_response.json())
    next_url = data['next']
    if next_url is not None:
        print('next_url: ', next_url)
    previous_url = data['previous']
    if previous_url is not None:
        print('previous_url: ', previous_url)
    results = data['results']
    print('results: ', results)

else:
    print('Wrong login details provided!!!')