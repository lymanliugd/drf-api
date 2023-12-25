from rest_framework import serializers

from django.contrib.auth.models import User


class SignupSerializer(serializers.Serializer):
    """Api signup serializer."""

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'email': {'required': True},
        }


class LoginSerializer(serializers.Serializer):
    """Api login serializer."""

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {
            'password': {'required': True},
        }
