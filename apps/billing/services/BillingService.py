from apps.billing.repositories.BillingRepository import BillRepository
from apps.authentication.models.UserModel import User
from apps.billing.models.BillingModel import Bill
from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist

class BillService:
    """
    Service class for handling business logic related to billing, with exception handling.
    """

    def __init__(self, bill_repository: BillRepository) -> None:
        """
        Initialize the service with dependency injection for the repository.
        """
        self.bill_repository = bill_repository

    def create_bill(self, user: User, date: str, amount: float, status: str = 'unpaid') -> Bill:
        """
        Create a billing record using the repository.
        
        Returns:
            Bill: The created bill instance.
        """
        return self.bill_repository.create_bill(user=user, date=date, amount=amount, status=status)

    def get_user_bills(self, user: User) -> List[Bill]:
        """
        Get all billing records for a user.
        
        Returns:
            List[Bill]: A list of bills for the user.
        """
        return self.bill_repository.get_bills_by_user(user)

    def get_all_bills(self) -> List[Bill]:
        """
        Get all billing records.
        
        Returns:
            List[Bill]: A list of all bills.
        """
        return self.bill_repository.get_all_bills()

    def update_bill(self, bill_id: int, **updated_fields) -> Optional[Bill]:
        """
        Update a billing record by its ID.
        
        Raises:
            ObjectDoesNotExist: If the bill does not exist.
        
        Returns:
            Optional[Bill]: The updated bill instance if successful, else None.
        """
        bill = self.bill_repository.get_bill_by_id(bill_id)
        if bill:
            return self.bill_repository.update_bill(bill, **updated_fields)
        raise ObjectDoesNotExist(f"Bill with ID {bill_id} does not exist.")

    def delete_bill(self, bill_id: int) -> bool:
        """
        Delete a billing record by its ID.
        
        Returns:
            bool: True if deletion was successful, else False.
        """
        bill = self.bill_repository.get_bill_by_id(bill_id)
        if bill:
            return self.bill_repository.delete_bill(bill)
        raise ObjectDoesNotExist(f"Bill with ID {bill_id} does not exist.")

    def aggregate_user_billing(self, user: User) -> float:
        """
        Aggregate total billing amount for a user.
        
        Returns:
            float: The total billing amount.
        """
        return self.bill_repository.aggregate_user_billing(user)

    def aggregate_all_users_billing(self) -> float:
        """
        Aggregate total billing amount across all users.
        
        Returns:
            float: The total billing amount.
        """
        return self.bill_repository.aggregate_all_users_billing()
