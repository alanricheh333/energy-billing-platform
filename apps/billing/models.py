from django.db import models

from django.conf import settings
from django.db import models

from django.db import models

class Rate(models.Model):
    effective_date = models.DateField()
    rate_per_kwh = models.DecimalField(max_digits=6, decimal_places=4)

    def __str__(self):
        return f'Rate from {self.effective_date}: ${self.rate_per_kwh}/kWh'