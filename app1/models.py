from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    profile_picture = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.username
