from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from drf_yasg.utils import swagger_auto_schema # type: ignore
from rest_framework.permissions import IsAuthenticated, IsAdminUser # type: ignore
from apps.billing.repositories.BillingRepository import BillRepository
from apps.invoices.services.InvoiceService import InvoiceService
from apps.invoices.repositories.InvoiceRepository import InvoiceRepository
from apps.invoices.serializers.InvoiceSerializer import InvoiceSerializer
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional

class InvoiceView(APIView):
    """
    Handles user-specific invoice data.
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, invoice_service: Optional[InvoiceService] = None, **kwargs):
        """
        Dependency injection for InvoiceService.
        """
        super().__init__(**kwargs)
        self.invoice_service = invoice_service or InvoiceService(InvoiceRepository(), bill_repository=BillRepository())

    @swagger_auto_schema(
        responses={200: InvoiceSerializer(many=True)},
    )
    def get(self, request):
        """
        Returns the invoices for the logged-in user.
        """
        try:
            user = request.user
            invoices = self.invoice_service.get_user_invoices(user)
            return Response(InvoiceSerializer(invoices, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=InvoiceSerializer,
        responses={201: InvoiceSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        """
        Create a new invoice for the logged-in user.
        """
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                invoice = self.invoice_service.create_invoice(
                    user=request.user,
                    billing_period_start=serializer.validated_data['billing_period_start'],
                    billing_period_end=serializer.validated_data['billing_period_end'],
                    total_amount=serializer.validated_data['total_amount'],
                    due_date=serializer.validated_data['due_date'],
                    pdf=serializer.validated_data.get('pdf', None),
                    bills=serializer.validated_data.get('bills', None),
                    status=serializer.validated_data.get('status', 'unpaid')
                )
                return Response(InvoiceSerializer(invoice).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceDetailView(APIView):
    """
    Handles retrieving, updating, and deleting a specific invoice for the logged-in user.
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, invoice_service: Optional[InvoiceService] = None, **kwargs):
        """
        Dependency injection for InvoiceService.
        """
        super().__init__(**kwargs)
        self.invoice_service = invoice_service or InvoiceService(InvoiceRepository(), bill_repository=BillRepository())

    @swagger_auto_schema(
        responses={200: InvoiceSerializer},
    )
    def get(self, request, invoice_id: int):
        """
        Retrieve a specific invoice for the logged-in user.
        """
        try:
            invoice = self.invoice_service.get_user_invoices(request.user)[0]
            if not invoice:
                raise ObjectDoesNotExist(f"Invoice with ID {invoice_id} not found.")
            return Response(InvoiceSerializer(invoice).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=InvoiceSerializer,
        responses={200: InvoiceSerializer, 400: "Bad Request"}
    )
    def put(self, request, invoice_id: int):
        """
        Update a specific invoice for the logged-in user.
        """
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                invoice = self.invoice_service.update_invoice(invoice_id, **serializer.validated_data)
                return Response(InvoiceSerializer(invoice).data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: "No Content"},
    )
    def delete(self, request, invoice_id: int):
        """
        Delete a specific invoice for the logged-in user.
        """
        try:
            if self.invoice_service.delete_invoice(invoice_id):
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise ObjectDoesNotExist(f"Invoice with ID {invoice_id} not found.")
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
