from django.shortcuts import render
from django.core.files.storage import default_storage
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class ProductCreateView(APIView):
    def post(self, request):
        prod  = ProductSerializer(data=request.data)
        prod.name = request.data.get('name')
        prod.categoryId = request.data.get('categoryId')
        prod.description = request.data.get('description')
        prod.price = request.data.get('price')
        if len(request.FILES) != 0:
            prod.imageUrl = request.FILES['imageUrl']

        prod.is_valid(raise_exception=True)
        prod.save()
        return Response(prod.data)
        
class ProductDetailView(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
class ProductUpdateView(APIView):
    def put(self, request, id):
        product = get_object_or_404(Product, id=id)
        prod = ProductSerializer(product, data=request.data)

        if prod.is_valid():
            prod.save()

            # Check if 'imageUrl' is present in request.FILES
            if 'imageUrl' in request.FILES and request.FILES['imageUrl']:
                # Hapus gambar lama jika ada
                if product.imageUrl:
                    image_path = str(product.imageUrl.path)
                    default_storage.delete(image_path)

                # Update 'imageUrl' separately as it's not part of the serializer fields
                product.imageUrl = request.FILES['imageUrl']
                product.save()

            return Response(prod.data)
        else:
            return Response(prod.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteView(APIView):
    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)

        # Mendapatkan path file gambar
        image_path = str(product.imageUrl)

        # Hapus produk
        product.delete()
        # Hapus gambar dari sistem file
        try:
            default_storage.delete(image_path)
        except FileNotFoundError:
            # File tidak ditemukan, dapat diabaikan atau lakukan penanganan khusus jika diperlukan
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
