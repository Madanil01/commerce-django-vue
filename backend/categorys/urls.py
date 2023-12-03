from django.urls import path
from .views import CategoryListView, CategoryCreateView, CategoryDetailView
urlpatterns = [
    path('category', CategoryListView.as_view(), name='category'),
    path('category/create', CategoryCreateView.as_view(), name='category_create'),
    path('category/details/<str:id>', CategoryDetailView.as_view(), name='category_detail'),

]
