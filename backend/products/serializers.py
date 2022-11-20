from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = ['pk', 'title', 'content', 'price', 'sale_price', 'my_discount']

    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            # Checks if obj has an attr called 'id'
            return None
        if not isinstance(obj, Product):
            # Checks if obj is an instance of Product
            return None
        return obj.get_discount()