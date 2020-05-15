from .models import Room, Product, Category, Payment
from rest_framework import serializers


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'roomId', 'price', 'status', 'created_at']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'sku', 'productName', 'category', 'price',
                  'discount', 'description', 'stock', 'created_at']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'checkInDate', 'checkOutDate', 'total']
