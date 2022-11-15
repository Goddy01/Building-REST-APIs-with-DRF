import json
from django.http import JsonResponse


def api_home(request, *args, **kwargs):
    print(request.GET)
    print(request.POST)
    
    body = request.body
    data = {}
    try:
        data = json.loads(body) # String of Json data to Python Dict
    except:
        pass
    print(data)
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type
    data['params'] = dict(request.GET)
    # print(request.headers)
    return JsonResponse(data)