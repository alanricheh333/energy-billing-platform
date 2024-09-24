from typing import Optional, List, Type
from apps.billing.models.BillingModel import Bill
from apps.authentication.models.UserModel import User
from django.db.models import Sum

class BillRepository:
    """
    Repository class for handling billing-related database operations.
    """

    def __init__ (self, bill_model: Optional[Type[Bill]] = None) -> None:
        """
        Initializes the BillRepository with the specified bill model.

        Args:
            bill_model (Optional[Type[Bill]]): The bill model to use. Defaults to the project's Bill model.
        """
        self.bill_model: Type[Bill] = bill_model or Bill


    def create_bill(self, user: User, date: str, amount: float, status: str = 'unpaid') -> Bill:
        """
        Creates a new bill for a user.
        
        Args:
            user (User): The user for whom the bill is created.
            date (str): The date of the bill.
            amount (float): The amount due.
            status (str, optional): The status of the bill. Defaults to 'unpaid'.
        
        Returns:
            Bill: The created bill instance.
        """
        return self.bill_model.objects.create(user=user, date=date, amount=amount, status=status)

    def get_bill_by_id(self, bill_id: int) -> Optional[Bill]:
        """
        Retrieves a bill by its ID.
        
        Args:
            bill_id (int): The ID of the bill.
        
        Returns:
            Optional[Bill]: The bill instance if found, else None.
        """
        try:
            return self.bill_model.objects.get(id=bill_id)
        except self.bill_model.DoesNotExist:
            return None

    def get_bills_by_user(self, user: User) -> List[Bill]:
        """
        Retrieves all bills for a specific user.
        
        Args:
            user (User): The user whose bills are being retrieved.
        
        Returns:
            List[Bill]: A list of bills for the user.
        """
        return list(self.bill_model.objects.filter(user=user).order_by('-date'))

    def get_all_bills(self) -> List[Bill]:
        """
        Retrieves all bills.
        
        Returns:
            List[Bill]: A list of all bills.
        """
        return list(self.bill_model.objects.all().order_by('-date'))

    def update_bill(self, bill: Bill, **updated_fields) -> Bill:
        """
        Updates a bill with new fields.
        
        Args:
            bill (Bill): The bill instance to update.
            **updated_fields: The fields to update.
        
        Returns:
            Bill: The updated bill instance.
        """
        for field, value in updated_fields.items():
            setattr(bill, field, value)
        bill.save()
        return bill

    def delete_bill(self, bill: Bill) -> bool:
        """
        Deletes a bill.
        
        Args:
            bill (Bill): The bill instance to delete.
        
        Returns:
            bool: True if deletion was successful, else False.
        """
        bill.delete()
        return True

    def aggregate_user_billing(self, user: User) -> float:
        """
        Aggregates total billing amount for a specific user.
        
        Args:
            user (User): The user whose total billing is being aggregated.
        
        Returns:
            float: The total billing amount.
        """
        return self.bill_model.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0.0

    def aggregate_all_users_billing(self) -> float:
        """
        Aggregates total billing amount across all users.
        
        Returns:
            float: The total billing amount.
        """
        return self.bill_model.objects.aggregate(Sum('amount'))['amount__sum'] or 0.0
