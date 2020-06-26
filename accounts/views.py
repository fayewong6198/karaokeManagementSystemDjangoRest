from .models import User, Schedule, WeeklySchedule
from rest_framework import viewsets, generics, mixins, views, filters
from rest_framework import permissions
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ScheduleSerializer, WeeklyScheduleSerializer, CreateWeeklyScheduleSerializer
from rest_framework.response import Response
from knox.models import AuthToken
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from .pagination import StandardResultsSetPagination, PaginationHandlerMixin, LargeResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status


class ListCreateUserViewSet(views.APIView, PaginationHandlerMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-created_at')

    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method in ['POST']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        instance = User.objects.all().order_by('-created_at')

        sort_by = request.query_params.get('ordering')

        my_model_fields = [field.name for field in User._meta.get_fields()]
        print(my_model_fields)
        if sort_by and sort_by[1:] in my_model_fields or sort_by in my_model_fields:
            instance = instance.order_by(sort_by)

        if 'search' in request.query_params:
            search = request.query_params.get('search')
            instance = instance.filter(username__icontains=search)

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(UserSerializer(page,
                                                                    many=True).data)
        else:
            serializer = UserSerializer(
                instance, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        print("----------------------------------------------")
        print(request.user)

        serializer_class = RegisterSerializer
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.is_staff = request.data['is_staff']
        user = serializer.save()
        user.save()
        AuthToken.objects.create(user)[1]

        # Create schedule for user
        if 'schedules' in request.data:
            for schedule in request.data["schedules"]:

                schedule["staff"] = user.id
                schedule_serializer = ScheduleSerializer(data=schedule)
                schedule_serializer.is_valid(raise_exception=True)
                new_schedule = schedule_serializer.save()

        return Response({
            'user': UserSerializer(user).data
        })


class RetriveUserViewSet(views.APIView, PaginationHandlerMixin):

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

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

        # Check duplicate schedule
        for schedule in request.data["schedules"]:
            count = 0
            for schedule_2 in request.data["schedules"]:
                if schedule['workingTime'] == schedule_2['workingTime'] and schedule['weekDay'] == schedule_2['weekDay']:
                    count = count + 1
                if count == 2:
                    return Response({'Schedule': [{"Schedule already exits"}]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LargeResultsSetPagination

    # Explicitly specify which fields the API may be ordered against

    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter)

    ordering = ['-created_at']


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter)

    def get_permissions(self):
        print(self.action)
        if self.action in ['update', 'destroy', 'create']:
            permission_classes = [permissions.IsAdminUser, ]
        else:
            permission_classes = [permissions.IsAuthenticated, ]

        return [permission() for permission in permission_classes]

    # Explicitly specify which fields the API may be ordered against

    search_fields = ['weekDay', 'workingTime']
    filterset_fields = ['weekDay', 'workingTime']
    # This will be used as the default ordering
    # This will be used as the default ordering
    ordering = ['-created_at']

    def create(self, request):
        print(request.data)
        user = get_object_or_404(User, pk=request.data['staff'])
        user_schedules = Schedule.objects.filter(staff=user)
        for user_schedule in user_schedules:
            if user_schedule.workingTime == request.data['workingTime'] and user_schedule.weekDay == request.data['weekDay']:
                return Response({'Schedule': [{"Schedule already exits"}]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        schedule = serializer.save()

        return Response(serializer.data)


class AllScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    # Explicitly specify which fields the API may be ordered against

    # This will be used as the default ordering
    ordering = ['-created_at']


""" 
Weekly Schedule 

"""


class WeeklyScheduleViewSet(viewsets.ModelViewSet):
    queryset = WeeklySchedule.objects.all()
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter)

    def get_permissions(self):
        print(self.action)
        if self.action in ['update', 'destroy', 'create']:
            permission_classes = [permissions.IsAdminUser, ]
        else:
            permission_classes = [permissions.IsAuthenticated, ]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['create']:
            return CreateWeeklyScheduleSerializer
        else:
            print("else")
            return WeeklyScheduleSerializer


class AllWeeklyScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeeklySchedule.objects.all()
    serializer_class = WeeklyScheduleSerializer
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        print("CON CAC")
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid() == False:

            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("before save user")
        user = serializer.save()
        print("save user")
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
