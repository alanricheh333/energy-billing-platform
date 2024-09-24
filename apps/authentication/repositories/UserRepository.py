from django.db import IntegrityError # type: ignore
from django.core.exceptions import ObjectDoesNotExist # type: ignore
from typing import Optional, Type, Any, cast
from django.contrib.auth import authenticate # type: ignore

from apps.authentication.models.UserModel import User  # Import your custom User model


class UserRepository:
    """
    Repository class for user-related database operations.
    """

    def __init__(self, user_model: Optional[Type[User]] = None) -> None:
        """
        Initializes the UserRepository with the specified user model.

        Args:
            user_model (Optional[Type[User]]): The user model to use. Defaults to the project's User model.
        """
        self.user_model: Type[User] = user_model or User

    def create_user(self, username: str, password: str, email: Optional[str] = None, **extra_fields: Any) -> User:
        """
        Creates a new user with the given username, password, email, and extra fields.

        Args:
            username (str): The username for the new user.
            password (str): The password for the new user.
            email (Optional[str]): The email address for the new user.
            **extra_fields: Additional fields for the user model.

        Returns:
            User: The created user object.

        Raises:
            IntegrityError: If a user with the given username already exists.
        """
        try:
            user: User = self.user_model.objects.create_user(
                username=username,
                password=password,
                email=email,
                **extra_fields
            )
            return user
        except IntegrityError as e:
            raise IntegrityError(f"User with username '{username}' already exists.") from e

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieves a user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            Optional[User]: The user object if found, otherwise None.
        """
        try:
            return self.user_model.objects.get(username=username)
        except ObjectDoesNotExist:
            return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieves a user by their email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            Optional[User]: The user object if found, otherwise None.
        """
        try:
            return self.user_model.objects.get(email=email)
        except ObjectDoesNotExist:
            return None
        
    def get_user_by_id(self, id: int) -> Optional[User]:
        """
        Retrieves a user by their ID.

        Args:
            id (int): The ID of the user to retrieve.

        Returns:
            Optional[User]: The user object if found, otherwise None.
        """
        try:
            return self.user_model.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    def update_user_by_username(self, username: str, **updated_fields: Any) -> Optional[User]:
        """
        Updates an existing user's information by their username.

        Args:
            username (str): The username of the user to update.
            **updated_fields (Any): Fields to update on the user object.

        Returns:
            Optional[User]: The updated user object if the user was found and updated, otherwise None.
        """
        user: Optional[User] = self.get_user_by_username(username)
        if not user:
            return None
        
        for field, value in updated_fields.items():
            setattr(user, field, value)
        user.save()
        return user

    def update_user_by_id(self, user_id: int, **updated_fields: Any) -> Optional[User]:
        """
        Updates an existing user's information by their ID.

        Args:
            user_id (int): The ID of the user to update.
            **updated_fields (Any): Fields to update on the user object.

        Returns:
            Optional[User]: The updated user object if the user was found and updated, otherwise None.
        """
        try:
            user: User = self.user_model.objects.get(id=user_id)
            for field, value in updated_fields.items():
                setattr(user, field, value)
            user.save()
            return user
        except ObjectDoesNotExist:
            return None

    def delete_user_by_username(self, username: str) -> bool:
        """
        Deletes a user by their username.

        Args:
            username (str): The username of the user to delete.

        Returns:
            bool: True if the user was successfully deleted, False if the user was not found.
        """
        user: Optional[User] = self.get_user_by_username(username)
        if user:
            user.delete()
            return True
        return False

    def delete_user_by_id(self, user_id: int) -> bool:
        """
        Deletes a user by their ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if the user was successfully deleted, False if the user was not found.
        """
        try:
            user: User = self.user_model.objects.get(id=user_id)
            user.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticates a user with the given username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            Optional[User]: The authenticated user if credentials are valid, otherwise None.
        """
        user: Optional[User] = cast(Optional[User], authenticate(username=username, password=password))
        return user
