import json
# from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms.models import model_to_dict
from products.models import Product
from products.serializers import ProductSerializer

@api_view(["GET"])
def api_home(request, *args, **kwargs):
    """DRF API VIEW"""
    data = {}
    instance = Product.objects.all().order_by("?").first()

    if instance:
        # data = model_to_dict(instance, fields=['content', 'id'])
        data = ProductSerializer(instance).data
    return Response(data)