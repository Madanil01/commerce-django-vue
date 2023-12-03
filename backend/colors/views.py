from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Color
from .serializers import ColorSerializer
from django.shortcuts import get_object_or_404


class ColorListView(APIView):
    def get(self, request):
        color = Color.objects.all()
        serializer = ColorSerializer(color, many=True)
        return Response(serializer.data)
    
class ColorCreateView(APIView):
    def post(self, request):
        serializer = ColorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#search by id
class ColorDetailView(APIView):
    def get(self, request, id):
        color = get_object_or_404(Color, id=id)
        serializer = ColorSerializer(color)
        return Response(serializer.data)
    
class ColorUpdateView(APIView):
    def put(self, request, id):
        color = get_object_or_404(Color, id=id)
        serializer = ColorSerializer(color, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ColorDeleteView(APIView):
    def delete(self, request, id):
        color = get_object_or_404(Color, id=id)
        color.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    