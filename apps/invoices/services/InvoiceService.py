from apps.billing.repositories.BillingRepository import BillRepository
from apps.invoices.repositories.InvoiceRepository import InvoiceRepository
from apps.authentication.models.UserModel import User
from apps.invoices.models.InvoiceModel import Invoice
from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist
from apps.billing.models.BillingModel import Bill
from apps.invoices.tasks import generate_invoice_pdf, send_invoice_ready_email

class InvoiceService:
    """
    Service class for handling business logic related to invoices, with exception handling.
    """

    def __init__(self, invoice_repository: InvoiceRepository, bill_repository: BillRepository) -> None:
        """
        Initialize the service with dependency injection for the repository.
        """
        self.invoice_repository = invoice_repository
        self.bill_repository = bill_repository

    def create_invoice(self, user: User, billing_period_start: str, billing_period_end: str, total_amount: float, due_date: str, pdf: Optional[str] = None, bills_ids: Optional[List[int]] = None, status: str = 'unpaid') -> Invoice:
        """
        Create an invoice using the repository.
        """
        bills: Optional[List[Bill]] = None
        if bills_ids:
            for bill_id in bills_ids:
                bill = self.bill_repository.get_bill_by_id(bill_id)
                if bill is not None:
                    bills.append(bill) #type: ignore

        invoice = self.invoice_repository.create_invoice(
            user=user,
            billing_period_start=billing_period_start,
            billing_period_end=billing_period_end,
            total_amount=total_amount,
            due_date=due_date,
            pdf=pdf,
            bills=bills,
            status=status,
        )

        # Generate the PDF asynchronously
        generate_invoice_pdf.delay(invoice.id)

        # Optionally, send email notification (if configured)
        send_invoice_ready_email.delay(user.email, invoice.id)

        return invoice

    def get_user_invoices(self, user: User) -> List[Invoice]:
        """
        Get all invoices for a user.
        """
        return self.invoice_repository.get_invoices_by_user(user)

    def get_all_invoices(self) -> List[Invoice]:
        """
        Get all invoices.
        """
        return self.invoice_repository.get_all_invoices()

    def update_invoice(self, invoice_id: int, **updated_fields) -> Optional[Invoice]:
        """
        Update an invoice by its ID.
        """
        invoice = self.invoice_repository.get_invoice_by_id(invoice_id)
        if invoice:
            return self.invoice_repository.update_invoice(invoice, **updated_fields)
        raise ObjectDoesNotExist(f"Invoice with ID {invoice_id} does not exist.")

    def delete_invoice(self, invoice_id: int) -> bool:
        """
        Delete an invoice by its ID.
        """
        invoice = self.invoice_repository.get_invoice_by_id(invoice_id)
        if invoice:
            return self.invoice_repository.delete_invoice(invoice)
        raise ObjectDoesNotExist(f"Invoice with ID {invoice_id} does not exist.")

    def aggregate_user_invoices(self, user: User) -> float:
        """
        Aggregate total invoice amount for a user.
        """
        return self.invoice_repository.aggregate_user_invoices(user)
