from django.urls import path, include
from .views import RegisterAPI, LoginAPI, UserAPI, ListCreateUserViewSet, RetriveUserViewSet
from knox import views as knox_views
from rooms.views import ListCreatePaymentViewSet, RetrivePaymentViewSet

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view()),
    path('api/users/', ListCreateUserViewSet.as_view()),
    path('api/users/<int:pk>', RetriveUserViewSet.as_view()),
    path('api/payments/<int:pk>', RetrivePaymentViewSet.as_view()),
    path('api/payments/', ListCreatePaymentViewSet.as_view()),
]
