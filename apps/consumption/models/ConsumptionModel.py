from django.db import models
from apps.authentication.models.UserModel import User
from typing import Optional

class Consumption(models.Model):
    """
    Model to track energy consumption for users.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consumptions')
    date = models.DateField()
    consumption = models.FloatField()
    unit = models.CharField(max_length=10, default='kWh')

    def __str__(self) -> str:
        return f'{self.user.username} - {self.date}: {self.consumption} {self.unit}'
