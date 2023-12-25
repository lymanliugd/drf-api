"""App notes urls"""
from django.urls import path

from notes import api_views

urlpatterns = [
    path(
        'notes/', 
        api_views.NotesApiView.as_view(),
        name='app-notes',
    ),
    path(
        'notes/<int:id>', 
        api_views.NotesApiView.as_view(),
        name='app-note',
    ),
    path(
        'notes/<int:id>/share', 
        api_views.ShareNoteApiView.as_view(),
        name='app-note-share',
    ),
    path(
        'search/<str:query>', 
        api_views.SearchNoteApiView.as_view(),
        name='app-note-search',
    ),
]
