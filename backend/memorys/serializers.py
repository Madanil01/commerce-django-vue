from rest_framework import serializers
from .models import Memory

class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ['id', 'size']
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }