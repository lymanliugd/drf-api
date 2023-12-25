from typing import Any

from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


from notes.models import Note
from notes.serializers import NoteSerializer, ShareNoteSerializer


class NotesApiView(APIView):
    """App notes api views"""

    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle GET requests from `api/notes` and `api/notes/<int:id>`.

        Returns:
            Http response with the list of notes for api/notes, 
            or the note with the parameter id
        """
        if kwargs.get('id'):
            note = get_object_or_404(Note.objects.filter(id=kwargs.get('id')))
            return Response(NoteSerializer(note, many=False).data)
        else:  
            notes = Note.objects.all()
            return Response(NoteSerializer(notes, many=True).data)
    
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle a PUT request to update a note instance.

        Args:
            request: the HTTP request
            args: additional arguments
            kwargs: additional keyword arguments

        Returns:
            the HTTP response
        """
        if not kwargs.get('id'):
            raise serializers.ValidationError(
                'Parameter id is required.',
            )
        
        if not request.data.get('content'):
            raise serializers.ValidationError(
                'Parameter id is required.',
            )
             
        note = get_object_or_404(Note.objects.filter(id=kwargs.get('id')))
        note.content = request.data.get('content')
        note.save()

        return Response({'Udate note id: {id} successfully'.format(id=note.id)})


    def post(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Handle a POST request to create a note instance.

        Args:
            request: HTTP request that initiates report generation
            args: varied amount of non-keyword arguments
            kwargs: varied amount of keyword arguments

        Returns:
            HTTP `Response` with the result of a note creation
        """
        serializer = NoteSerializer(data=request.data)
        # Validate received data. Return a 400 response if the data was invalid.
        serializer.is_valid(raise_exception=True)

        user = request.user
        note_data = serializer.validated_data
        Note.objects.create(user=user, content=note_data['content'])

        return Response({'Create the note: {content} successfully'.format(
            content=note_data['content'],
        )})
    
    def delete(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Handle a DELETE request to delete a note instance.

        Args:
            request: HTTP request that initiates report generation
            args: varied amount of non-keyword arguments
            kwargs: varied amount of keyword arguments

        Returns:
            HTTP `Response` with the result of a note creation
        """
        if not kwargs.get('id'):
            raise serializers.ValidationError(
                'Parameter id is required.',
            )
        
        note = get_object_or_404(Note, id=kwargs.get('id'))
        note.delete()
        return Response({'Delete the note id: {id} successfully'.format(id=kwargs.get('id'))})
    

class ShareNoteApiView(APIView):
    """Api view for share note"""

    permission_classes = [IsAuthenticated]
    serializer_class = ShareNoteSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle POST requests from `api/notes/<int:id>/share`.

        Args:
            request: Http request.

        Returns:
            Http response empty
        """
        serializer = ShareNoteSerializer(data=request.data)
        # Validate received data. Return a 400 response if the data was invalid.
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        print(data['user'])
        user = get_object_or_404(User, username=data['user']['username'])
        note = get_object_or_404(Note, id=kwargs['id'])
        new_note = Note(user=user, content=note.content)
        new_note.save()
        return Response(
            {
                'Share the note: {content} with user: {username} successfully'.format(
                    content=note.content,
                    username=user.username,
                ),
            },
        )
    

class SearchNoteApiView(APIView):
    """Api view for searching note"""

    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle GET requests from `api/notes/search/<str: query>`.

        Args:
            request: Http request.

        Raises:
            ParseError: If the query was not provided.

        Returns:
            Http response with the list of notes for the request user.
        """
        user = request.user
        query = kwargs.get('query')
        notes = Note.objects.filter(user=user, content__contains=query)
        return Response(NoteSerializer(notes, many=True).data)