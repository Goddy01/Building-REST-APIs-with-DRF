from .models import Product
from .serializers import ProductSerializer
from rest_framework import viewsets


class ProductViewset(viewsets.ModelViewSet):
    """
    GET -> LIST -> QUERYSET
    GET -> DETAIL -> INSTANCE
    POST -> CREATE -> A NEW INSTANCE
    PUT -> FULL UPDATE
    PATCH -> PARTIAL UPDATE
    DELETE -> DESTROY
    """
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'