from rest_framework import serializers # type: ignore
from apps.invoices.models.InvoiceModel import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Invoice model, used for validating and serializing invoice data.
    """
    is_overdue = serializers.ReadOnlyField()  # Expose the is_overdue property in the API

    class Meta:
        model = Invoice
        fields = ['id', 'user', 'billing_period_start', 'billing_period_end', 'total_amount', 'due_date', 'pdf', 'status', 'created_at', 'bills', 'is_overdue']
        read_only_fields = ['user', 'created_at', 'is_overdue']

    def validate_total_amount(self, value: float) -> float:
        """
        Ensure that the total amount is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Total amount must be a positive number.")
        return value
