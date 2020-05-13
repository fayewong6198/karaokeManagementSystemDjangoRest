from django.contrib import admin

# Register your models here.
from .models import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'roomId', 'price', 'status')
    list_display_links = ('id', 'roomId')
    list_per_page = 25


admin.site.register(Room, RoomAdmin)
