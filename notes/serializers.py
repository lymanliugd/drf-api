from rest_framework import serializers

from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    """Model note serializer."""

    class Meta:
        model = Note
        fields = ['id', 'content']


class ShareNoteSerializer(serializers.ModelSerializer):
    """Api ShareNote serializer."""

    username = serializers.CharField(source='user.username')

    class Meta:
        model = Note
        fields = ['id', 'username']
        extra_kwargs = {'username': {'required': True}}
