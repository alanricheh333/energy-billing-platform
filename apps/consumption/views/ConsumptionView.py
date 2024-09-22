from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from drf_yasg.utils import swagger_auto_schema # type: ignore
from drf_yasg import openapi # type: ignore
from rest_framework.permissions import IsAuthenticated, IsAdminUser # type: ignore
from apps.consumption.services.ConsumptionService import ConsumptionService
from apps.consumption.repositories.ConsumptionRepository import ConsumptionRepository
from apps.consumption.serializers.ConsumptionSerializers import ConsumptionSerializer
from django.db import IntegrityError
from typing import Optional
from apps.authentication.models.UserModel import User


class ConsumptionView(APIView):
    """
    Handles user-specific consumption data and admin access for viewing all users' data and aggregation.
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, consumption_service: Optional[ConsumptionService] = None, **kwargs):
        super().__init__(**kwargs)
        self.consumption_service = consumption_service or ConsumptionService(ConsumptionRepository())

    @swagger_auto_schema(
        responses={200: ConsumptionSerializer(many=True)},
    )
    def get(self, request):
        """
        - Users: Return consumption records for the logged-in user.
        - Admins: Return all users' consumption records.
        """
        try:
            if request.user.is_staff:
                consumptions = self.consumption_service.get_all_consumptions()  # Admin: All users
            else:
                consumptions = self.consumption_service.get_user_consumptions(request.user)  # User: Their own records
            return Response(ConsumptionSerializer(consumptions, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=ConsumptionSerializer,
        responses={201: ConsumptionSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        """
        Create a new consumption record for the logged-in user.
        """
        serializer = ConsumptionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                consumption = self.consumption_service.create_consumption(
                    user=request.user,
                    date=serializer.validated_data['date'],
                    consumption=serializer.validated_data['consumption'],
                    unit=serializer.validated_data.get('unit', 'kWh')
                )
                return Response(ConsumptionSerializer(consumption).data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminAggregationView(APIView):
    """
    Handles consumption data aggregation for admins.
    """
    permission_classes = [IsAdminUser]  # Only accessible to admins

    def __init__(self, consumption_service: Optional[ConsumptionService] = None, **kwargs):
        super().__init__(**kwargs)
        self.consumption_service = consumption_service or ConsumptionService(ConsumptionRepository())

    @swagger_auto_schema(
        responses={200: openapi.Response('Total consumption across all users', openapi.Schema(type=openapi.TYPE_NUMBER))}
    )
    def get(self, request):
        """
        Admins: Aggregate total consumption across all users.
        """
        try:
            total_consumption = self.consumption_service.aggregate_all_users_consumption()
            return Response({'total_consumption': total_consumption}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminUserAggregationView(APIView):
    """
    Handles consumption aggregation for a specific user (Admin access only).
    """
    permission_classes = [IsAdminUser]

    def __init__(self, consumption_service: Optional[ConsumptionService] = None, **kwargs):
        super().__init__(**kwargs)
        self.consumption_service = consumption_service or ConsumptionService(ConsumptionRepository())

    @swagger_auto_schema(
        responses={200: openapi.Response('Total consumption for the user', openapi.Schema(type=openapi.TYPE_NUMBER))}
    )
    def get(self, request, user_id: int):
        """
        Admins: Aggregate total consumption for a specific user.
        """
        try:
            user = User.objects.get(id=user_id)
            total_consumption = self.consumption_service.aggregate_user_consumption(user)
            return Response({'total_consumption': total_consumption}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": f"User with ID {user_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
