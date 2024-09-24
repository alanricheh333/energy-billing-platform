from typing import Optional, List, Type, cast
from apps.consumption.models.ConsumptionModel import Consumption
from apps.authentication.models.UserModel import User
from django.db.models import Sum

class ConsumptionRepository:
    """
    Repository class for handling consumption-related database operations.
    """

    def __init__(self, consumption_model: Optional[Type[Consumption]] = None, user_model: Optional[Type[User]] = None) -> None:
        """
        Initializes the ConsumptionRepository.

        Args:
            consumption_model (Optional[Type[Consumption]]): The consumption model to use. Defaults to the project's Consumption model.
            user_model (Optional[Type[User]]): The user model to use. Defaults to the project's User model.
        """
        self.consumption_model: Type[Consumption] = consumption_model or Consumption
        self.user_model: Type[User] = user_model or User
        

    def create_consumption(self, user: User, date: str, consumption: float, unit: str = 'kWh') -> Consumption:
        """
        Creates a new consumption record for a user.
        Args:
            user (User): The user for whom the consumption is being recorded.
            date (str): The date of the consumption.
            consumption (float): The energy consumed.
            unit (str, optional): The unit of measurement. Defaults to 'kWh'.
        Returns:
            Consumption: The created consumption record.
        """
        return Consumption.objects.create(user=user, date=date, consumption=consumption, unit=unit)

    def get_consumption_by_id(self, consumption_id: int) -> Optional[Consumption]:
        """
        Retrieves a consumption record by its ID.
        Args:
            consumption_id (int): The ID of the consumption record.
        Returns:
            Optional[Consumption]: The consumption record if found, otherwise None.
        """
        try:
            return Consumption.objects.get(id=consumption_id)
        except Consumption.DoesNotExist:
            return None

    def get_consumption_by_user(self, user: User) -> List[Consumption]:
        """
        Retrieves all consumption records for a specific user.
        Args:
            user (User): The user whose consumption records are being retrieved.
        Returns:
            List[Consumption]: A list of consumption records for the user.
        """
        return list(Consumption.objects.filter(user=user).order_by('-date'))

    def get_all_consumption(self) -> List[Consumption]:
        """
        Retrieves all consumption records.
        Returns:
            List[Consumption]: A list of all consumption records.
        """
        return list(Consumption.objects.all().order_by('-date'))

    def update_consumption(self, consumption: Consumption, **updated_fields) -> Consumption:
        """
        Updates a consumption record with new fields.
        Args:
            consumption (Consumption): The consumption record to update.
            **updated_fields: The fields to update on the consumption record.
        Returns:
            Consumption: The updated consumption record.
        """
        for field, value in updated_fields.items():
            setattr(consumption, field, value)
        consumption.save()
        return consumption

    def delete_consumption(self, consumption: Consumption) -> bool:
        """
        Deletes a consumption record.
        Args:
            consumption (Consumption): The consumption record to delete.
        Returns:
            bool: True if the consumption was deleted, otherwise False.
        """
        consumption.delete()
        return True

    def aggregate_user_consumption(self, user: User) -> float:
        """
        Aggregates total consumption for a specific user.
        Args:
            user (User): The user whose total consumption is being aggregated.
        Returns:
            float: The total consumption for the user.
        """
        return Consumption.objects.filter(user=user).aggregate(Sum('consumption'))['consumption__sum'] or 0.0

    def aggregate_all_users_consumption(self) -> float:
        """
        Aggregates total consumption across all users.
        Returns:
            float: The total consumption for all users.
        """
        return Consumption.objects.aggregate(Sum('consumption'))['consumption__sum'] or 0.0
