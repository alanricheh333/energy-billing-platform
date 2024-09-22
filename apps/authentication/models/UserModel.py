from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore
from typing import Literal

class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    def save(self, *args, **kwargs):
        # Ensure that users with the 'admin' role have admin privileges
        if self.role == 'admin':
            self.is_staff = True
            self.is_superuser = True  # You can adjust this depending on your admin logic
        super().save(*args, **kwargs)
