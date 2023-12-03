from rest_framework import serializers
from .models import Varian

class VarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Varian
        fields = ['id', 'size', 'color', 'productId', 'stock', 'price', 'imageUrl']
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }