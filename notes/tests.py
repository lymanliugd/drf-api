from http import HTTPStatus

from django.contrib.auth.models import User
from django.urls import resolve, reverse

from rest_framework.test import APIClient

from notes.models import Note


class TestNotesUrls:  # unit tests
    """Test the app notes api urls"""

    def test_note_list_and_create_note(self) -> None:
        """Ensure note list and create a note urls are defined."""
        path = '/api/notes/'
        assert reverse('notes:notes-notes') == path
        assert resolve(path).view_name == 'notes:notes-notes'

    def test_get_and_update_a_note(self) -> None:
        """Ensure get and update a note urls are defined."""
        path = '/api/notes/123'
        assert reverse('notes:notes-note', kwargs={'id': 123}) == path
        assert resolve(path).view_name == 'notes:notes-note'

    def test_notes_share(self) -> None:
        """Ensure share note url is defined."""
        path = '/api/notes/123/share'
        assert reverse('notes:notes-share', kwargs={'id': 123}) == path
        assert resolve(path).view_name == 'notes:notes-share'

    def test_notes_search(self) -> None:
        """Ensure search note url is defined."""
        path = '/api/search/test'
        assert reverse('notes:notes-search', kwargs={'query': 'test'}) == path
        assert resolve(path).view_name == 'notes:notes-search'


class TestNoteApiView:  # integration tests
    """Test the apis for NoteApiView"""

    def test_create_one_note(self, api_client: APIClient, admin_user: User) -> None:
        """Test the api create one note for a user."""
        api_client.force_login(user=admin_user)

        response = api_client.post(
            reverse('notes:notes-notes'),
            data={'content': 'test1'},
            format='json',
        )

        notes = Note.objects.all().first()
        assert response.status_code == HTTPStatus.OK
        assert response.data == 'Create the note: test1 successfully'
        assert notes.content == 'test1'

    def test_get_one_note(self, api_client: APIClient, admin_user: User) -> None:
        """Test the api get a note with note id for a user."""
        api_client.force_login(user=admin_user)
        note = Note(user=admin_user, content='test1')
        note.save()

        response = api_client.get(reverse('notes:notes-note', kwargs={'id': note.id}))

        assert response.data['content'] == note.content
        assert response.status_code == HTTPStatus.OK

    def test_update_one_note(self, api_client: APIClient, admin_user: User) -> None:
        """Test the api update a note with note id for a user."""
        api_client.force_login(user=admin_user)
        note = Note(user=admin_user, content='test1')
        note.save()

        response = api_client.put(
            reverse('notes:notes-note', kwargs={'id': note.id}),
            data={'content': 'new_test'},
            format='json',
        )

        note.refresh_from_db()
        assert response.status_code == HTTPStatus.OK
        assert response.data == 'Udate note id: 1 successfully'
        assert note.content == 'new_test'

    def test_delete_one_note(self, api_client: APIClient, admin_user: User) -> None:
        """Test the api delete a note with note id for a user."""
        api_client.force_login(user=admin_user)
        note = Note(user=admin_user, content='test1')
        note.save()

        response = api_client.delete(
            reverse('notes:notes-note', kwargs={'id': note.id}),
        )

        notes = Note.objects.all()
        assert response.status_code == HTTPStatus.OK
        assert response.data == 'Delete the note id: 1'
        assert not notes

    def test_share_one_note(self, api_client: APIClient, admin_user: User) -> None:
        """Test the api share a note with a user."""
        api_client.force_login(user=admin_user)
        normal_user = User(username='normal_user')
        normal_user.save()
        note = Note(user=admin_user, content='test1')
        note.save()

        response = api_client.post(
            reverse('notes:notes-share', kwargs={'id': note.id}),
            data={'username': 'normal_user'},
            format='json',
        )

        new_note = Note.objects.filter(user=normal_user).first()
        assert response.status_code == HTTPStatus.OK
        assert new_note.content == note.content

    def test_search_notes(self, api_client: APIClient, admin_user: User) -> None:
        """Test the api search the notes with note keywords."""
        api_client.force_login(user=admin_user)
        note1 = Note(user=admin_user, content='test1')
        note1.save()
        note2 = Note(user=admin_user, content='test2')
        note2.save()

        response = api_client.get(
            reverse('notes:notes-search', kwargs={'query': 'test'}),
        )
        assert response.status_code == HTTPStatus.OK
        assert len(response.data) == 2
        assert response.data[1]['content'] == 'test2'

        response = api_client.get(
            reverse('notes:notes-search', kwargs={'query': 'test1'}),
        )
        assert response.status_code == HTTPStatus.OK
        assert len(response.data) == 1
        assert response.data[0]['content'] == 'test1'

    def test_notes_apiview_authentication_failure(
            self,
            api_client: APIClient,
    ) -> None:
        """Test the notes apiview authentication."""

        response = api_client.post(
            reverse('notes:notes-notes'),
            data={'content': 'test1'},
            format='json',
        )

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_note_serializer_validation(self, api_client: APIClient, admin_user: User) -> None:
        """Test note serializer validation without content."""
        api_client.force_login(user=admin_user)

        response = api_client.post(
            reverse('notes:notes-notes'),
            data={},
            format='json',
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert str(response.data) == '{0}'.format(
            "{'content': [ErrorDetail(string='This field is required.', code='required')]}",
        )

    def test_share_note_serializer_validation(self, api_client: APIClient, admin_user: User) -> None:
        """Test share note serializer validation without content."""
        api_client.force_login(user=admin_user)
        normal_user = User(username='normal_user')
        normal_user.save()
        note = Note(user=admin_user, content='test1')
        note.save()

        response = api_client.post(
            reverse('notes:notes-share', kwargs={'id': note.id}),
            data={},
            format='json',
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert str(response.data) == '{0}'.format(
            "{'username': [ErrorDetail(string='This field is required.', code='required')]}",
        )
    
    
