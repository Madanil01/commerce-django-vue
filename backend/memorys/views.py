from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Memory
from .serializers import MemorySerializer
from django.shortcuts import get_object_or_404


class MemoryListView(APIView):
    def get(self, request):
        memory = Memory.objects.all()
        serializer = MemorySerializer(memory, many=True)
        return Response(serializer.data)
    
class MemoryCreateView(APIView):
    def post(self, request):
        serializer = MemorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#search by id
class MemoryDetailView(APIView):
    def get(self, request, id):
        memory = get_object_or_404(Memory, id=id)
        serializer = MemorySerializer(memory)
        return Response(serializer.data)

class MemoryUpdateView(APIView):
    def put(self, request, id):
        memory = get_object_or_404(Memory, id=id)
        serializer = MemorySerializer(memory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemoryDeleteView(APIView):
    def delete(self, request, id):
        memory = get_object_or_404(Memory, id=id)
        memory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    