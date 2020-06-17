from .models import Room, Product, Category, Payment, ProductUsed, Bill
from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'roomId', 'price', 'status', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'sku', 'productName', 'category', 'price',
                  'discount', 'description', 'stock', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']


class InlineProductUsedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUsed
        fields = ['productId', 'quantity', 'created_at']


class ProductUsedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUsed
        fields = ['id', 'payment', 'productId', 'price',
                  'quantity', 'created_at']

        def create(self, validated_data):
            productUsed = ProductUsed()
            productUsed.productId = validated_data["productId"]
            productUsed.quantity = validated_data["quantity"]
            productUsed.payment = validated_data["payment"]

            return productUsed


class PaymentSerializer(serializers.ModelSerializer):
    products = InlineProductUsedSerializer(many=True)

    class Meta:
        model = Payment
        fields = ['id', 'room', 'checkInDate', 'status', 'price',
                  'checkOutDate', 'products', 'total']

    def create(self, validated_data):
        payment = Payment()
        payment.checkInDate = validated_data["checkInDate"]
        if "checkOutDate" in validated_data:
            payment.checkOutDate = validated_data["checkOutDate"]
        else:
            payment.checkOutDate = None
        payment.status = validated_data["status"]

        payment.room = validated_data["room"]

        return payment

    def update(self, instance, validated_data):
        instance.status = validated_data["status"]

        instance.checkInDate = validated_data["checkInDate"]

        if "checkOutDate" in validated_data:
            instance.checkOutDate = validated_data["checkOutDate"]
        else:
            instance.checkOutDate = None
        return instance


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'room', 'checkInDate', 'status', 'products',
                  'checkOutDate', 'total']
