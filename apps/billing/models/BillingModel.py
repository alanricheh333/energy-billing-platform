from django.db import models
from apps.authentication.models.UserModel import User
from apps.consumption.models.ConsumptionModel import Consumption
from typing import Optional

class Bill(models.Model):
    """
    Model to represent a billing record for a user.
    """
    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bills')
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    consumption = models.ManyToManyField(Consumption, related_name='bills', blank=True)

    def __str__(self) -> str:
        return f'Bill {self.id} for {self.user.username} on {self.date}: {self.amount} USD ({self.status})' #type: ignore
