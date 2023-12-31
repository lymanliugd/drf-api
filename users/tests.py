import copy, pytest

from http import HTTPStatus

from django.contrib.auth.models import User
from django.urls import resolve, reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

user_data: dict = {
    'username': 'user1',
    'email': 'user1@test.com',
    'password': '111',
    'first_name': 'first',
    'last_name': 'last',
}

class TestUsersUrls:  # unit tests
    """Test the app users api urls"""

    def test_note_list_and_create_note(self) -> None:
        """Ensure user signup url are defined."""
        path = '/api/auth/signup'
        assert reverse('users:user-signup') == path
        assert resolve(path).view_name == 'users:user-signup'

    def test_get_and_update_a_note(self) -> None:
        """Ensure user login url are defined."""
        path = '/api/auth/login'
        assert reverse('users:user-login') == path
        assert resolve(path).view_name == 'users:user-login'

@pytest.mark.django_db()
class TestUsersApiView:  # integration tests
    """Test the apis for UsersApiView"""

    def test_user_signup(self, api_client: APIClient) -> None:
        """Test the api user signup."""
        response = api_client.post(
            reverse('users:user-signup'),
            data=user_data,
            format='json',
        )

        user = User.objects.get(username=user_data['username'])
        token = Token.objects.get(user=user)
        assert response.status_code == HTTPStatus.OK
        assert user.email == user_data['email']
        assert user.check_password(user_data['password'])
        assert user.first_name == user_data['first_name']
        assert user.last_name == user_data['last_name']
        assert token

    def test_user_signup_failed_without_username(self, api_client: APIClient) -> None:
        """Test the api user signup failed without username."""
        data = copy.deepcopy(user_data)
        del data['username']
        response = api_client.post(
            reverse('users:user-signup'),
            data=data,
            format='json',
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert str(response.data) == '{0}'.format(
            "{'username': [ErrorDetail(string='This field is required.', code='required')]}",
        )

    def test_user_login(self, api_client: APIClient) -> None:
        """Test the api user login."""
        user = User.objects.create(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
        )
        user.set_password(user_data['password'])
        user.save()
        token = Token.objects.create(
            user=user
        )
        token.save()

        # test login with username and password
        response = api_client.post(
            reverse('users:user-login'),
            data={
                'username': user_data['username'],
                'password': user_data['password'],
            },
            format='json',
        )
        assert response.status_code == HTTPStatus.OK
        assert response.data['token'] == token.key

        # test login with email and password
        response = api_client.post(
            reverse('users:user-login'),
            data={
                'email': user_data['email'],
                'password': user_data['password'],
            },
            format='json',
        )
        assert response.status_code == HTTPStatus.OK
        assert response.data['token'] == token.key

    def test_user_login_without_password(self, api_client: APIClient) -> None:
        """Test the api user login failed without password."""

        user = User.objects.create(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
        )
        user.set_password(user_data['password'])
        user.save()
        token = Token.objects.create(
            user=user
        )
        token.save()

        # test login with username and password
        response = api_client.post(
            reverse('users:user-login'),
            data={
                'username': user_data['username'],
            },
            format='json',
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert str(response.data) == '{0}'.format(
            "{'password': [ErrorDetail(string='This field is required.', code='required')]}",
        )