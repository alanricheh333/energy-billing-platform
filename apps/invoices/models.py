from django.db import models

from django.conf import settings
from django.db import models

class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    billing_period_start = models.DateField()
    billing_period_end = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pdf = models.FileField(upload_to='invoices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Invoice {self.id} for {self.user.username}'
