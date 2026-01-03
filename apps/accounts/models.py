from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        app_label = 'accounts'

    def __str__(self):
        return self.username