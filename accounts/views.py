from .models import User, Schedule
from rest_framework import viewsets, generics, mixins, views
from rest_framework import permissions
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ScheduleSerializer
from rest_framework.response import Response
from knox.models import AuthToken
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from .pagination import StandardResultsSetPagination, PaginationHandlerMixin, LargeResultsSetPagination


class ListCreateUserViewSet(views.APIView, PaginationHandlerMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-created_at')

    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        instance = User.objects.all().order_by('-created_at')
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(UserSerializer(page,
                                                                    many=True).data)
        else:
            serializer = UserSerializer(
                instance, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = RegisterSerializer
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        AuthToken.objects.create(user)[1]

        # Create schedule for user
        for schedule in request.data["schedules"]:
            schedule["staff"] = user.id
            schedule_serializer = ScheduleSerializer(data=schedule)
            schedule_serializer.is_valid(raise_exception=True)
            new_schedule = schedule_serializer.save()

        return Response({
            'user': UserSerializer(user).data
        })


class RetriveUserViewSet(views.APIView, PaginationHandlerMixin):

    def get(self, request, format=None, pk=None):
        """
        Return a single user.
        """
        instance = get_object_or_404(User, pk=pk)

        serializer = UserSerializer(instance=instance)
        return Response({'result': serializer.data})

    def put(self, request, format=None, pk=None):
        """
        Update User.
        """
        instance = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        instance.save()
        # Delete old schedule
        Schedule.objects.filter(staff=instance).delete()

        # Update schedule for user
        for schedule in request.data["schedules"]:
            schedule["staff"] = instance.id
            schedule_serializer = ScheduleSerializer(data=schedule)
            schedule_serializer.is_valid(raise_exception=True)
            new_schedule = schedule_serializer.save()

        return Response(UserSerializer(instance=instance).data)

    def delete(selt, request, format=None, pk=None):
        user = get_object_or_404(User, pk=pk)
        print(user)
        user.delete()
        return Response({'msg': 'User deleted'})


class AllUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    pagination_class = LargeResultsSetPagination


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by('-created_at')
    serializer_class = ScheduleSerializer


class AllScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by('-created_at')
    serializer_class = ScheduleSerializer
    pagination_class = LargeResultsSetPagination


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1]
        })


# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1]
        })

# Get User API


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
