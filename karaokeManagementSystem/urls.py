"""karaokeManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from accounts import views as accounts_views
from rooms import views as rooms_views

router = routers.DefaultRouter()
# router.register(r'users', accounts_views.UserViewSet)
router.register(r'schedules', accounts_views.ScheduleViewSet)
router.register(r'products', rooms_views.ProductViewSet)
router.register(r'categories', rooms_views.CategoryViewSet)
# router.register(r'payments', rooms_views.PaymentViewSet)
router.register(r'rooms', rooms_views.RoomViewSet)
router.register(r'weeklySchedules', accounts_views.WeeklyScheduleViewSet)

"""
Get all 
"""
# router.register(r'users', accounts_views.UserViewSet)
router.register(r'allSchedules', accounts_views.AllScheduleViewSet)
router.register(r'allProducts', rooms_views.AllProductViewSet)
router.register(r'allCategories', rooms_views.AllCategoryViewSet)
# router.register(r'payments', rooms_views.PaymentViewSet)
router.register(r'allRooms', rooms_views.AllRoomViewSet)
router.register(r'allUsers', accounts_views.AllUserViewSet)
router.register(r'allPayments', rooms_views.AllPaymentViewSet)
router.register(r'allWeeklySchedules', accounts_views.AllWeeklyScheduleViewSet)

urlpatterns = [
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
