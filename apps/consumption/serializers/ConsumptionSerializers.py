from rest_framework import serializers # type: ignore
from apps.consumption.models.ConsumptionModel import Consumption

class ConsumptionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Consumption model, used for validating and serializing consumption data.
    """
    class Meta:
        model = Consumption
        fields = ['id', 'user', 'date', 'consumption', 'unit']
        read_only_fields = ['user']  # We will automatically assign the user in the views

    def validate_consumption(self, value):
        """
        Ensure that the consumption value is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Consumption must be a positive number.")
        return value