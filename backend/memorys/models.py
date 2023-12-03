from django.db import models


class Memory(models.Model):
    size = models.CharField(max_length=255)

    def __str__(self):
        return self.name
