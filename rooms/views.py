from .models import Room
from rest_framework import viewsets, mixins
from rest_framework import permissions
from .serializers import RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Room.objects.all().order_by('-created_at')
    serializer_class = RoomSerializer
 #   permission_classes = [permissions.IsAuthenticated]
