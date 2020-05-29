from django.contrib import admin

# Register your models here.
from .models import Room, Product, Payment, ProductUsed, Bill


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'roomId', 'price', 'status')
    list_display_links = ('id', 'roomId')
    list_per_page = 25


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'productName', 'price', 'stock')
    list_display_links = ('id', 'productName', 'price', 'stock')
    list_per_page = 25


class ProductUsedInline(admin.StackedInline):
    model = ProductUsed
    extra = 0


class PaymentAdmin(admin.ModelAdmin):
    inlines = [ProductUsedInline, ]
    list_display = ('id', 'room', 'total', 'checkInDate',
                    'checkOutDate', 'status')
    list_display_links = ('id', 'room')
    list_per_page = 25


admin.site.register(Room, RoomAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(ProductUsed)
admin.site.register(Bill)
