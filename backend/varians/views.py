from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Varian 
from .serializers import VarianSerializer
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage


class VarianListView(APIView):
    def get(self, request):
        varian = Varian.objects.all()
        serializer = VarianSerializer(varian, many=True)
        return Response(serializer.data)
    
class VarianCreateView(APIView):
    def post(self, request):
        varian = VarianSerializer(data=request.data)
        varian.size = request.data.get('size')
        varian.color = request.data.get('color')
        varian.productId = request.data.get('productId')
        varian.stock = request.data.get('stock')
        varian.price = request.data.get('price')
        if len(request.FILES) != 0:
            varian.imageUrl = request.FILES['imageUrl']
        if varian.is_valid():
            varian.save()
            return Response(varian.data, status=status.HTTP_201_CREATED)
        return Response(varian.errors, status=status.HTTP_400_BAD_REQUEST)
    
#search by id
class VarianDetailView(APIView):
    def get(self, request, id):
        varian = get_object_or_404(Varian, id=id)
        serializer = VarianSerializer(varian)
        return Response(serializer.data)

class VarianUpdateView(APIView):
    def put(self, request, id):
        varian = get_object_or_404(Varian, id=id)
        var = VarianSerializer(varian, data=request.data)

        if var.is_valid():
            var.save()

            # Check if 'imageUrl' is present in request.FILES
            if 'imageUrl' in request.FILES and request.FILES['imageUrl']:
                # Hapus gambar lama jika ada
                if varian.imageUrl:
                    image_path = str(varian.imageUrl.path)
                    default_storage.delete(image_path)

                # Update 'imageUrl' separately as it's not part of the serializer fields
                varian.imageUrl = request.FILES['imageUrl']
                varian.save()

            return Response(var.data)
        else:
            return Response(var.errors, status=status.HTTP_400_BAD_REQUEST)
        
class VarianDeleteView(APIView):
    def delete(self, request, id):
        varian = get_object_or_404(Varian, id=id)

        # Mendapatkan path file gambar
        image_path = str(varian.imageUrl)

        # Hapus produk
        varian.delete()
        # Hapus gambar dari sistem file
        try:
            default_storage.delete(image_path)
        except FileNotFoundError:
            # File tidak ditemukan, dapat diabaikan atau lakukan penanganan khusus jika diperlukan
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
