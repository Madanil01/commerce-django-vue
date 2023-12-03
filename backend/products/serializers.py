from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'categoryId', 'description', 'price', 'imageUrl']
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }