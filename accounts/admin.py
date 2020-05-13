from django.contrib import admin

# Register your models here.
from .models import User, Schedule


class ScheduleAdmin(admin.ModelAdmin):
    pass


class ScheduleInline(admin.StackedInline):
    model = Schedule
    max_num = 20
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline, ]
    list_display = ('id', 'username', 'email')
    list_display_links = ('id', 'username')
    list_per_page = 25


admin.site.register(User, UserAdmin)
