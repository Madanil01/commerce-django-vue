from django.urls import path
from .views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProductDetailView

urlpatterns = [
    path('products', ProductListView.as_view()),
    path('products/create', ProductCreateView.as_view(), name='product_create'),
    path('products/details/<str:id>', ProductDetailView.as_view(), name='product_detail'),
    path('products/update/<str:id>', ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<str:id>', ProductDeleteView.as_view(), name='product_delete'),
]
