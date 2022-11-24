from rest_framework import authentication, generics, mixins
from api.mixins import IsStaffEditorPermissionMixin, UserQuerySetMixin
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class ProductCreateAPIView(UserQuerySetMixin, IsStaffEditorPermissionMixin, generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """This func will run upon the creation of an instance"""
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = f'This is {title}.'
        serializer.save(content=content)


class ProductListCreateAPIView(UserQuerySetMixin, IsStaffEditorPermissionMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        user = self.request.user
        if content is None:
            content = title
        serializer.save(content=title, user=user)

    # def get_queryset(self):
    #     # qs = super().get_queryset()
    #     request = self.request
    #     user = request.user
    #     # if not user.is_authenticated:
    #     #     return Product.objects.none
    #     return Product.objects.filter(user=self.request.user)


class ProductDetailAPIView(UserQuerySetMixin, IsStaffEditorPermissionMixin, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup = 'pk'


class ProductListAPIView(UserQuerySetMixin, IsStaffEditorPermissionMixin, generics.ListAPIView):
    """Listing instances along"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateAPIView(UserQuerySetMixin, IsStaffEditorPermissionMixin, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    # permission_classes = [IsStaffEditorPermission]

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

class ProductDeleteAPIView(UserQuerySetMixin, IsStaffEditorPermissionMixin, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # Whatever logic necessary
        return super().perform_destroy(instance)



class SearchListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        results = Product.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results = qs.search(q, user=user)
        return results

class ProductMixinView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Mixins are classes that contan combination of methods from other classes. They inherit from other classes
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        """The method to list/retrieve products"""
        pk = kwargs.get('pk')
        if pk is not None:
            # Retrieve -> Product Detail
            return self.retrieve(request, *args, **kwargs)
        # List Products
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """The method to create products"""
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Runs when creating a new product"""
        if not serializer.validated_data.get('content'):
            serializer.save(content='Mixins are amazing')

    def patch(self, request, *args, **kwargs):
        """The method for partial_update of a product, which means all the fields of the Product model will be optional"""
        print(f'ARGS: {args}, KWARGS: {kwargs}')
        kwargs['partial'] = True
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        """Runs when updating an existing product"""
        instance = serializer.save()
        # if not instance.content:
        instance.content = 'Mixins sure are amazing'

    def delete(self, request, *args, **kwargs):
        """The method to delete products"""
        return self.destroy(request, *args, **kwargs)


@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    if request.method == 'POST': # A request to create a product
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