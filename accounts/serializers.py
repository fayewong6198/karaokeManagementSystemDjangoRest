from .models import User, Schedule, WeeklySchedule
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.response import Response


class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ['id', 'staff', 'weekDay', 'workingTime']


class InlineScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['weekDay', 'workingTime']


class InlineScheduleSerializerWeekly(serializers.ModelSerializer):
    class Meta:
        model = Schedule,
        fields = ['weekDay', 'workingTime', 'user']


class WeeklyScheduleSerializer(serializers.ModelSerializer):
    schedules = InlineScheduleSerializerWeekly(many=True)

    class Meta:
        model = WeeklySchedule
        fields = ['id', 'start', 'schedules']


class CreateWeeklyScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeeklySchedule
        fields = ['id', 'start']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    schedules = InlineScheduleSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'gender', 'monthly_salary', 'salary',
                  'role', 'schedules', 'is_staff', 'created_at']

    def update(self, instance, validated_data):
        instance.username = validated_data.get(
            'username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)

        return instance


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])
        print(validated_data)
        if 'is_staff' in validated_data:
            print("DIT ME MAY")
            user.is_staff = validated_data['is_staff']
            print(user.is_staff)

        return user

# Login Serializer


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
