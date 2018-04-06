from rest_framework import serializers
from printerCtrl.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'productName', 'quantity', 'productFileName')
