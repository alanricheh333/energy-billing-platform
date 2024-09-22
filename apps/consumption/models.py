from django.db import models

from django.conf import settings
from django.db import models

class ConsumptionRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    consumption = models.FloatField()  # in kWh

    def __str__(self):
        return f'{self.user.username} - {self.date} - {self.consumption} kWh'
