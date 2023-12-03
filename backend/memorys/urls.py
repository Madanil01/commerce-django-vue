from django.urls import path
from .views import MemoryListView,MemoryCreateView,MemoryDetailView
urlpatterns = [
    path('memory', MemoryListView.as_view(), name='memory'),
    path('memory/create', MemoryCreateView.as_view(), name='memory_create'),
    path('memory/details/<str:id>', MemoryDetailView.as_view(), name='color_detail'),

]
