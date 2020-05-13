from .models import Room
from rest_framework import serializers


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'roomId', 'price', 'status', 'created_at']
