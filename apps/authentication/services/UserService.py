from apps.authentication.repositories.UserRepository import UserRepository
from apps.authentication.models.UserModel import User
from typing import Optional
from django.core.exceptions import PermissionDenied

class AuthService:
    """
    Service class for authentication and registration-related business logic.
    """

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def register_customer(self, username: str, password: str, email: Optional[str] = None) -> User:
        """
        Allows customers to register themselves.
        
        Args:
            username (str): The username of the new customer.
            password (str): The password of the new customer.
            email (Optional[str]): The email of the new customer.

        Returns:
            User: The created customer user object.
        """
        try:
            user = self.user_repository.create_user(
                username=username,
                password=password,
                email=email
            )
            user.role= 'customer'  # Ensure the new user is a customer
            user.save()
        except:
            raise Exception("User already exists.")
        return user

    def register_user_by_admin(self, current_user: User, username: str, password: str, email: Optional[str] = None, role: str = 'customer') -> User:
        """
        Admins can create both customer and admin users.
        
        Args:
            current_user (User): The admin user making the request.
            username (str): The username of the new user.
            password (str): The password of the new user.
            email (Optional[str]): The email of the new user.
            role (str): The role of the new user ('admin' or 'customer').

        Returns:
            User: The created user object.

        Raises:
            PermissionDenied: If the current user is not an admin.
        """
        if not current_user.is_staff:  # Only admins can create other users
            raise PermissionDenied("Only admins can create users.")

        user = self.user_repository.create_user(
            username=username,
            password=password,
            email=email
        )
        user.role = role
        user.save()
        return user

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticates a user with the given credentials.
        
        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            Optional[User]: The authenticated user if credentials are valid, otherwise None.
        """
        user = self.user_repository.authenticate_user(
            username=username,
            password=password
        )
        return user

    def update_user(self, current_user: User, user_id: int, **updated_fields) -> Optional[User]:
        """
        Updates the user's profile information.
        
        Args:
            current_user (User): The current user making the request (for permission checks).
            user_id (int): The ID of the user to update.
            **updated_fields: The fields to update for the user.

        Returns:
            Optional[User]: The updated user object if found, otherwise None.

        Raises:
            PermissionDenied: If the current user does not have permission to update the user.
        """
        user_to_update = self.user_repository.get_user_by_id(user_id)

        if current_user.is_staff or current_user == user_to_update:  # Admins or the user themselves
            user = self.user_repository.update_user_by_id(user_id, **updated_fields)
            return user
        raise PermissionDenied("You do not have permission to update this user.")

    def delete_user(self, current_user: User, user_id: int) -> bool:
        """
        Deletes a user by their ID.
        
        Args:
            current_user (User): The current user making the request (for permission checks).
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if the user was successfully deleted, False if the user was not found.

        Raises:
            PermissionDenied: If the current user does not have permission to delete the user.
        """
        if not current_user.is_staff:
            raise PermissionDenied("Only admins can delete users.")
        
        return self.user_repository.delete_user_by_id(user_id)
