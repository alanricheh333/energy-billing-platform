from django.urls import path
from .views.InvoiceView import InvoiceView, InvoiceDetailView # type: ignore

urlpatterns = [
    path('user/', InvoiceView.as_view(), name='user-invoice-list'),  # GET, POST
    path('user/<int:invoice_id>/', InvoiceDetailView.as_view(), name='user-invoice-detail'),  # GET, PUT, DELETE
]
