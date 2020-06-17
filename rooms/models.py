from django.db import models
from datetime import datetime, date
import decimal


class Room(models.Model):
    roomId = models.CharField(max_length=255, unique=True)
    price = models.IntegerField()
    AVAILABLE = 'available'
    NOT_AVAILABLE = 'notAvailable'

    STATUS_CHOICES = (
        (AVAILABLE, 'AVAILABLE'),
        (NOT_AVAILABLE, 'NOT AVAILABLE'),
    )

    status = models.CharField(
        max_length=31,
        choices=STATUS_CHOICES,
        default=AVAILABLE
    )

    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.roomId


class Category(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=255, unique=True)
    productName = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", blank=True, null=True)
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    stock = models.IntegerField(default=0)

    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.productName


class Payment(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="payments")

    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    checkInDate = models.DateTimeField(default=datetime.now)
    checkOutDate = models.DateTimeField(null=True, blank=True)

    CHECKED_IN = 'checkedIn'
    CHECKED_OUT = 'checkedOut'

    STATUS_CHOICES = (
        (CHECKED_IN, 'CHECKED IN'),
        (CHECKED_OUT, 'CHECKED OUT'),
    )

    status = models.CharField(
        max_length=31,
        choices=STATUS_CHOICES
    )

    def get_total(self):
        if self.checkOutDate is None:
            return 0
        diff = ((self.checkOutDate - self.checkInDate) / 3600)
        diff = diff.total_seconds()
        print(diff)
        price = self.price * decimal.Decimal(diff)

        for product in self.products.all():
            price = decimal.Decimal(
                price) + product.productId.price * product.quantity

        return price

    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.status


class ProductUsed(models.Model):
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="products")
    productId = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="payments")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    created_at = models.DateTimeField(default=datetime.now)


class Bill(models.Model):
    room = models.CharField(max_length=255)

    checkInDate = models.DateTimeField(default=datetime.now)
    checkOutDate = models.DateTimeField(null=True, blank=True)

    CHECKED_IN = 'checkedIn'
    CHECKED_OUT = 'checkedOut'

    STATUS_CHOICES = (
        (CHECKED_IN, 'CHECKED IN'),
        (CHECKED_OUT, 'CHECKED OUT'),
    )

    products = models.TextField()

    status = models.CharField(
        max_length=31,
        choices=STATUS_CHOICES
    )

    total = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.status
