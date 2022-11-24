from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from .validators import validate_title_no_hello, unique_title_validator
from api.serializers import UserPublicSerializer, UserProductInlineSerializer


class ProductSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    email = serializers.EmailField(write_only=True)
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    title = serializers.CharField(validators=[validate_title_no_hello, unique_title_validator])
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field = 'pk'
    )
    related_fields = UserProductInlineSerializer(many=True, source='user.product_set.all', read_only=True)
    # name = serializers.CharField(source='title', read_only=True)
    class Meta:
        model = Product
        fields = ['user', 'pk', 'url', 'edit_url', 'email', 'title', 'content', 'price', 'sale_price', 'my_discount', 'related_fields'
        # 'name'
        ]

    # Custom Validation wih Serializer (1)
    # def validate_title(self, value):
    #     obj = Product.objects.filter(title__iexact=value)
    #     if obj.exists():
    #         return serializers.ValidationError(f"'{value}' is already a product name.")
    #     return value
    
    def create(self, validated_data):
        email = validated_data.pop('email')
        # print(email)
        return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     email = validated_data.pop('email')
    #     return super().update(instance, validated_data)

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        # print(request)
        return reverse("product-edit", kwargs={'pk': obj.pk}, request=request)

    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            # Checks if obj has an attr called 'id'
            return None
        if not isinstance(obj, Product):
            # Checks if obj is an instance of Product
            return None
        return obj.get_discount()