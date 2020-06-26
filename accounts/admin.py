from django.contrib import admin

# Register your models here.
from .models import User, Schedule, WeeklySchedule, WeeklySalary


class ScheduleInline(admin.StackedInline):
    model = Schedule
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline, ]
    list_display = ('id', 'username', 'email', 'monthly_salary')
    list_display_links = ('id', 'username')
    list_per_page = 25


admin.site.register(User, UserAdmin)
admin.site.register(Schedule)

admin.site.register(WeeklySchedule)


class WeeklySalaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'weeklySchedule')


admin.site.register(WeeklySalary, WeeklySalaryAdmin)
