from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        """This func will run upon the creation of an instance"""
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = f'This is {title}.'
        serializer.save(content=content)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        content = serializer.validated_data.get('content')
        if not content:
            serializer.save(content=None)


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup = 'pk'


class ProductListAPIView(generics.ListAPIView):
    """Listing instances along"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    if request.method == 'POST': # Could either be a create or update request
        data = request.data
        serializer = ProductSerializer(data=data, many=False)
        if serializer.is_valid():
            # Checking if content is not None, if False content will be 'This is {title}'
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content')
            if not content:
                content = f'This is {title}.'
            serializer.save(content=content)
        return Response(serializer.data)

    elif request.method == 'GET': # Could either be a detail or list request
        if pk is not None: # Checking if pk is present, if so, it means it is a product detail request
            obj = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(obj, many=False).data
            return Response(serializer)
        