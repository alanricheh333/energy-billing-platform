from rest_framework import serializers # type: ignore
from apps.billing.models.BillingModel import Bill

class BillSerializer(serializers.ModelSerializer):
    """
    Serializer for the Bill model, used for validating and serializing billing data.
    """
    class Meta:
        model = Bill
        fields = ['id', 'user', 'date', 'amount', 'status']
        read_only_fields = ['user']

    def validate_amount(self, value: float) -> float:
        """
        Ensure that the amount is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Amount must be a positive number.")
        return value
