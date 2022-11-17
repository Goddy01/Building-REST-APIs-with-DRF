from rest_framework import generics, mixins
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


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # Whatever logic necessary
        return super().perform_destroy(instance)

class ProductMixinView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    Mixins are classes that contan combination of methods from other classes. They inherit from other classes
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        """The method for list/retrieve mixins"""
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """The method for create/update mixins"""
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Runs when creating a new instance"""
        if not serializer.validated_data.get('content'):
            serializer.save(content='Mixins are amazing')

    def patch(self, request, *args, **kwargs):
        """The method for partial_update of an instance, which means all the fields for the update will be optional"""
        print(f'ARGS: {args}, KWARGS: {kwargs}')
        kwargs['partial'] = True
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        """Runs when updating an existing instance"""
        instance = serializer.save()
        # if not instance.content:
        instance.content = 'Mixins sure are amazing'

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
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        
        # If no pk is present, then it means it is a list request
        qs = Product.objects.all()
        data = ProductSerializer(qs, many=True).data
        return Response(data)