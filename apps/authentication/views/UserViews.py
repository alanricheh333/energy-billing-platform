from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from drf_yasg.utils import swagger_auto_schema # type: ignore
from drf_yasg import openapi # type: ignore
from ..serializers.UserSerializers import UserRegistrationSerializer, UserDetailSerializer, UserLoginSerializer # type: ignore
from ..services.UserService import AuthService # type: ignore
from apps.authentication.repositories.UserRepository import UserRepository # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore



class RegisterView(APIView):
    """
    Handles customer registration.
    """
    
    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={201: UserDetailSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user_repository = UserRepository()
            auth_service = AuthService(user_repository)
            user = auth_service.register_customer(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                email=serializer.validated_data.get('email')
            )
            return Response(UserDetailSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AdminRegisterView(APIView):
    """
    Admin-only endpoint for creating users (both customers and admins).
    """
    
    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={201: UserDetailSerializer, 403: "Forbidden", 400: "Bad Request"}
    )
    def post(self, request):
        current_user = request.user
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid() and current_user.is_staff:
            user_repository = UserRepository()
            auth_service = AuthService(user_repository)
            user = auth_service.register_user_by_admin(
                current_user=current_user,
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                email=serializer.validated_data.get('email'),
                role=serializer.validated_data['role'],
            )
            return Response(UserDetailSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Handles user login.
    """

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={200: openapi.Response('Login successful'), 401: 'Unauthorized'}
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user_repository = UserRepository()
            auth_service = AuthService(user_repository)
            user = auth_service.authenticate_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
    """
    View and update the profile of the currently logged-in user.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: UserDetailSerializer, 404: 'User not found'}
    )
    def get(self, request):
        user_repository = UserRepository()
        user = user_repository.get_user_by_id(request.user.id)
        if user:
            return Response(UserDetailSerializer(user).data)
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,  # You can also create a specific update serializer
        responses={200: UserDetailSerializer, 400: 'Bad Request'}
    )
    def put(self, request):
        serializer = UserRegistrationSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            user_repository = UserRepository()
            auth_service = AuthService(user_repository)
            user = auth_service.update_user(
                user_id=request.user.id,
                **serializer.validated_data
            )
            return Response(UserDetailSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserManagementView(APIView):
    """
    Admin-only view for updating and deleting users.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={200: UserDetailSerializer, 403: 'Forbidden', 404: 'Not found'}
    )
    def put(self, request, user_id):
        current_user = request.user
        serializer = UserRegistrationSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            user_repository = UserRepository()
            auth_service = AuthService(user_repository)
            user = auth_service.update_user(
                current_user=current_user,
                user_id=user_id,
                **serializer.validated_data
            )
            return Response(UserDetailSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: 'No Content', 403: 'Forbidden', 404: 'Not found'}
    )
    def delete(self, request, user_id):
        current_user = request.user
        user_repository = UserRepository()
        auth_service = AuthService(user_repository)
        success = auth_service.delete_user(current_user, user_id)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
