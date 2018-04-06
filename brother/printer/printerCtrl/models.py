from django.db import models

class Product(models.Model):
    productID = models.CharField(max_length=30)
    productName = models.CharField(max_length=30)
    quantity = models.CharField(max_length=12)
    productFileName = models.CharField(max_length=100)

    class Meta:
        ordering = ('productID',)
