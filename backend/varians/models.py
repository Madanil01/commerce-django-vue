
# Create your models here.
from django.db import models
from .utils import file_path


class Varian(models.Model):
    size = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    productId = models.CharField(max_length=255)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    imageUrl = models.ImageField(upload_to=file_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
