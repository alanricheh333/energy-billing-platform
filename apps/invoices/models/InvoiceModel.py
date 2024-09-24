from django.db import models
from django.conf import settings
from apps.billing.models.BillingModel import Bill

class Invoice(models.Model):
    """
    Model to represent an invoice for a user, generated based on billing records.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    billing_period_start = models.DateField()
    billing_period_end = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pdf = models.FileField(upload_to='invoices/', blank=True, null=True)
    bills = models.ManyToManyField(Bill, related_name='invoices', blank=True)  # Linking invoices to bills
    status = models.CharField(max_length=10, choices=[('unpaid', 'Unpaid'), ('paid', 'Paid'), ('overdue', 'Overdue')], default='unpaid')  # Status of the invoice
    due_date = models.DateField()  # When the invoice is due
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Invoice {self.id} for {self.user.username}'

    @property
    def is_overdue(self) -> bool:
        """
        Check if the invoice is overdue based on the due date and status.
        """
        from django.utils.timezone import now
        return self.status == 'unpaid' and self.due_date < now().date()
