from apps.consumption.repositories.ConsumptionRepository import ConsumptionRepository
from apps.authentication.models.UserModel import User
from apps.consumption.models.ConsumptionModel import Consumption
from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

class ConsumptionService:
    """
    Service class for handling business logic related to energy consumption, with exception handling.
    """

    def __init__(self, consumption_repository: ConsumptionRepository) -> None:
        self.consumption_repository = consumption_repository

    def create_consumption(self, user: User, date: str, consumption: float, unit: str = 'kWh') -> Consumption:
        """
        Create a consumption record using the repository.
        Raises:
            IntegrityError: If the record cannot be created due to database constraints.
        """
        try:
            return self.consumption_repository.create_consumption(user, date, consumption, unit)
        except IntegrityError as e:
            raise IntegrityError(f"Failed to create consumption record for {user.username}: {str(e)}")

    def get_user_consumptions(self, user: User) -> List[Consumption]:
        """
        Get all consumption records for a user.
        """
        return self.consumption_repository.get_consumption_by_user(user)

    def get_all_consumptions(self) -> List[Consumption]:
        """
        Get all consumption records.
        """
        return self.consumption_repository.get_all_consumption()

    def update_consumption(self, consumption_id: int, **updated_fields) -> Optional[Consumption]:
        """
        Update a consumption record by its ID.
        Raises:
            ObjectDoesNotExist: If the consumption record does not exist.
        """
        try:
            consumption = self.consumption_repository.get_consumption_by_id(consumption_id)
            if consumption:
                return self.consumption_repository.update_consumption(consumption, **updated_fields)
            else:
                raise ObjectDoesNotExist(f"Consumption record with ID {consumption_id} does not exist.")
        except ObjectDoesNotExist as e:
            raise ObjectDoesNotExist(f"Failed to update consumption: {str(e)}")

    def delete_consumption(self, consumption_id: int) -> bool:
        """
        Delete a consumption record by its ID.
        Raises:
            ObjectDoesNotExist: If the consumption record does not exist.
        """
        try:
            consumption = self.consumption_repository.get_consumption_by_id(consumption_id)
            if consumption:
                return self.consumption_repository.delete_consumption(consumption)
            else:
                raise ObjectDoesNotExist(f"Consumption record with ID {consumption_id} does not exist.")
        except ObjectDoesNotExist as e:
            raise ObjectDoesNotExist(f"Failed to delete consumption: {str(e)}")

    def aggregate_user_consumption(self, user: User) -> float:
        """
        Aggregate total consumption for a user.
        """
        return self.consumption_repository.aggregate_user_consumption(user)

    def aggregate_all_users_consumption(self) -> float:
        """
        Aggregate total consumption across all users.
        """
        return self.consumption_repository.aggregate_all_users_consumption()
