import json
# from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms.models import model_to_dict
from products.models import Product

@api_view(["GET"])
def api_home(request, *args, **kwargs):
    """DRF API VIEW"""
    data = {}
    model_data = Product.objects.all().order_by("?").first()

    if model_data:
        data = model_to_dict(model_data, fields=['content', 'id'])
    return Response(data)