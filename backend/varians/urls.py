from django.urls import path
from .views import VarianListView, VarianCreateView, VarianDetailView, VarianUpdateView, VarianDeleteView


urlpatterns = [
    path('varian', VarianListView.as_view(), name='varian'),
    path('varian/create', VarianCreateView.as_view(), name='varian_create'),
    path('varian/details/<str:id>', VarianDetailView.as_view(), name='varian_detail'),
    path('varian/update/<str:id>', VarianUpdateView.as_view(), name='varian_update'),
    path('varian/delete/<str:id>', VarianDeleteView.as_view(), name='varian_delete'),
]
