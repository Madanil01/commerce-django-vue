from django.urls import path
from .views import ColorListView,ColorCreateView,ColorDetailView
urlpatterns = [
    path('color', ColorListView.as_view(), name='color'),
    path('color/create', ColorCreateView.as_view(), name='color_create'),
    path('color/details/<str:id>', ColorDetailView.as_view(), name='color_detail'),

]
