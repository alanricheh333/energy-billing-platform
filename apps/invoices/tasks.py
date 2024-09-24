from celery import shared_task # type: ignore
from apps.invoices.models.InvoiceModel import Invoice
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from django.template.loader import render_to_string
from weasyprint import HTML # type: ignore
import os

@shared_task
def generate_invoice_pdf(invoice_id: int) -> str:
    """
    Task to generate a PDF for a given invoice and save the file using WeasyPrint.
    """
    try:
        invoice = Invoice.objects.get(id=invoice_id)

        # Define the HTML content for the PDF (using Django's template engine)
        html_content = render_to_string('templates/invoice_template.html', {'invoice': invoice})

        # Define the path where the PDF will be saved
        pdf_filename = f'invoice_{invoice.id}.pdf'
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'invoices', pdf_filename)

        # Generate the PDF using WeasyPrint
        HTML(string=html_content).write_pdf(pdf_path)

        # Update the invoice model with the PDF path
        invoice.pdf = pdf_filename
        invoice.save()

        return pdf_filename

    except Invoice.DoesNotExist:
        return f"Invoice with ID {invoice_id} does not exist."

@shared_task
def send_invoice_ready_email(user_email: str, invoice_id: int) -> None:
    """
    Task to send an email notifying that the invoice is ready.
    """
    send_mail(
        subject="Your Invoice is Ready",
        message=f"Invoice {invoice_id} has been generated and is ready for viewing.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )
