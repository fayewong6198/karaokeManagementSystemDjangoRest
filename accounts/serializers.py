from .models import User, Schedule
from rest_framework import serializers
from django.contrib.auth import authenticate


class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ['id', 'staff', 'weekDay', 'workingTime']


class InlineScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ['weekDay', 'workingTime']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    schedules = InlineScheduleSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'gender',
                  'role', 'schedules', 'is_staff', 'created_at']

    def update(self, instance, validated_data):
        instance.username = validated_data.get(
            'username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.gender = validated_data.get('gender', instance.gender)

        return instance


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])

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
