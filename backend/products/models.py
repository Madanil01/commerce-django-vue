
# Create your models here.
from django.db import models
from .utils import file_path

class Product(models.Model):
    name = models.CharField(max_length=255)
    categoryId = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    imageUrl = models.ImageField(upload_to=file_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
