from rest_framework import serializers # type: ignore

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.CharField(default='customer')

    def validate_username(self, value):
        """
        Additional custom validation for the username can be done here.
        """
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        return value
    


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    def validate(self, data):
        """
        You can add any custom validation logic here, such as ensuring the username is unique.
        """
        if not data:
            raise serializers.ValidationError("No fields to update.")
        return data


class UserDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        fields = ['id', 'username', 'email', 'date_joined']



