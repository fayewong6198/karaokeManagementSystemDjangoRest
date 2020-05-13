from django.db import models
from datetime import datetime


class Room(models.Model):
    roomId = models.CharField(max_length=255, unique=True)
    price = models.IntegerField()
    AVAILABLE = 'available'
    NOT_AVAILABLE = 'notAvailable'

    STATUS_CHOICES = (
        (AVAILABLE, 'AVAILABLE'),
        (NOT_AVAILABLE, 'NOT AVAILABLE'),
    )

    status = models.CharField(
        max_length=31,
        choices=STATUS_CHOICES,
        default=AVAILABLE
    )

    created_at = models.DateTimeField(default=datetime.now)
