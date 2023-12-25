from typing import Any

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import LoginSerializer, SignupSerializer


class LoginApiView(APIView):
    """Login api view"""

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle GET requests from `api/auth/login`.

        Args:
            request: Http request.

        Raises:
            ParseError: If the user or the token does not exist.

        Returns:
            Http response with the toke of the login user.
        """
        serializer = LoginSerializer(data=request.data)
        # Validate received data. Return a 400 response if the data was invalid.
        serializer.is_valid(raise_exception=True)

        user_data = request.data
        password = user_data['password']

        user = None
        if 'username' in user_data:
            username = user_data['username']
            user = authenticate(username=username, password=password)
        elif 'email' in user_data:
            email = user_data['email']
            user = get_object_or_404(User, email=email)
            if not user.check_password(password):
                user = None
        if not user:
            raise serializers.ValidationError(
                'The user does not exist or the password is invalid.',
            )
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            raise serializers.ValidationError(
                'The user does not have a token.',
            )
        return Response({'token': token.key})


class SignupApiView(APIView):
    """Signup api view"""

    def post(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Handle POST requests from `api/auth/signup`.

        Args:
            request: HTTP request
            args: varied amount of non-keyword arguments
            kwargs: varied amount of keyword arguments

        Returns:
            HTTP `Response` with empty info
        """
        serializer = SignupSerializer(data=request.data)
        # Validate received data. Return a 400 response if the data was invalid.
        serializer.is_valid(raise_exception=True)

        user_data = request.data
        username = user_data['username']
        password = user_data['password']
    
        if not 'first_name' in user_data:
            user_data['first_name'] = ''
        elif not 'last_name' in user_data:
            user_data['last_name'] = ''
       
        user = User.objects.create(
            username=username,
            password=password,
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
        )
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return Response()