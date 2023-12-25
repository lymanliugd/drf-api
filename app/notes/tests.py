import pytest
from http import HTTPStatus

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase

from notes.models import Note

# pytestmark = pytest.mark.django_db(databases=['default'])

# import environ
# env = environ.Env()
# environ.Env.read_env()
# import os


class TestNoteApiView(APITestCase):

    @pytest.mark.django_db
    def test_aaa(self, api_client: APIClient, user: User) -> None:
        # user = User(username='bbb', password='111')
        # note = Note(user=user, content='ttt')

        # print(note.content)
        # assert note.content == 'ttt'
        # print(env('SECRET_KEY'))
        assert 1 == 1

    # def test_get_one_note(self, api_client: APIClient, admin_user: User) -> None:
    #     api_client.force_login(user=admin_user)
    #     note = Note(user=admin_user, content='ttt')

    #     response = api_client.get(reverse('api:app-note', kwargs={'id': admin_user.id}))

    #     print(admin_user.id)
    #     print(response.data)
    #     assert response.data['content'] == note.content
    #     assert response.status_code == HTTPStatus.OK
    
    
