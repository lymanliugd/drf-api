from rest_framework import serializers

from django.contrib.auth.models import User


class SignupSerializer(serializers.ModelSerializer):
    """Api signup serializer."""

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'email': {'required': True},
        }

# Use custom serializer instead, because of creating non-unique user issue
class LoginSerializer(serializers.Serializer):
    """Api login serializer."""

    username = serializers.CharField(source='user.username', required=False)
    email = serializers.CharField(source='user.email', required=False)
    password = serializers.CharField(source='user.password')

    class Meta:
        fields = ['username', 'password', 'email']
