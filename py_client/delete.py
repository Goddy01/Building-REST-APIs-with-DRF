import requests

product_id = input('What is the id of the product you want to delete? ')
try:
    product_id = int(product_id)
except:
    print(f'{product_id} is not a valid id.')
    product_id = None
else:
    if product_id:
        endpoint = f'http://localhost:8000/api/products/mixins/{product_id}/delete/'

        get_response = requests.delete(endpoint)
        print(get_response, get_response.status_code==204)