from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from drf_yasg.utils import swagger_auto_schema # type: ignore
from drf_yasg import openapi # type: ignore
from rest_framework.permissions import IsAuthenticated, IsAdminUser # type: ignore
from apps.billing.services.BillingService import BillService
from apps.billing.repositories.BillingRepository import BillRepository
from apps.billing.serializers.BillingSerializer import BillSerializer
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional

class BillView(APIView):
    """
    Handles user-specific billing data.
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, bill_service: Optional[BillService] = None, **kwargs):
        """
        Dependency injection for BillService.
        """
        super().__init__(**kwargs)
        self.bill_service = bill_service or BillService(BillRepository())

    @swagger_auto_schema(
        responses={200: BillSerializer(many=True)},
    )
    def get(self, request):
        """
        Returns the billing records for the logged-in user.
        """
        try:
            user = request.user
            bills = self.bill_service.get_user_bills(user)
            return Response(BillSerializer(bills, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=BillSerializer,
        responses={201: BillSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        """
        Create a new billing record for the logged-in user.
        """
        serializer = BillSerializer(data=request.data)
        if serializer.is_valid():
            try:
                bill = self.bill_service.create_bill(
                    user=request.user,
                    date=serializer.validated_data['date'],
                    amount=serializer.validated_data['amount'],
                    status=serializer.validated_data.get('status', 'unpaid')
                )
                return Response(BillSerializer(bill).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BillDetailView(APIView):
    """
    Handles retrieving, updating, and deleting a specific billing record for the logged-in user.
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, bill_service: Optional[BillService] = None, **kwargs):
        """
        Dependency injection for BillService.
        """
        super().__init__(**kwargs)
        self.bill_service = bill_service or BillService(BillRepository())

    @swagger_auto_schema(
        responses={200: BillSerializer},
    )
    def get(self, request, bill_id: int):
        """
        Retrieve a specific billing record for the logged-in user.
        """
        try:
            bill = self.bill_service.get_user_bills(request.user)[0]
            if not bill:
                raise ObjectDoesNotExist(f"Bill with ID {bill_id} not found.")
            return Response(BillSerializer(bill).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=BillSerializer,
        responses={200: BillSerializer, 400: "Bad Request"}
    )
    def put(self, request, bill_id: int):
        """
        Update a specific billing record for the logged-in user.
        """
        serializer = BillSerializer(data=request.data)
        if serializer.is_valid():
            try:
                bill = self.bill_service.update_bill(bill_id, **serializer.validated_data)
                return Response(BillSerializer(bill).data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: "No Content"},
    )
    def delete(self, request, bill_id: int):
        """
        Delete a specific billing record for the logged-in user.
        """
        try:
            if self.bill_service.delete_bill(bill_id):
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Bill not found."}, status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class AdminAggregationView(APIView):
    """
    Handles billing data aggregation for admins.
    """
    permission_classes = [IsAdminUser]

    def __init__(self, bill_service: Optional[BillService] = None, **kwargs):
        """
        Dependency injection for BillService.
        """
        super().__init__(**kwargs)
        self.bill_service = bill_service or BillService(BillRepository())

    @swagger_auto_schema(
        responses={200: openapi.Response('Total billing across all users', openapi.Schema(type=openapi.TYPE_NUMBER))}
    )
    def get(self, request):
        """
        Admins: Aggregate total billing across all users.
        """
        try:
            total_billing = self.bill_service.aggregate_all_users_billing()
            return Response({'total_billing': total_billing}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
