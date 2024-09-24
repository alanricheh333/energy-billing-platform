from typing import Optional, List, Type
from apps.invoices.models.InvoiceModel import Invoice
from apps.authentication.models.UserModel import User
from apps.billing.models.BillingModel import Bill
from django.db.models import Sum

class InvoiceRepository:
    """
    Repository class for handling invoice-related database operations.
    """

    def __init__(self, invoice_model: Optional[Type[Invoice]] = None) -> None:
        """
        Initializes the InvoiceRepository with the specified invoice model.
        """
        self.invoice_model: Type[Invoice] = invoice_model or Invoice

    def create_invoice(self, user: User, billing_period_start: str, billing_period_end: str, total_amount: float, due_date: str, pdf: Optional[str] = None, bills: Optional[List[Bill]] = None, status: str = 'unpaid') -> Invoice:
        """
        Creates a new invoice for a user, based on the billing period and amount.
        """
        invoice = self.invoice_model.objects.create(
            user=user,
            billing_period_start=billing_period_start,
            billing_period_end=billing_period_end,
            total_amount=total_amount,
            due_date=due_date,
            pdf=pdf,
            status=status,
        )
        if bills:
            invoice.bills.set(bills)
        invoice.save()
        return invoice

    def get_invoice_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """
        Retrieves an invoice by its ID.
        """
        try:
            return self.invoice_model.objects.get(id=invoice_id)
        except self.invoice_model.DoesNotExist:
            return None

    def get_invoices_by_user(self, user: User) -> List[Invoice]:
        """
        Retrieves all invoices for a specific user.
        """
        return list(self.invoice_model.objects.filter(user=user).order_by('-created_at'))

    def get_all_invoices(self) -> List[Invoice]:
        """
        Retrieves all invoices.
        """
        return list(self.invoice_model.objects.all().order_by('-created_at'))

    def update_invoice(self, invoice: Invoice, **updated_fields) -> Invoice:
        """
        Updates an invoice with new fields.
        """
        for field, value in updated_fields.items():
            setattr(invoice, field, value)
        invoice.save()
        return invoice

    def delete_invoice(self, invoice: Invoice) -> bool:
        """
        Deletes an invoice.
        """
        invoice.delete()
        return True

    def aggregate_user_invoices(self, user: User) -> float:
        """
        Aggregates total invoice amount for a specific user.
        """
        return self.invoice_model.objects.filter(user=user).aggregate(Sum('total_amount'))['total_amount__sum'] or 0.0
